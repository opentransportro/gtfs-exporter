import logging

import requests

from exporter.util.perf import measure_execution_time

logger = logging.getLogger("gtfsexporter")

shared_session = requests.Session()


class Request(object):
    def __init__(self, url):
        self._url = url
        self.encoding = 'utf-8'

    @property
    def url(self):
        return self._url

    # This construct allows objects to be called as functions in python
    @measure_execution_time
    def __call__(self, *args):
        request_url = self.url.format(*args)

        logger.debug(f"requesting data from ${request_url}")
        # ts = time.time()
        response = shared_session.get(request_url, headers={'Content-Type': 'application/json'})
        # te = time.time()
        # logger.info('%r took %2.2f ms' % (request_url, (te - ts) * 1000))

        return response.json()
