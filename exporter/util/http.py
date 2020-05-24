import logging
import time

import requests
from ratelimit import limits, sleep_and_retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import csv


class RequestDecoder(object):
    def decode(self, response):
        """Decode the response and return the content"""
        pass


class JsonDecoder(RequestDecoder):
    def decode(self, response):
        return response.json()


class CsvDecoder(RequestDecoder):
    def decode(self, response):
        if response.status_code == 200:
            decoded_content = response.content.decode('utf-8')
            timetable_cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            return list(timetable_cr)
        else:
            return []


class Request(object):
    def __init__(self, url: str, decoder=JsonDecoder(), headers=None, logger=None):
        if headers is None:
            headers = {}
        self._url = url
        self.decoder = decoder
        self.headers = headers
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

        return self.decoder.decode(response=response)

    @sleep_and_retry
    @limits(calls=20, period=1)
    def __safe_request(self, request_url):
        try:
            response = self.request_shared_session.get(request_url, headers=self.headers)
        except:
            response = self.__safe_request(request_url=request_url)

        return response
