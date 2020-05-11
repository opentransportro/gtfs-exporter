import logging
import time

import requests
from ratelimit import limits, sleep_and_retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from exporter.util.perf import measure_execution_time


class Request(object):
    def __init__(self, url: str, logger=None):
        self._url = url
        self.encoding = 'utf-8'
        if logger is None:
            self.logger = logging.getLogger("gtfsexporter")
        else:
            self.logger = logger
        retries = Retry(total=10,
                        backoff_factor=0.1,
                        status_forcelist=[400, 404, 500, 502, 503, 504])

        self.request_shared_session = requests.Session()
        self.request_shared_session.mount(url, HTTPAdapter(max_retries=retries))

    @property
    def url(self):
        return self._url

    def __call__(self, *args):
        # api call rate limiting to 20 requests / 1 second => 1 request / 50 msec
        # --- average response time observed was ~35 msec
        request_url = self._url.format(*args)

        ts = time.time()
        response = self.__safe_request(request_url)
        te = time.time()
        self.logger.debug('%r took %2.2f ms' % (request_url, (te - ts) * 1000))

        return response.json()

    @sleep_and_retry
    @limits(calls=20, period=1)
    def __safe_request(self, request_url):
        try:
            response = self.request_shared_session.get(request_url, headers={'Content-Type': 'application/json'})
        except:
            response = self.__safe_request(request_url=request_url)

        return response
