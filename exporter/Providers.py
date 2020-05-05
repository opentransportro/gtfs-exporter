import requests
import os
import logging
from gtfslib.dao import Dao, transactional
from gtfslib.csvgtfs import Gtfs, ZipFileSource


class DataProvider:
    def __init__(self):
        pass

    def load_data_source(self, dao: Dao) -> bool:
        """Load in the file for extracting text."""
        pass


class FileDataProvider(DataProvider):
    def __init__(self, path: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__()
        self.path = path
        self.feed_id = feed_id
        self.lenient = lenient
        self.disable_normalization = disable_normalization

    def load_data_source(self, dao: Dao) -> bool:
        @transactional(dao.session())
        def _do_load_gtfs():
            with Gtfs(ZipFileSource(self.path)).load() as gtfs:
                from gtfslib.converter import _convert_gtfs_model
                _convert_gtfs_model(self.feed_id, gtfs, dao, self.lenient, self.disable_normalization)

        _do_load_gtfs()
        return super().load_data_source(dao)


class HttpDataProvider(FileDataProvider):
    def __init__(self, url: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__("feed.zip", feed_id, lenient, disable_normalization, **kwargs)
        self.url = url

    def load_data_source(self, dao: Dao) -> bool:
        # logging.info("importing data from url {} for feed id {}".format(url, feed_id))
        response = requests.get(self.url)
        # remove existing file
        if os.path.exists(self.path):
            os.remove(self.path)
        # save the new one
        with open(self.path, 'wb') as r:
            r.write(response.content)
        return super().load_data_source(dao)


class ApiDataProvider(DataProvider):
    pass
