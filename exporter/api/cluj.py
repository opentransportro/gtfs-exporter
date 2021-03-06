import datetime as datetime
import logging
import math

from exporter.gtfs.dao import Dao
from exporter.gtfs.model import Agency, FeedInfo, Calendar, CalendarDate, Route, Shape, ShapePoint, Stop, Trip, StopTime

from exporter.provider import ApiDataProvider
from exporter.util.http import Request, CsvDecoder
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import DataNormalizer

logger = logging.getLogger("gtfsexporter")


class ClujApiDataProvider(ApiDataProvider):
    WINK_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.UGhnZDFrdndzWTFlUTRCd2pvbnVkR29pVG5ZQVROTDk.m9vK9qfiQtfx9_YyFrpfCRVEp6WFaRT8C_R65483d9o'

    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info
        self.feedinfo = FeedInfo(self.feed_id)

        self.line_detail_request = Request("https://m-go.wink.ro/api" + "/route/all/{0}",
                                           headers={'azza': ClujApiDataProvider.WINK_TOKEN})
        self.times_request = Request("http://www.ctpcj.ro/orare/csv/orar_{0}_{1}.csv",
                                     headers={'Referer': 'http://www.ctpcj.ro'},
                                     decoder=CsvDecoder())

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

        self.ctp_cluj = Agency(self.feed_id, 5, "Compania de Transport Public Cluj", "http://www.ctpcj.ro",
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

        today = datetime.datetime.today()
        start_date = CalendarDate.fromYYYYMMDD(today.strftime('%Y%m%d'))
        end_date = CalendarDate.fromYYYYMMDD(datetime.date(today.year, 12, 31).strftime('%Y%m%d'))

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
                    route = Route(self.feed_id,
                                  str(line['routeId']),
                                  self.ctp_cluj.agency_id,
                                  self.__parse_route_type(line['routeType']), **{
                            "route_color": line['routeColor'],
                            "route_text_color": "000000",
                            "route_short_name": line['routeShortname']
                        })
                    route.route_long_name = line['routeName']

                    is_route_supported = self.__process_route(route, line['routeWayCoordinates'],
                                                              line['routeRoundWayCoordinates'],
                                                              line['routeWaypoints'], line['routeRoundWaypoints'])

                    if is_route_supported:
                        self.dao.add(route)

    def __process_route(self, route, way_coordinates, round_way_coordinates, waypoints, round_waypoints):
        logger.debug(f" - processing trips for {route.name()}")

        shape_in = self.__process_shape(route, 0, way_coordinates)
        shape_out = self.__process_shape(route, 1, round_way_coordinates)

        is_route_supported = True

        for service_id in self.service_ids:
            in_times, out_times = self.__load_timetables(route, service_id)

            if len(in_times) > 0:
                self.__process_trips(route, shape_in, 0, waypoints, in_times, service_id)
                is_route_supported = True
            if len(out_times) > 0:
                self.__process_trips(route, shape_out, 1, round_waypoints, out_times, service_id)
                is_route_supported = True

        return is_route_supported

    def __process_trips(self, route, shape, direction, waypoints, timepoints, service_id):
        logger.debug(f"total stops to process {len(waypoints)}")

        for timepoint_idx, timepoint in enumerate(timepoints):
            trip_id = f"{route.agency_id}_{route.route_id}_{direction}_{service_id}_{timepoint_idx}"

            trip = Trip(self.feed_id,
                        trip_id,
                        route.route_id,
                        service_id,
                        **{"trip_short_name": waypoints[0]['name'] + '-' + waypoints[-1]['name'],
                           "trip_headsign": waypoints[-1]['name'],
                           "direction_id": direction,
                           "shape_id": shape.shape_id
                           }
                        )

            self.__process_stops_and_times(trip, timepoint, waypoints)

            self.dao.add(trip)

    def __process_stops_and_times(self, trip, timepoint, waypoints):
        filtered_waypoints = [x for x in waypoints if x['name']]
        for waypoint_idx, waypoint in enumerate(filtered_waypoints):
            stop = Stop(self.feed_id,
                        str(waypoint['stationID']),
                        waypoint['name'],
                        waypoint['lat'],
                        waypoint['lng'])

            if stop.stop_id not in self.stops:
                self.stops.add(stop.stop_id)
                self.dao.add(stop)

            distance_traveled = math.floor(waypoint['total'])

            first_departure_time = 0
            if waypoint_idx == 0:
                departure_time = self.__convert_tsm(timepoint)
                stop_time = StopTime(feed_id=self.feed_id,
                                     trip_id=trip.trip_id,
                                     stop_id=stop.stop_id,
                                     stop_sequence=0,
                                     departure_time=departure_time,
                                     arrival_time=departure_time,
                                     shape_dist_traveled=distance_traveled,
                                     timepoint=1)
                first_departure_time = departure_time
            elif waypoint_idx == (len(filtered_waypoints) - 1):
                delta_time = self.__process_time_for_distance(waypoint['total'])
                end_time = int(delta_time + first_departure_time)
                stop_time = StopTime(feed_id=self.feed_id,
                                     trip_id=trip.trip_id,
                                     stop_id=stop.stop_id,
                                     stop_sequence=waypoint_idx,
                                     departure_time=end_time,
                                     arrival_time=end_time,
                                     shape_dist_traveled=distance_traveled,
                                     timepoint=1)
            else:
                stop_time = StopTime(feed_id=self.feed_id,
                                     trip_id=trip.trip_id,
                                     stop_id=stop.stop_id,
                                     stop_sequence=waypoint_idx,
                                     departure_time=None,
                                     arrival_time=None,
                                     shape_dist_traveled=distance_traveled,
                                     interpolated=True,
                                     timepoint=0)

            trip.stop_times.append(stop_time)

    def __process_shape(self, route, direction, coordinates):
        logger.debug("processing shape")
        shp = Shape(route.feed_id, f"shp_{route.agency_id}_{route.route_id}_{direction}")
        self.dao.add(shp)
        dao_shape_pts = []
        for shp_point_index, shape_point in enumerate(coordinates):
            shp_point = ShapePoint(route.feed_id,
                                   shp.shape_id,
                                   shp_point_index,
                                   shape_point['lat'],
                                   shape_point['lng'],
                                   -999999)
            dao_shape_pts.append(shp_point)
        self.dao.bulk_save_objects(dao_shape_pts)

        return shp

    def __load_timetables(self, route: Route, service_id):
        in_times = []
        out_times = []

        csv_lines = self.times_request(route.name(), service_id)

        if csv_lines:
            if len(csv_lines) <= 5:
                return [], []

            for csv_line in range(5, len(csv_lines)):
                if len(csv_lines[csv_line]) > 0:
                    in_times.append(csv_lines[csv_line][0].strip())
                    out_times.append(csv_lines[csv_line][1].strip())

        return [x for x in in_times if x], [x for x in out_times if x]

    @staticmethod
    def __process_time_for_distance(distance) -> int:
        # 15 km / h = 15000 m / 3600 s = 4.1 m / s
        average_speed = 4.1
        return int(distance / average_speed)

    @staticmethod
    def __parse_route_type(route_type_literal: str):
        switcher = {
            '1': Route.TYPE_BUS,
            '2': Route.TYPE_TRAM,
            '3': Route.TYPE_CABLECAR,
            '4': Route.TYPE_SUBWAY,
        }

        return switcher.get(route_type_literal)

    @staticmethod
    def __convert_tsm(time) -> int:
        # check for time typos; adapt to variances of human mistakes
        time_parts = time.split(':')

        if len(time_parts) != 2:
            time_parts = time.split('.')

        hours, minutes = map(str, time_parts)

        if int(hours) > 24:
            hours = hours[::-1]

        date = datetime.datetime.strptime(f"{hours}:{minutes}", '%H:%M')  # for example
        return int(datetime.timedelta(hours=date.hour, minutes=date.minute,
                                      seconds=date.second).total_seconds())
