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
        self.service_ids = set()

        start_date = CalendarDate.fromYYYYMMDD("20200501")
        end_date = CalendarDate.fromYYYYMMDD("20201231")

        def save_calendar_for(service_id: str, dow: []):
            self.service_ids.add(service_id)

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
                    route = Route(self.feed_id, line['_id'], self.ctp_cluj.agency_id,
                                  self.__parse_route_type(line['routeType']), **{
                            "route_color": line['routeColor'],
                            "route_text_color": "000000",
                            "route_short_name": line['routeShortname']
                        })
                    route.route_long_name = line['routeName']

                    self.dao.add(route)

                    self.__process_route(route, line['routeWayCoordinates'], line['routeRoundWayCoordinates'],
                                         line['routeWaypoints'], line['routeRoundWaypoints'])

    def __process_route(self, route, wayCoordinates, roundWayCoordinates, waypoints, roundWaypoints):
        logger.debug(f" - processing trips for {route.name()}")

        self.__process_shape(route, 0, wayCoordinates)
        self.__process_shape(route, 1, roundWayCoordinates)

        for service_id in self.service_ids:
            in_times, out_times = self.__load_timetables(route, service_id)

            if len(in_times) > 0:
                # process individually each direction instance
                self.__process_trip(waypoints, in_times)
                self.__process_trip(roundWaypoints, out_times)

    def __process_shape(self, route, direction, coordinates):
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

    def __process_trip(self, waypoints, times):
        logger.debug(f"total stops to process {len(waypoints)}")
        for stop_index, stop in enumerate(waypoints):
            logger.debug(f" - processing stop {stop_index + 1} of {len(waypoints)}")
            if stop['name']:
                s = Stop(self.feed_id, str(stop['stationID']), stop['name'], stop['lat'], stop['lng'])
                if s.stop_id not in self.stops:
                    self.stops.add(s.stop_id)
                    self.dao.add(s)

    @staticmethod
    def __load_timetables(route: Route, service_id):
        # TODO: move HTTP business
        response = requests.get(f"http://www.ctpcj.ro/orare/csv/orar_{route.name()}_{service_id}.csv",
                                headers={'Referer': 'http://www.ctpcj.ro'})

        in_times = []
        out_times = []
        if response.status_code == 200:
            decoded_content = response.content.decode('utf-8')

            timetable_cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            csv_lines = list(timetable_cr)

            if len(csv_lines) <= 5:
                return [], []

            for csv_line in range(5, len(csv_lines)):
                if len(csv_lines[csv_line]) > 0:
                    in_times.append(csv_lines[csv_line][0])
                    out_times.append(csv_lines[csv_line][1])

            print(in_times)

        return in_times, out_times

    @staticmethod
    def __parse_route_type(type: str):
        switcher = {
            '1': Route.TYPE_BUS,
            '2': Route.TYPE_SUBWAY,
            '3': Route.TYPE_TRAM,
            '4': Route.TYPE_CABLECAR,
        }

        return switcher.get(type)
