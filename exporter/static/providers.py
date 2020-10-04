import datetime
import logging
import math
import os
import re
import unicodedata
from zipfile import ZipFile

import dateutil
import pandas
import polyline
import pytz
import requests

from exporter import __output_path__ as out_path
from exporter.gtfs.csvgtfs import Gtfs
from exporter.gtfs.dao import transactional, Dao
from exporter.gtfs.model import FeedInfo, CalendarDate, Calendar, Route, Stop, Shape, Trip, StopTime, ShapePoint, Agency
from exporter.util.http import Request, CsvDecoder
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import DataNormalizer

logger = logging.getLogger("gtfsexporter")
TIMEZONE = "Europe/Bucharest"


class FolderSource(object):
    def __init__(self, input_file, output_path):
        self.output_path = output_path
        if os.path.exists(input_file):
            with ZipFile(input_file, "r") as zip_ref:
                zip_ref.extractall(output_path)

        # change route type from 5 or 11 to 3 since other are not supported by opentripplanner
        r = pandas.read_csv(os.path.join(output_path, "routes.txt"))
        r.loc[r.route_type.isin([5, 11]), 'route_type'] = 3
        r.to_csv(os.path.join(output_path, "routes.txt"), index=False, sep=',')

    def open(self, filename, mode='rU'):
        f = os.path.join(self.output_path, filename)
        if os.path.exists(f):
            return open(f, mode + "b")

        raise KeyError(filename)

    def close(self):
        pass


class DataProvider(object):
    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        self._feed_id = feed_id
        self._lenient = lenient
        self._disable_normalization = disable_normalization

    def load_data_source(self, dao: Dao) -> bool:
        """Load in the file for extracting text."""
        return True

    @property
    def feed_id(self):
        return self._feed_id

    @property
    def lenient(self):
        return self._lenient

    @property
    def disable_normalization(self):
        return self._disable_normalization

    def is_from_api(self) -> bool:
        return False


class ApiDataProvider(DataProvider):
    def is_from_api(self) -> bool:
        return True


class FileDataProvider(DataProvider):
    def __init__(self, path: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization, **kwargs)
        self._path = path
        self._folder_source = FolderSource(self.path, output_path=out_path)

    def load_data_source(self, dao: Dao) -> bool:
        @transactional(dao.session)
        def _do_load_gtfs():
            with Gtfs(self.folder_source).load() as gtfs:
                from exporter.gtfs.converter import _convert_gtfs_model
                _convert_gtfs_model(self.feed_id, gtfs, dao, self.lenient, self.disable_normalization)

        _do_load_gtfs()
        return super().load_data_source(dao)

    @property
    def path(self):
        return self._path

    @property
    def folder_source(self):
        return self._folder_source


