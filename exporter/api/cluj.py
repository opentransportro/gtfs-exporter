import logging
import time
import polyline
from gtfslib.dao import Dao
from gtfslib.model import Agency, FeedInfo, Route, Trip, Stop, StopTime, Shape, ShapePoint, Calendar, CalendarDate
from exporter.provider import ApiDataProvider
from exporter.api.requests import RequestExecutor
from exporter.util.http import Request
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import DataNormalizer

logger = logging.getLogger("gtfsexporter")

SLEEP_TIME = 0


class ClujApiDataProvider(ApiDataProvider):
    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info
        self.feedinfo = FeedInfo(self.feed_id)
        self.request_executor = RequestExecutor()
        self.url = "https://m-go-cluj.wink.ro/apiPublic"

        self.line_detail_request = Request(self.url + "/route/byId/{0}")

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

        stb = Agency(self.feed_id, 1, "Compania de Transport Public Cluj", "http://www.ctpcj.ro",
                     "Europe/Bucharest", **{
                "agency_lang": "ro",
                "agency_email": "sugestii@ctpcj.ro",
                "agency_fare_url": "http://www.ctpcj.ro/index.php/ro/tarife/transport-urban",
                "agency_phone": "0264-430917"
            })

        self.dao.add(stb)
        self.agency_ids.add(stb.agency_id)

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

        save_calendar_for("LV", [1, 1, 1, 1, 1, 0, 0])
        save_calendar_for("S", [0, 0, 0, 0, 0, 1, 0])
        save_calendar_for("D", [0, 0, 0, 0, 0, 0, 1])

    def __load_routes(self):
        for line_id in range(150):
            stops = set()
            route_data = self.line_detail_request(str(line_id))
            if route_data['type']:
                print(route_data)
