import requests
import logging
import time
from exporter.util.perf import measure_execution_time

logger = logging.getLogger("gtfsexpoter")


class Request(object):
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    # This construct allows objects to be called as functions in python
    @measure_execution_time
    def __call__(self, *args):
        request_url = self.url.format(*args)

        logger.debug(f"requesting data from ${request_url}")
        # ts = time.time()
        response = requests.get(request_url)
        # te = time.time()
        # logger.info('%r took %2.2f ms' % (request_url, (te - ts) * 1000))

        return response.json()
