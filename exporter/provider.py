import os
from zipfile import ZipFile

import pandas as pd
import requests
from exporter.gtfs.csvgtfs import Gtfs
from exporter.gtfs.dao import Dao, transactional

import exporter


class FolderSource(object):
    def __init__(self, input_file, output_path):
        self.output_path = output_path
        if os.path.exists(input_file):
            with ZipFile(input_file, "r") as zip_ref:
                zip_ref.extractall(output_path)

        # change route type from 5 or 11 to 3 since other are not supported by opentripplanner
        r = pd.read_csv(os.path.join(output_path, "routes.txt"))
        r.loc[r.route_type.isin([5, 11]), 'route_type'] = 3
        r.to_csv(os.path.join(output_path, "routes.txt"), index=False, sep=',')

    def open(self, filename, mode='rU'):
        f = os.path.join(self.output_path, filename)
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


class FileDataProvider(DataProvider):
    def __init__(self, path: str, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__(feed_id, lenient, disable_normalization, **kwargs)
        self._path = path
        self._folder_source = FolderSource(self.path, output_path=exporter.__output_path__)

    def load_data_source(self, dao: Dao) -> bool:
        @transactional(dao.session())
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


class ApiDataProvider(DataProvider):
    def is_from_api(self) -> bool:
        return True