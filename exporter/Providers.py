import requests
import json
import os
from gtfslib.dao import Dao, transactional
from gtfslib.csvgtfs import Gtfs, ZipFileSource
from exporter import Processor


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
        response = requests.get(url)
        # remove existing file
        if os.path.exists("feed.zip"):
            os.remove("feed.zip")
        # save the new one
        with open('feed.zip', 'wb') as r:
            r.write(response.content)

        super().__init__("feed.zip", feed_id, lenient, disable_normalization, **kwargs)


class ApiDataProvider(DataProvider):
    ""
