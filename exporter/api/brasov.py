import logging

from exporter.provider import ApiDataProvider
from exporter.util.perf import measure_execution_time
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


class BrasovApiDataProvider(ApiDataProvider):
    def __init__(
        self, feed_id="", lenient=False, disable_normalization=False, **kwargs
    ):
        super().__init__(feed_id, lenient, disable_normalization, **kwargs)
        self.feedinfo = FeedInfo(self.feed_id)

    @measure_execution_time
    def load_data_source(self, dao: Dao) -> bool:
        # TODO: populate stuff here

        dn = DataNormalizer(dao, self.feed_id)
        dn.normalize()
        dao.commit()
        return super().load_data_source(dao)

    def _load_agencies(self):
        logger.info("Importing agencies")
        logger.info("Imported 1 agencies")
        pass
