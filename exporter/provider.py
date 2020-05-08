from zipfile import ZipFile

import requests
import os
import exporter
from gtfslib.dao import Dao, transactional
from gtfslib.csvgtfs import Gtfs


class FolderSource(object):
    def __init__(self, input_file):
        if os.path.exists(input_file):
            with ZipFile(input_file, "r") as zip_ref:
                zip_ref.extractall(exporter.__temp_path__)

    def open(self, filename, mode='rU'):
        f = os.path.join(exporter.__temp_path__, filename)
        if os.path.exists(f):
            return open(f, mode + "b")

        raise KeyError(filename)

    def close(self):
        pass


class DataProvider:
    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        self._feed_id = feed_id
        self._lenient = lenient
        self._disable_normalization = disable_normalization

    def load_data_source(self, dao: Dao) -> bool:
        """Load in the file for extracting text."""
        pass

    @property
    def feed_id(self):
        return self._feed_id

    @property
    def lenient(self):
        return self._lenient

    @property
    def disable_normalization(self):
        return self._disable_normalization


class FileDataProvider(DataProvider):
    def __init__(self, path: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization, **kwargs)
        self._path = path
        self._folder_source = FolderSource(self.path)

    def load_data_source(self, dao: Dao) -> bool:
        @transactional(dao.session())
        def _do_load_gtfs():
            with Gtfs(self.folder_source).load() as gtfs:
                from gtfslib.converter import _convert_gtfs_model
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


class ApiDataProvider(DataProvider):
    pass
