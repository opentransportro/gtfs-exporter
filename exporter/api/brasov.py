import logging
import pytz
import re
import unicodedata

import datetime
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
from exporter.util.spatial import DataNormalizer
from .brasov_data import DEFAULT_COLORS, COLOR_MAP, STOP_LIST, STOP_MAP

logger = logging.getLogger("gtfsexporter.brasov")

ROUTE_LIST_URL = "https://ratbv-scraper.herokuapp.com/allroutes"
STOP_LIST_URL = "https://ratbv-scraper.herokuapp.com/getStations"
ROUTE_STOP_LIST_URL = "https://ratbv-scraper.herokuapp.com/schedule?route={}"

TIMEZONE = "Europe/Bucharest"
DEFAULT_LATITUDE = 45.669_646_7
DEFAULT_LONGITUDE = 25.634_601_6

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
                logger.error(f"Skipping route {route_key}")
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
            stop_id = self._make_stop(stop_label, **STOP_MAP.get(stop_label, {}))
            for service_key, hour_data in schedule_data.items():
                trips = []
                times = flatten_times(today, hour_data)
                if service_key in service_trips:
                    trips = service_trips[service_key]
                else:
                    service_trips[service_key] = trips
                    trip_id_prefix = "_".join(
                        [str(self.agency_id), route_id, direction_key, service_key]
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
        stop_data = self._fetch_data(STOP_LIST_URL, "stop list") or []
        for stop_label in stop_data:
            self._make_stop(stop_label, **STOP_MAP.get(stop_label, {}))

        logger.debug(f"Fetched {len(stop_data)} stops.")

    def _make_stop(self, stop_label, **kwargs):
        stop_id = sanitize(stop_label)
        if stop_id not in self.stop_map:
            if "latitude" not in kwargs or "longitude" not in kwargs:
                logger.error(f"Mising GPS position for stop: {stop_label}")
            lat = kwargs.get("latitude", DEFAULT_LATITUDE)
            lng = kwargs.get("longitude", DEFAULT_LONGITUDE)
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
    last_time = today
    for hour, minutes in hour_data.items():
        for minute in minutes:
            try:
                if minute.endswith("*"):
                    logger.debug(f"Dropping star(*) suffix from time: `{hour}:{minute}`")
                int_hour = int(hour)
                int_minute = int(minute.strip("*"))
                last_time = today + datetime.timedelta(
                    hours=int_hour, minutes=int_minute
                )
            except ValueError:
                logger.error(f"Failed to parse time: `{hour}:{minute}`")

            result.append(last_time)
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
