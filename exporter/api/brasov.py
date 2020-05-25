import logging
import pytz
import re
import unicodedata

import datetime as datetime

from exporter.provider import ApiDataProvider
from exporter.util.perf import measure_execution_time
from exporter.util.http import Request
from gtfslib.dao import Dao
from gtfslib.model import (
    Agency,
    FeedInfo,
    Calendar,
    CalendarDate,
    Route,
    Shape,
    ShapePoint,
    Stop,
    Trip,
    StopTime,
)

logger = logging.getLogger("gtfsexporter.brasov")

ROUTE_LIST_URL = "https://ratbv-scraper.herokuapp.com/allroutes"
STOP_LIST_URL = "https://ratbv-scraper.herokuapp.com/getStations"
ROUTE_STOP_LIST_URL = "https://ratbv-scraper.herokuapp.com/schedule?route={}"

DEBUG = False

TIMEZONE = "Europe/Bucharest"
DEFAULT_COLORS = {"route_color": "000000", "route_text_color": "FFFFFF"}
COLOR_MAP = {
    # TODO: Grab colors from official website (check out style.css)
    # https://ratbv.ro/trasee-si-orare/
    "Linia 1": {"route_color": "fcf81d", "route_text_color": "000000"},
    "Linia 2": {"route_color": "00bd47", "route_text_color": "000000"},
    "Linia 3": {"route_color": "a9aea8", "route_text_color": "000000"},
    "Linia 4": {"route_color": "6b99ba", "route_text_color": "000000"},
    "Linia 5": {"route_color": "f82b3c", "route_text_color": "000000"},
    "Linia 5M": {"route_color": "fd7306", "route_text_color": "000000"},
    "Linia 6": {"route_color": "01a98f", "route_text_color": "000000"},
    "Linia 7": {"route_color": "fd7306", "route_text_color": "000000"},
    "Linia 9": {"route_color": "efe44e", "route_text_color": "000000"},
    "Linia 8": {"route_color": "ecc1df", "route_text_color": "000000"},
    "Linia 10": {"route_color": "b31f37", "route_text_color": "000000"},
    "Linia 14": {"route_color": "4bba3a", "route_text_color": "000000"},
    "Linia 15": {"route_color": "030d91", "route_text_color": "000000"},
    "Linia 16": {"route_color": "f66e32", "route_text_color": "000000"},
    "Linia 17": {"route_color": "65eded", "route_text_color": "000000"},
    "Linia 17B": {"route_color": "fdf681", "route_text_color": "000000"},
    "Linia 18": {"route_color": "ed839a", "route_text_color": "000000"},
    "Linia 20 Expres": {"route_color": "b1f000", "route_text_color": "000000"},
    "Linia 21": {"route_color": "f66e32", "route_text_color": "000000"},
    "Linia 22": {"route_color": "006bc5", "route_text_color": "000000"},
    "Linia 23": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 23B": {"route_color": "db33a4", "route_text_color": "000000"},
    "Linia 24": {"route_color": "db33a4", "route_text_color": "000000"},
    "Linia 25": {"route_color": "a2e9bd", "route_text_color": "000000"},
    "Linia 28": {"route_color": "efe44e", "route_text_color": "000000"},
    "Linia 29": {"route_color": "f82b3c", "route_text_color": "000000"},
    "Linia 31": {"route_color": "f66e32", "route_text_color": "000000"},
    "Linia 32": {"route_color": "113bab", "route_text_color": "000000"},
    "Linia 33": {"route_color": "c4c4c4", "route_text_color": "000000"},
    "Linia 34": {"route_color": "9c9c9c", "route_text_color": "000000"},
    "Linia 34B": {"route_color": "ecc1df", "route_text_color": "000000"},
    "Linia 35": {"route_color": "af90a0", "route_text_color": "000000"},
    "Linia 36": {"route_color": "338185", "route_text_color": "000000"},
    "Linia 37": {"route_color": "6e3710", "route_text_color": "000000"},
    "Linia 40": {"route_color": "ff9d1c", "route_text_color": "000000"},
    "Linia 41": {"route_color": "56abc0", "route_text_color": "000000"},
    "Linia 50": {"route_color": "e30e78", "route_text_color": "000000"},
    "Linia 51": {"route_color": "beb53e", "route_text_color": "000000"},
    "Linia 52": {"route_color": "a1d7d7", "route_text_color": "000000"},
    "Linia 53": {"route_color": "f82b3c", "route_text_color": "000000"},
    "Linia 120": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 210": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 220": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 310": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 420": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 520": {"route_color": "2391d0", "route_text_color": "000000"},
    "Linia 540": {"route_color": "2391d0", "route_text_color": "000000"},
}

# TODO: Grab route types from official website
# https://ratbv.ro/trasee-si-orare/
TROLLEY_ROUTES = {"Linia 3", "Linia 7", "Linia 8", "Linia 10", "Linia 33"}


