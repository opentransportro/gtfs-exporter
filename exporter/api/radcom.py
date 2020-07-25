import logging
import time

import polyline
from gtfslib.dao import Dao
from gtfslib.model import FeedInfo, Route, Trip, Stop, StopTime, Shape, ShapePoint, Calendar, CalendarDate

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

        import datetime
        self.service_id = "LV" if datetime.datetime.today().weekday() < 5 else "SD"

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
        import datetime
        year = datetime.datetime.now().year
        start_date = CalendarDate.fromYYYYMMDD(f"{year}0101")
        end_date = CalendarDate.fromYYYYMMDD(f"{year}1231")

        def save_calendar_for(service_id: str, dow: []):
            service = Calendar(self.feed_id, service_id)
            dates = []
            for d in CalendarDate.range(start_date, end_date.next_day()):
                if dow[d.dow()] == 1:
                    d.service_id = service.service_id
                    d.feed_id = self.feed_id

                    # add to list to be saved
                    dates.append(d)

            self._safe_insert(service)
            self._safe_bulk_insert(dates)
            self.dao.flush()

        save_calendar_for("LV", [1, 1, 1, 1, 1, 0, 0])
        save_calendar_for("SD", [0, 0, 0, 0, 0, 1, 1])

    def _load_routes(self):
        self._clear_trips()

        stops = set()
        route_data = self.line_request()
        logger.info(f"Total lines to process \t\t\t{len(route_data['lines'])}")
        for line_nb, line in enumerate(route_data["lines"]):
            logger.info(f"\tprocessing line {line['name']} \t\t\t [{line_nb + 1}/{len(route_data['lines'])}]")
            r = Route(self.feed_id, line['id'], line['organization']['id'],
                      self._parse_route_type(line['type']), **{
                    "route_color": line['color'],
                    "route_text_color": "000000",
                    "route_short_name": line['name']
                })

            # fetch both directions
            for direction in [0, 1]:
                trip_data = self.line_detail_request(r.route_id, direction)
                r.route_long_name = f"{trip_data['direction_name_tur']} - {trip_data['direction_name_retur']}"

                trips = []

                shape_points = polyline.decode(trip_data['segment_path'])

                logger.debug("processing shape")
                shp = Shape(self.feed_id, f"shp{r.agency_id}_{r.route_id}_{direction}")
                self._safe_insert(shp)

                dao_shape_pts = []
                for shp_point_index, shape_point in enumerate(shape_points):
                    shp_point = ShapePoint(self.feed_id, shp.shape_id, shp_point_index, shape_point[0], shape_point[1],
                                           -999999)
                    dao_shape_pts.append(shp_point)
                self._safe_bulk_insert(dao_shape_pts)

                logger.debug(f"total stops to process {len(trip_data['stops'])}")
                for stop_index, stop in enumerate(trip_data['stops']):
                    logger.debug(f" - processing stop {stop_index + 1} of {len(trip_data['stops'])}")
                    s = Stop(self.feed_id, stop['id'], stop['name'], stop['lat'], stop['lng'])
                    if s.stop_id not in stops:
                        stops.add(s.stop_id)
                        self._safe_insert(s)

                    result = self._process_route_stop(r, s, shp, direction, stop_index, trips)

            self._safe_insert(r)
            self.dao.flush()

    def _process_route_stop(self, r: Route, s: Stop, shp: Shape, direction, stop_index, trips):
        # executing request
        stoptime_data = self.line_stops_request(r.route_id, s.stop_id)

        index = 0
        if len(stoptime_data[0]['lines']) == 0:
            logger.warning(f"\t\tStop information missing for route {r.route_short_name} and stop {s.stop_name}")
        if len(stoptime_data[0]['lines']) == 0 or stoptime_data[0]['lines'][0]['timetable'] is None:
            return False

        stop_times_dao = []
        timetables = self._convert_timetable(stoptime_data[0]['lines'][0]['timetable'])
        for schedule_time in timetables:
            if len(trips) <= index:
                t = Trip(self.feed_id, f"{r.agency_id}_{r.route_id}_{direction}_{self.service_id}_{index}",
                         r.route_id,
                         self.service_id,
                         **{"trip_short_name": stoptime_data[0]['name'],
                            "trip_headsign": stoptime_data[0]['description'],
                            "direction_id": direction,
                            "shape_id": shp.shape_id})
                trips.append(t)

                self._safe_insert(t)
            else:
                t = trips[index]
                if t.stop_times[-1].arrival_time > schedule_time:
                    continue

            st = StopTime(self.feed_id, t.trip_id, s.stop_id, stop_index, schedule_time, schedule_time, 0, **{
                # "stop_headsign": "00000"
            })
            t.stop_times.append(st)
            stop_times_dao.append(st)

            index += 1

        self._safe_bulk_insert(stop_times_dao)
        self.dao.flush()
        return True

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

    def _safe_bulk_insert(self,bulk):
        """
        performs a safe bulk insert, that updates existing items
        or creates a new record if not found
        """
        with self.dao.session().begin_nested():
            try:
                for record in bulk:
                    self._safe_insert(record)

                self.dao.flush()

            except Exception as e:
                logger.error(f"An exception was meet in bulk insert:{e}")
                self.dao.session().rollback()

    def _safe_insert(self,record):
        """
        performs a safe insert, that updates existing items
        or creates a new record if not found
        """
        self.dao.session().merge(record)

    def _clear_trips(self):
        """
        drops all the trips from the databse with the service id
        equal to the one for the current execution (LV or SD)
        """
        self.dao.session().query(Trip).filter(Trip.service_id == self.service_id).delete(synchronize_session=False)
        self.dao.session().commit()
        logger.debug(f"Successfully droped trips with service id: {self.service_id}")