class HttpDataProvider(FileDataProvider):
    def __init__(self, url: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(self.__load_data(url), feed_id, lenient, disable_normalization, **kwargs)
        self._url = url

    def __load_data(self, url: str):
        import tempfile
        tmp = tempfile.NamedTemporaryFile()
        response = requests.get(url)

        # save the new one
        with open(tmp.name + ".zip", 'wb') as r:
            r.write(response.content)

        return tmp.name + ".zip"

    @property
    def url(self):
        return self._url


class RadcomApiDataProvider(ApiDataProvider):
    def __init__(self, url: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info
        self.feedinfo = FeedInfo(self.feed_id)

        self.line_request = Request(url + "/lines/")
        self.line_detail_request = Request(url + "/lines/{0}/direction/{1}")
        self.line_stops_request = Request(url + "/lines/{0}/stops/{1}")

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

    def _safe_bulk_insert(self, bulk):
        """
        performs a safe bulk insert, that updates existing items
        or creates a new record if not found
        """
        with self.dao.session.begin_nested():
            try:
                for record in bulk:
                    self._safe_insert(record)

                self.dao.flush()

            except Exception as e:
                logger.error(f"An exception was meet in bulk insert:{e}")
                self.dao.session.rollback()

    def _safe_insert(self, record):
        """
        performs a safe insert, that updates existing items
        or creates a new record if not found
        """
        self.dao.session.merge(record)

    def _clear_trips(self):
        """
        drops all the trips from the databse with the service id
        equal to the one for the current execution (LV or SD)
        """
        self.dao.session.query(Trip).filter(Trip.service_id == self.service_id).delete(synchronize_session=False)
        self.dao.session.commit()
        logger.info(f"Successfully droped trips with service id: {self.service_id}")


class BucharestApiDataProvider(RadcomApiDataProvider):
    # base providers url
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
        self._safe_insert(stb)
        self.agency_ids.add(stb.agency_id)

        self._safe_insert(metrorex)
        self.agency_ids.add(metrorex.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 2)


class ConstantaApiDataProvider(RadcomApiDataProvider):
    # base providers url
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

        self._safe_insert(stb)
        self.agency_ids.add(stb.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 1)


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


class BrasovApiDataProvider(ApiDataProvider):
    ROUTE_LIST_URL = "https://ratbv-scraper.herokuapp.com/allroutes"
    STOP_LIST_URL = "https://ratbv-scraper.herokuapp.com/getStations"
    ROUTE_STOP_LIST_URL = "https://ratbv-scraper.herokuapp.com/schedule?route={}"
    DEFAULT_LATITUDE = 45.669_646_7
    DEFAULT_LONGITUDE = 25.634_601_6

    # TODO: Grab route types from official website
    # https://ratbv.ro/trasee-si-orare/
    TROLLEY_ROUTES = {"Linia 3", "Linia 7", "Linia 8", "Linia 10", "Linia 33"}

    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization, **kwargs)
        self.feedinfo = FeedInfo(self.feed_id)
        self.dao = None
        self.stop_map = {}
        self.routes = []
        self.agency_id = None

    @measure_execution_time
    def load_data_source(self, dao: Dao) -> bool:
        self.dao = dao
        self._load_agencies()
        self._load_service()
        self._load_routes()
        self._load_schedule()

        dn = DataNormalizer(dao, self.feed_id)
        dn.normalize()
        dao.commit()
        return super().load_data_source(dao)

    def _load_agencies(self):
        logger.info("Importing agencies")
        self.agency_id = 6
        agency = Agency(
            feed_id=self.feed_id,
            agency_id=self.agency_id,
            agency_name="Regia Autonomă de Transport Brașov",
            agency_url="https://www.ratbv.ro/",
            agency_timezone=TIMEZONE,
            agency_lang="ro",
            agency_email="comunicare@ratbv.ro",
            agency_fare_url="https://ratbv.ro/tarife-trasee-urbane/",
            agency_phone="0368-800-600",
        )

        self.dao.add(agency)
        self.dao.flush()
        self.dao.commit()
        logger.info("Imported 1 agencies")

    def _load_service(self):
        logger.info("Importing service records")
        today = datetime.datetime.today()

        self.service_lv_id = "luniVineri"
        service, dates = self.make_dow_service(
            self.feed_id, self.service_lv_id, today, [1, 1, 1, 1, 1, 0, 0]
        )
        self.dao.add(service)
        self.dao.bulk_save_objects(dates)

        self.service_sd_id = "sambataDuminica"
        service, dates = self.make_dow_service(
            self.feed_id, self.service_sd_id, today, [0, 0, 0, 0, 0, 1, 1]
        )
        self.dao.add(service)
        self.dao.bulk_save_objects(dates)

        logger.info("Imported 2 service records")

    def _load_routes(self):
        logger.debug("Fetching routes")
        route_data = self._fetch_data(BrasovApiDataProvider.ROUTE_LIST_URL, "route list") or {}

        from exporter.static.brasov_data import COLOR_MAP, DEFAULT_COLORS

        for route_key, route_info in route_data.items():
            route_description = route_info.get("descriere")
            if "suspend" in route_key.lower():
                logger.error(f"Skipping route {route_key}")
                continue
            route = Route(
                feed_id=self.feed_id,
                route_id=self.sanitize(route_key),
                agency_id=self.agency_id,
                route_type=self._get_route_type(route_key),
                route_short_name=route_key,
                route_long_name=route_description,
                **{**COLOR_MAP.get(route_key, DEFAULT_COLORS)},
            )
            self.dao.add(route)
            self.routes.append({"key": route_key, "description": route_description})

        logger.debug(f"Fetched {len(route_data)} routes.")

    def _load_schedule(self):
        logger.debug("Fetching schedule")
        for route_data in self.routes:
            self._load_route_stops(route_data)
        logger.debug("Fetched schedule")

    def _load_route_stops(self, route_data):
        route_key = route_data["key"]
        logger.debug("Fetching stops for route {route_key}")

        stop_data = (
                self._fetch_data(BrasovApiDataProvider.ROUTE_STOP_LIST_URL, "route stop list", route_key) or {}
        )
        if len(stop_data) == 0:
            logger.warning(f"Expected stop data for {route_key}, received: {stop_data}")
        elif len(stop_data) != 1:
            logger.warning(
                f"Expected stop data for {route_key}, received: {stop_data.leys()}"
            )

        for route_key, direction_data in stop_data.items():
            route_id = self.sanitize(route_key)
            for direction_key, direction_stop_data in direction_data.items():
                self._load_trips(route_id, direction_key, direction_stop_data)

        logger.debug(f"Fetched {len(stop_data)} stops for route {route_key}.")

    def _load_trips(self, route_id, direction_key, direction_stop_data):
        today = self.midnight_today(TIMEZONE)
        stop_list = list(direction_stop_data.keys())
        service_trips = {}
        stop_sequence = 0

        # TODO: compute distance traveled based on stop gps positions
        distance_traveled = 1
        from exporter.static.brasov_data import STOP_MAP
        for stop_label, schedule_data in direction_stop_data.items():
            stop_id = self._make_stop(stop_label, **STOP_MAP.get(stop_label, {}))
            for service_key, hour_data in schedule_data.items():
                trips = []
                times = self.flatten_times(today, hour_data)
                if service_key in service_trips:
                    trips = service_trips[service_key]
                else:
                    service_trips[service_key] = trips
                    trip_id_prefix = "_".join(
                        [str(self.agency_id), route_id, direction_key, service_key]
                    )
                    for idx, time in enumerate(times):
                        trip_id = self.sanitize(f"{trip_id_prefix}_{idx}")
                        trip = Trip(
                            feed_id=self.feed_id,
                            trip_id=trip_id,
                            route_id=route_id,
                            service_id=service_key,
                        )
                        trips.append(trip)
                        self.dao.add(trip)

                for trip, time in zip(trips, times):
                    total_seconds_from_midnight = (time - today).total_seconds()
                    stop_time = StopTime(
                        feed_id=self.feed_id,
                        trip_id=trip.trip_id,
                        stop_id=stop_id,
                        stop_sequence=stop_sequence,
                        arrival_time=int(total_seconds_from_midnight),
                        departure_time=int(total_seconds_from_midnight),
                        shape_dist_traveled=distance_traveled,
                        timepoint=1,
                    )
                    trip.stop_times.append(stop_time)
            stop_sequence += 1

        for service_key, trips in service_trips.items():
            for trip in trips:
                self.dao.add(trip)

    def _load_stops(self):
        logger.debug("Fetching stops")
        stop_data = self._fetch_data(BrasovApiDataProvider.STOP_LIST_URL, "stop list") or []
        from exporter.static.brasov_data import STOP_MAP
        for stop_label in stop_data:
            self._make_stop(stop_label, **STOP_MAP.get(stop_label, {}))

        logger.debug(f"Fetched {len(stop_data)} stops.")

    def _make_stop(self, stop_label, **kwargs):
        stop_id = self.sanitize(stop_label)
        if stop_id not in self.stop_map:
            if "latitude" not in kwargs or "longitude" not in kwargs:
                logger.error(f"Mising GPS position for stop: {stop_label}")
            lat = kwargs.get("latitude", BrasovApiDataProvider.DEFAULT_LATITUDE)
            lng = kwargs.get("longitude", BrasovApiDataProvider.DEFAULT_LONGITUDE)
            self.dao.add(Stop(self.feed_id, stop_id, stop_label, lat, lng))
            self.stop_map[stop_id] = {"id": stop_id, "label": stop_label}

        elif stop_label != self.stop_map[stop_id]["label"]:
            existing_label = self.stop_map[stop_id]["label"]
            logger.error(
                f"Stop label consistency issue: {stop_label} != {existing_label}"
            )

        return stop_id

    def _fetch_data(self, url: str, entity: str, *args):
        data_request = Request(url)
        data_response = data_request(*args)
        error_status = data_response.get("status", {}).get("err")
        if error_status is not None and error_status is not False:
            logger.error(
                f"Failed to fetch {entity} from {url}, "
                f"received error response: {data_response}"
            )
        return data_response.get("data")

    def _get_route_type(self, route_key):
        if route_key in BrasovApiDataProvider.TROLLEY_ROUTES:
            return Route.TYPE_CABLECAR
        return Route.TYPE_BUS

    @staticmethod
    def make_dow_service(feed_id: str, service_id: str, today, dow: list = []):
        dates = []
        service = Calendar(feed_id, service_id)

        start_date = CalendarDate.fromYYYYMMDD(today.strftime("%Y%m%d"))
        end_date = CalendarDate.fromYYYYMMDD(
            datetime.date(today.year, 12, 31).strftime("%Y%m%d")
        )
        for d in CalendarDate.range(start_date, end_date.next_day()):
            if dow[d.dow()] == 1:
                d.feed_id = feed_id
                d.service_id = service.service_id
                dates.append(d)
        return service, dates

    @staticmethod
    def flatten_times(today, hour_data) -> list:
        result = []
        last_time = today
        for hour, minutes in hour_data.items():
            for minute in minutes:
                try:
                    if minute.endswith("*"):
                        logger.debug(
                            f"Dropping star(*) suffix from time: `{hour}:{minute}`"
                        )
                    int_hour = int(hour)
                    int_minute = int(minute.strip("*"))
                    last_time = today + datetime.timedelta(
                        hours=int_hour, minutes=int_minute
                    )
                except ValueError:
                    logger.error(f"Failed to parse time: `{hour}:{minute}`")

                result.append(last_time)
        return result

    @staticmethod
    def midnight_today(timezone) -> datetime.datetime:
        tz = pytz.timezone(timezone)
        naive_midnight = dateutil.parser.isoparse(datetime.date.today().isoformat())
        return tz.localize(naive_midnight)

    @staticmethod
    def sanitize(value):
        value = str(value)
        value = (
            unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        )
        value = re.sub(r"[^\w\s-]", "", value).strip()
        return re.sub(r"[-\s]+", "-", value)



# https://www.transporturban.ro/api/lines-get.php?router=oradea
# https://www.transporturban.ro/api/lines-trips-get.php?router=oradea&line=xxx
class TransportUrbanProvider(ApiDataProvider):
    def __init__(self):
        pass

class ApiProviderBuilder:
    def __init__(
            self,
            provider: str,
            feed_id="",
            lenient=False,
            disable_normalization=False,
            **kwargs
    ):
        self.provider = provider
        self.feed_id = feed_id
        self.lenient = lenient
        self.disable_normalization = disable_normalization
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def build(self) -> ApiDataProvider:
        switcher = {
            "bucharest": BucharestApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "constanta": ConstantaApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "cluj": ClujApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
            "brasov": BrasovApiDataProvider(
                self.feed_id, self.lenient, self.disable_normalization
            ),
        }

        return switcher.get(self.provider)
