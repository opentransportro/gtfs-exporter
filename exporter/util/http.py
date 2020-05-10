import logging
import time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from exporter.util.perf import measure_execution_time


class Request(object):
    def __init__(self, url: str, logger = None):
        self._url = url
        self.encoding = 'utf-8'
        if logger is None:
            self.logger = logging.getLogger("gtfsexporter")
        else:
            self.logger = logger

        retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[400, 500, 502, 503, 504 ])

        self.request_shared_session = requests.Session()
        self.request_shared_session.mount(url, HTTPAdapter(max_retries=retries))

    @property
    def url(self):
        return self._url

    # This construct allows objects to be called as functions in python
    @measure_execution_time
    def __call__(self, *args):
        request_url = self._url.format(*args)

        ts = time.time()
        response = self.request_shared_session.get(request_url, headers={'Content-Type': 'application/json'})
        te = time.time()
        self.logger.debug('%r took %2.2f ms' % (request_url, (te - ts) * 1000))

        return response.json()