class BrasovApiDataProvider(ApiDataProvider):
    def __init__(
        self, feed_id="", lenient=False, disable_normalization=False, **kwargs
    ):
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
        service, dates = make_dow_service(
            self.feed_id, self.service_lv_id, today, [1, 1, 1, 1, 1, 0, 0]
        )
        self.dao.add(service)
        self.dao.bulk_save_objects(dates)

        self.service_sd_id = "sambataDuminica"
        service, dates = make_dow_service(
            self.feed_id, self.service_sd_id, today, [0, 0, 0, 0, 0, 1, 1]
        )
        self.dao.add(service)
        self.dao.bulk_save_objects(dates)

        logger.info("Imported 2 service records")

    def _load_routes(self):
        logger.debug("Fetching routes")
        route_data = self._fetch_data(ROUTE_LIST_URL, "route list") or {}

        for route_key, route_info in route_data.items():
            route_description = route_info.get("descriere")
            if "suspend" in route_key.lower():
                logger.error("Skipping route {route_key}")
                continue
            route = Route(
                feed_id=self.feed_id,
                route_id=sanitize(route_key),
                agency_id=self.agency_id,
                route_type=_get_route_type(route_key),
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
            if DEBUG:
                logger.error("Breaking cycle early to facilitate debugging")
                break
        logger.debug("Fetched schedule")

    def _load_route_stops(self, route_data):
        route_key = route_data["key"]
        logger.debug("Fetching stops for route {route_key}")

        stop_data = (
            self._fetch_data(ROUTE_STOP_LIST_URL, "route stop list", route_key) or {}
        )
        if len(stop_data) == 0:
            logger.warning(f"Expected stop data for {route_key}, received: {stop_data}")
        elif len(stop_data) != 1:
            logger.warning(
                f"Expected stop data for {route_key}, received: {stop_data.leys()}"
            )

        for route_key, direction_data in stop_data.items():
            route_id = sanitize(route_key)
            for direction_key, direction_stop_data in direction_data.items():
                self._load_trips(route_id, direction_key, direction_stop_data)

        logger.debug(f"Fetched {len(stop_data)} stops for route {route_key}.")

    def _load_trips(self, route_id, direction_key, direction_stop_data):
        today = midnight_today(TIMEZONE)
        stop_list = list(direction_stop_data.keys())
        service_trips = {}
        stop_sequence = 0

        # TODO: compute distance traveled based on stop gps positions
        distance_traveled = 1
        for stop_label, schedule_data in direction_stop_data.items():
            stop_id = self._make_stop(stop_label)
            for service_key, hour_data in schedule_data.items():
                trips = []
                times = flatten_times(today, hour_data)
                if service_key not in service_trips:
                    service_trips[service_key] = trips
                    trip_id_prefix = "_".join(
                        [self.agency_id, route_id, direction_key, service_key]
                    )
                    for idx, time in enumerate(times):
                        trip_id = sanitize(f"{trip_id_prefix}_{idx}")
                        trip = Trip(
                            feed_id=self.feed_id,
                            trip_id=trip_id,
                            route_id=route_id,
                            service_id=service_key,
                        )
                        trips.append(trip)
                        self.dao.add(trip)
                else:
                    trips = service_trips[service_key]

                for trip, time in zip(trips, times):
                    stop_time = StopTime(
                        feed_id=self.feed_id,
                        trip_id=trip.trip_id,
                        stop_id=stop_id,
                        stop_sequence=stop_sequence,
                        departure_time=time,
                        arrival_time=time,
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
        stop_data = self._fetch_data(STOP_LIST_URL, "stop list") or []
        for stop_label in stop_data:
            self._make_stop(stop_label)

        logger.debug(f"Fetched {len(stop_data)} stops.")

    def _make_stop(self, stop_label, **kwargs):
        stop_id = sanitize(stop_label)
        if stop_id not in self.stop_map:
            # TODO: find GPS coordinates for stops
            lat = kwargs.get("lat", 45.669_646_7)
            lng = kwargs.get("lng", 25.634_601_6)
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
        if error_status is not None or error_status is not False:
            logger.error("Received error response: {data_response}")
        return data_response.get("data")


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


def _get_route_type(route_key):
    if route_key in TROLLEY_ROUTES:
        return Route.TYPE_CABLECAR
    return Route.TYPE_BUS


def flatten_times(today, hour_data) -> list:
    result = []
    for hour, minutes in hour_data.items():
        result.extend(
            [today + datetime.timedelta(hour=hour, minute=minute) for minute in minutes]
        )
    return result


def midnight_today(timezone) -> datetime.datetime:
    tz = pytz.timezone(timezone)
    naive_midnight = datetime.datetime.fromisoformat(datetime.date.today().isoformat())
    return tz.localize(naive_midnight)


def sanitize(value):
    value = str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return re.sub(r"[-\s]+", "-", value)
