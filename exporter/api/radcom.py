import logging
import datetime

import polyline
from exporter.gtfs.dao import Dao
from exporter.gtfs.model import FeedInfo, Route, Trip, Stop, StopTime, Shape, ShapePoint, Calendar, CalendarDate, Agency

from exporter.provider import ApiDataProvider
from exporter.util.http import Request
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import DataNormalizer

logger = logging.getLogger("gtfsexporter")


class RadcomApiDataProvider(ApiDataProvider):
    def __init__(self, url: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info
        self.feedinfo = FeedInfo(self.feed_id)

        self.line_request = Request(url + "/lines/")
        self.line_detail_request = Request(url + "/lines/{0}/direction/{1}")
        self.line_stops_request = Request(url + "/lines/{0}/stops/{1}")

    @measure_execution_time
    def load_data_source(self, dao: Dao) -> bool:
        self.dao = dao
        self._load_agencies()
        self._load_services()
        self._load_routes()
        dn = DataNormalizer(dao, self.feed_id)
        dn.normalize()
        dao.commit()

        return super().load_data_source(dao)

    def _load_agencies(self):
        pass

    def _load_services(self):
        year = datetime.datetime.now().year
        start_date = CalendarDate.fromYYYYMMDD(f"{year}0101")
        end_date = CalendarDate.fromYYYYMMDD(f"{year}1231")

        def save_calendar_for(service_id: str, dow: []):
            service = Calendar(self.feed_id, service_id)
            self.dao.update(service)
            self.dao.flush()

        save_calendar_for("LV", [1, 1, 1, 1, 1, 0, 0])
        save_calendar_for("SD", [0, 0, 0, 0, 0, 1, 1])
                
        self.service_id = "LV" if datetime.datetime.today().weekday() < 5 else "SD"

    def _load_routes(self):
        self._clear_trips()

        stops = set()
        route_data = self.line_request()
        logger.info(f"Total lines to process \t\t\t{len(route_data['lines'])}")
        for line_nb, line in enumerate(route_data["lines"]):
            logger.info(f"\tprocessing line {line['name']} \t\t\t [{line_nb + 1}/{len(route_data['lines'])}]")
            r = Route(self.feed_id, line['id'], line['organization']['id'], self._parse_route_type(line['type']), **{
                    "route_color": line['color'],
                    "route_text_color": "000000",
                    "route_short_name": line['name']
                })

            # fetch both directions
            for direction in [0, 1]:
                trip_data = self.line_detail_request(r.route_id, direction)
                r.route_long_name = f"{trip_data['direction_name_tur']} - {trip_data['direction_name_retur']}"

                trips = []
                shape_id = f"shp{r.agency_id}_{r.route_id}_{direction}"

                shape_count = self.dao.session.query(Shape).filter(Shape.shape_id == shape_id).count()
                shape_points_count = self.dao.session.query(ShapePoint).filter(ShapePoint.shape_id == shape_id).count()

                if shape_count == 0 or shape_points_count == 0:
                    shape_points = polyline.decode(trip_data['segment_path'])
                    logger.debug("processing shape")
                    shp = Shape(self.feed_id, f"shp{r.agency_id}_{r.route_id}_{direction}")
                    self.dao.add(shp)

                    for shp_point_index, shape_point in enumerate(shape_points):
                        self.dao.add(ShapePoint(self.feed_id, shp.shape_id, shp_point_index, shape_point[0], shape_point[1], -999999))
                else:
                    shp = self.dao.session.query(Shape).get([self.feed_id, shape_id])

                logger.debug(f"total stops to process {len(trip_data['stops'])}")
                for stop_index, stop in enumerate(trip_data['stops']):
                    logger.debug(f" - processing stop {stop_index + 1} of {len(trip_data['stops'])}")
                    s = Stop(self.feed_id, stop['id'], stop['name'], stop['lat'], stop['lng'])
                    if s.stop_id not in stops:
                        stops.add(s.stop_id)
                        self.dao.update(s)

                    result = self._process_route_stop(r, s, shp, direction, stop_index, trips)

            self.dao.update(r)
            self.dao.flush()

    def _process_route_stop(self, r: Route, s: Stop, shp: Shape, direction, stop_index, trips):
        stoptime_data = self.line_stops_request(r.route_id, s.stop_id)

        index = 0
        if len(stoptime_data[0]['lines']) == 0:
            logger.warning(f"\t\tStop information missing for route {r.route_short_name} and stop {s.stop_name}")
        if len(stoptime_data[0]['lines']) == 0 or stoptime_data[0]['lines'][0]['timetable'] is None:
            return

        for schedule_time in self._convert_timetable(stoptime_data[0]['lines'][0]['timetable']):
            if len(trips) <= index:
                t = Trip(self.feed_id, f"{r.agency_id}_{r.route_id}_{direction}_{self.service_id}_{index}",
                         r.route_id,
                         self.service_id,
                         **{"trip_short_name": stoptime_data[0]['name'],
                            "trip_headsign": stoptime_data[0]['description'],
                            "direction_id": direction,
                            "shape_id": shp.shape_id})
                trips.append(t)
                self.dao.add(t)
            else:
                t = trips[index]
                if t.stop_times[-1].arrival_time > schedule_time:
                    continue

            if len(t.stop_times):
                t.stop_times[-1].stop_headsign = s.stop_name;

            t.stop_times.append(StopTime(self.feed_id, t.trip_id, s.stop_id, stop_index, schedule_time, schedule_time, 0))

            index += 1

    @staticmethod
    def _convert_timetable(timetable) -> list:
        stoptimes = list()
        for t in timetable:
            for m in t['minutes']:
                schedule_time = int(t['hour']) * 3600 + int(m) * 60
                stoptimes.append(schedule_time)
        stoptimes.sort()

        return list(dict.fromkeys(stoptimes))

    @staticmethod
    def _parse_route_type(type: str):
        switcher = {
            'BUS': Route.TYPE_BUS,
            'SUBWAY': Route.TYPE_SUBWAY,
            'TRAM': Route.TYPE_TRAM,
            'CABLE_CAR': Route.TYPE_CABLECAR,
        }

        return switcher.get(type)

    def _clear_trips(self):
        """
        drops all the trips from the databse with the service id
        equal to the one for the current execution (LV or SD)
        """
        trips_to_delete = self.dao.session.query(Trip).filter(Trip.service_id == self.service_id).all()
        for trip in trips_to_delete:
            self.dao.session.query(StopTime).filter(StopTime.trip_id == trip.trip_id).delete();

        self.dao.session.query(Trip).filter(Trip.service_id == self.service_id).delete();
        self.dao.flush()

        logger.info(f"Successfully droped trips with service id: {self.service_id}")


class BucharestApiDataProvider(RadcomApiDataProvider):
    # base api url
    BASE_URL = "https://info.stbsa.ro/rp/api"

    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(BucharestApiDataProvider.BASE_URL, feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info

    def _load_agencies(self):
        self.agency_ids = set()
        logger.info("Importing agencies...")

        stb = Agency(self.feed_id, 1, "STB SA", "https://stbsa.ro", "Europe/Bucharest", **{
            "agency_lang": "ro",
            "agency_email": "contact@stbsa.ro",
            "agency_fare_url": "http://stbsa.ro/portofel_electronic.php",
            "agency_phone": "0213110595"
        })

        metrorex = Agency(self.feed_id, 2, "METROREX SA", "https://metrorex.ro", "Europe/Bucharest",
                          **{
                              "agency_lang": "ro",
                              "agency_email": "contact@metrorex.ro",
                              "agency_fare_url": "http://metrorex.ro/titluri_de_calatorie_p1381-1",
                              "agency_phone": "0213193601"
                          })
        self.dao.update(stb)
        self.agency_ids.add(stb.agency_id)

        self.dao.update(metrorex)
        self.agency_ids.add(metrorex.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 2)


class ConstantaApiDataProvider(RadcomApiDataProvider):
    # base api url
    BASE_URL = "https://info.ctbus.ro/rp/api"

    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(ConstantaApiDataProvider.BASE_URL, feed_id, lenient, disable_normalization, **kwargs)

    def _load_agencies(self):
        self.agency_ids = set()
        logger.info("Importing agencies...")

        stb = Agency(self.feed_id, 1, "Regia Autonomă de Transport în Comun Constanța", "https://ctbus.ro",
                     "Europe/Bucharest", **{
                "agency_lang": "ro",
                "agency_email": "contact@ctbus.ro",
                "agency_fare_url": "https://www.ctbus.ro/#Tarife",
                "agency_phone": "0241694960"
            })

        self.dao.update(stb)
        self.agency_ids.add(stb.agency_id)

        logger.info("Imported %d agencies" % 1)
