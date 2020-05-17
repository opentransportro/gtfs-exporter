import csv
import logging

from gtfslib.dao import Dao
from gtfslib.model import Agency, FeedInfo, Calendar, CalendarDate, Route, Shape, ShapePoint, Stop

from exporter.api.requests import RequestExecutor
from exporter.provider import ApiDataProvider
from exporter.util.http import Request
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import DataNormalizer
import requests as requests

logger = logging.getLogger("gtfsexporter")

SLEEP_TIME = 0

TOKEN = 'eyJhbGciOiJIUzI1NiJ9.UGhnZDFrdndzWTFlUTRCd2pvbnVkR29pVG5ZQVROTDk.m9vK9qfiQtfx9_YyFrpfCRVEp6WFaRT8C_R65483d9o'


class ClujApiDataProvider(ApiDataProvider):
    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info
        self.feedinfo = FeedInfo(self.feed_id)
        self.request_executor = RequestExecutor()
        self.url = "https://m-go.wink.ro/api"

        self.line_detail_request = Request(self.url + "/route/all/{0}", headers={'azza': TOKEN})

    @measure_execution_time
    def load_data_source(self, dao: Dao) -> bool:
        self.dao = dao
        self._load_agencies()
        self.__load_services()
        self.__load_routes()
        dn = DataNormalizer(dao, self.feed_id)
        dn.normalize()
        dao.commit()

        return super().load_data_source(dao)

    def _load_agencies(self):
        self.agency_ids = set()
        logger.info("Importing agencies...")

        self.ctp_cluj = Agency(self.feed_id, 1, "Compania de Transport Public Cluj", "http://www.ctpcj.ro",
                               "Europe/Bucharest", **{
                "agency_lang": "ro",
                "agency_email": "sugestii@ctpcj.ro",
                "agency_fare_url": "http://www.ctpcj.ro/index.php/ro/tarife/transport-urban",
                "agency_phone": "0264-430917"
            })

        self.dao.add(self.ctp_cluj)
        self.agency_ids.add(self.ctp_cluj.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 1)
        pass

    def __load_services(self):
        start_date = CalendarDate.fromYYYYMMDD("20200301")
        end_date = CalendarDate.fromYYYYMMDD("20201231")

        def save_calendar_for(service_id: str, dow: []):
            service = Calendar(self.feed_id, service_id)
            dates = []
            for d in CalendarDate.range(start_date, end_date.next_day()):
                if dow[d.dow()] == 1:
                    d.service_id = service.service_id
                    d.feed_id = self.feed_id

                    # add to list to be saved
                    dates.append(d)

            self.dao.add(service)
            self.dao.bulk_save_objects(dates)

        save_calendar_for("lv", [1, 1, 1, 1, 1, 0, 0])
        save_calendar_for("s", [0, 0, 0, 0, 0, 1, 0])
        save_calendar_for("d", [0, 0, 0, 0, 0, 0, 1])

    def __load_routes(self):
        self.stops = set()

        # The API offers a paging-like mechanism to fetch routes
        for page in range(0, 12):
            line_data = self.line_detail_request(str(page))['data']
            if line_data:
                line_total = len(line_data)
                logger.info(f"Total lines to process \t\t\t{line_total}")
                for line_idx, line in enumerate(line_data):
                    logger.info(f"\tprocessing line {line['routeShortname']} \t\t\t [{line_idx}/{line_total}]")
                    r = Route(self.feed_id, line['_id'], self.ctp_cluj.agency_id,
                              self.__parse_route_type(line['routeType']), **{
                            "route_color": line['routeColor'],
                            "route_text_color": "000000",
                            "route_short_name": line['routeShortname']
                        })
                    r.route_long_name = line['routeName']

                    self.__process_route(r, line['routeWayCoordinates'], line['routeRoundWayCoordinates'],
                                         line['routeWaypoints'], line['routeRoundWaypoints'])

    def __process_route(self, route, wayCoordinates, roundWayCoordinates, waypoints, roundWaypoints):
        logger.debug(f" - processing trips for {route.name()}")

        response_lv = requests.get(f"http://www.ctpcj.ro/orare/csv/orar_{route.name()}_lv.csv",
                                headers={'Referer': 'http://www.ctpcj.ro'})

        response_s = requests.get(f"http://www.ctpcj.ro/orare/csv/orar_{route.name()}_s.csv",
                                   headers={'Referer': 'http://www.ctpcj.ro'})

        response_d = requests.get(f"http://www.ctpcj.ro/orare/csv/orar_{route.name()}_d.csv",
                                  headers={'Referer': 'http://www.ctpcj.ro'})

        if response_lv.status_code == 200:
            decoded_content = response_lv.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            print(my_list)

            self.dao.add(route)

            self.__load_trip(route=route, direction=0, coordinates=wayCoordinates, waypoints=waypoints)
            self.__load_trip(route=route, direction=1, coordinates=roundWayCoordinates, waypoints=roundWaypoints)

    def __load_trip(self, route, direction, coordinates, waypoints):
        logger.debug("processing shape")
        shp = Shape(route.feed_id, f"shp{route.agency_id}_{route.route_id}_{direction}")
        self.dao.add(shp)
        dao_shape_pts = []
        for shp_point_index, shape_point in enumerate(coordinates):
            shp_point = ShapePoint(route.feed_id, shp.shape_id, shp_point_index, shape_point['lat'],
                                   shape_point['lng'],
                                   -999999)
            dao_shape_pts.append(shp_point)
        self.dao.bulk_save_objects(dao_shape_pts)

        trips = []

        logger.debug(f"total stops to process {len(waypoints)}")
        for stop_index, stop in enumerate(waypoints):
            logger.debug(f" - processing stop {stop_index + 1} of {len(waypoints)}")
            s = Stop(self.feed_id, stop['_id'], stop['name'], stop['lat'], stop['lng'])
            if s.stop_id not in self.stops:
                self.stops.add(s.stop_id)
                self.dao.add(s)

        self.process_route_trips(route, shp, direction, trips, 'lv')

    def process_route_trips(self, r: Route, shape, direction, trips, service_id):

        return True

    @staticmethod
    def __parse_route_type(type: str):
        switcher = {
            '1': Route.TYPE_BUS,
            '2': Route.TYPE_SUBWAY,
            '3': Route.TYPE_TRAM,
            '4': Route.TYPE_CABLECAR,
        }

        return switcher.get(type)
