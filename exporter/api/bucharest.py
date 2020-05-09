import logging
import time
import polyline
from gtfslib.dao import Dao
from gtfslib.model import Agency, FeedInfo, Route, Trip, Stop, StopTime, Shape, ShapePoint
from exporter.provider import ApiDataProvider
from exporter.api.requests import RequestExecutor
from exporter.util.http import Request
from exporter.util.perf import measure_execution_time

logger = logging.getLogger("grfsexporter")

SLEEP_TIME = 0

BASE_URL = "https://info.stbsa.ro/rp/api"


class BucharestApiDataProvider(ApiDataProvider):
    # base api url

    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info
        self.feedinfo = FeedInfo(self.feed_id)
        self.request_executor = RequestExecutor()

        self.line_request = Request(BASE_URL + "/lines/")
        self.line_detail_request = Request(BASE_URL + "/lines/{0}/direction/{1}")
        self.line_stops_request = Request(BASE_URL + "/lines/{0}/stops/{1}")

    def load_data_source(self, dao: Dao) -> bool:
        self.dao = dao
        self.__load_agencies()
        self.__load_routes()
        self.__load_trips()
        return super().load_data_source(dao)

    @measure_execution_time
    def __load_agencies(self):
        self.agency_ids = set()
        logger.info("Importing agencies...")

        stb = Agency(self.feed_id, 1, "STB SA", "https://stbsa.ro,Europe/Bucharest", "Europe/Bucharest", **{
            "agency_lang": "ro",
            "agency_email": "contact@stbsa.ro",
            "agency_fare_url": "http://stbsa.ro/portofel_electronic.php",
            "agency_phone": "0213110595"
        })

        metrorex = Agency(self.feed_id, 2, "METROREX SA", "https://metrorex.ro,Europe/Bucharest", "Europe/Bucharest",
                          **{
                              "agency_lang": "ro",
                              "agency_email": "contact@metrorex.ro",
                              "agency_fare_url": "http://metrorex.ro/titluri_de_calatorie_p1381-1",
                              "agency_phone": "0213193601"
                          })
        self.dao.add(stb)
        self.agency_ids.add(stb.agency_id)
        self.dao.add(metrorex)
        self.agency_ids.add(metrorex.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 2)
        pass

    def __load_routes(self):
        ### https://info.stbsa.ro/rp/api/lines/
        stops = set()
        route_data = self.line_request()
        logger.info(f"total lines to process {len(route_data['lines'])}")
        for line_nb, line in enumerate(route_data["lines"]):
            logger.info(f" - processing line {line_nb} of {len(route_data['lines'])}")
            r = Route(self.feed_id, line['id'], line['organization']['id'],
                      self.__parse_route_type(line['type']), **{
                    "route_color": line['color'],
                    "route_text_color": "000000",
                })
            self.dao.add(r)
            # self.dao.flush()

            # fetch both directions
            for direction in [0, 1]:
                time.sleep(SLEEP_TIME)

                trip_data = self.line_detail_request(r.route_id, direction)
                trips = []

                shape_points = polyline.decode(trip_data['segment_path'])

                logger.debug("processing shape")
                shp = Shape(self.feed_id, f"shp{r.agency_id}_{r.route_id}_{direction}")
                self.dao.add(shp)
                for shp_point_index, shape_point in enumerate(shape_points):
                    shp_point = ShapePoint(self.feed_id, shp.shape_id, shp_point_index, shape_point[0],
                                           shape_point[1], 0)
                    self.dao.add(shp_point)

                logger.info(f"total stops to process {len(trip_data['stops'])}")
                for stop_index, stop in enumerate(trip_data['stops']):
                    logger.info(f" - processing stop {stop_index + 1} of {len(trip_data['stops'])}")
                    s = Stop(self.feed_id, stop['id'], stop['name'], stop['lat'], stop['lng'])
                    if s.stop_id not in stops:
                        stops.add(s.stop_id)
                        self.dao.add(s)
                        # self.dao.flush()

                    time.sleep(SLEEP_TIME)

                    self.process_route_stop(r, s, shp, direction, stop_index, trips)
                    # self.request_executor.enqueue_request(process_route_stop, s, r, direction, stop_index)
                    # tasks = []
                    # tasks.append(self.process_route_stop(r, s, shp, direction, stop_index, trips))
                    # responses = asyncio.run(await asyncio.gather(*tasks, return_exceptions=True))

            self.dao.flush()

    @measure_execution_time
    def process_route_stop(self, r: Route, s: Stop, shp: Shape, direction, stop_index, trips):
        # executing request
        stoptime_data = self.line_stops_request(r.route_id, s.stop_id)

        index = 0
        if stoptime_data[0]['lines'][0]['timetable'] is None:
            return

        for timetable in stoptime_data[0]['lines'][0]['timetable']:
            for minute in timetable['minutes']:
                if len(trips) <= index:
                    t = Trip(self.feed_id, f"{r.agency_id}_{r.route_id}_{direction}_{index}",
                             r.route_id,
                             f"s{r.agency_id}",
                             **{"trip_short_name": stoptime_data[0]['name'],
                                "trip_headsign": stoptime_data[0]['description'],
                                "shape_id": shp.shape_id})
                    trips.append(t)
                    r.trips.append(t)

                    self.dao.add(t)
                    # self.dao.flush()
                else:
                    t = trips[index]

                # calculate time (in seconds) since midnight
                schedule_time = int(timetable['hour']) * 3600 + int(minute) * 60

                st = StopTime(self.feed_id, t.trip_id, s.stop_id, stop_index, schedule_time, schedule_time, 0)
                t.stop_times.append(st)
                self.dao.add(st)
                # self.dao.flush()
                index += 1

    def __load_trips(self):
        pass

    def __parse_route_type(self, type: str):
        switcher = {
            'BUS': Route.TYPE_BUS,
            'SUBWAY': Route.TYPE_SUBWAY,
            'TRAM': Route.TYPE_TRAM,
            'CABLE_CAR': Route.TYPE_CABLECAR,
        }

        return switcher.get(type)
