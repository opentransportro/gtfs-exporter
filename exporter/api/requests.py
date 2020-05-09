import queue

from concurrent.futures import ThreadPoolExecutor
import logging
import random
import time
import queue

import requests
import threading

NTHREADS = 2
DELAY_SECONDS = 0.5
URLS = ['https://google.com', 'http://yahoo.com', 'http://github.com', 'https://bing.com']

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# def callback():
#     response = requests.get(random.choice(URLS), timeout=120)
#     logging.info('status_code=%d ok=%s', response.status_code, response.ok)


#
# with ThreadPoolExecutor(NTHREADS) as executor:
#     while True:
#         time.sleep(DELAY_SECONDS)  # do not hit the site too hard
#         queued_works = executor._work_queue.qsize()
#         logging.info('queued works: %s', queued_works)
#         if queued_works < 10:  # do not flood executor's queue
#             executor.submit(callback)


class RequestExecutor(threading.Thread):
    class RequestWrapper:
        def __init__(self, url, callback, **kwargs):
            self.url = url
            self.callback = callback
            self.params = kwargs

    def __init__(self):
        super().__init__()
        self._should_stop = False
        self._thread_pool = ThreadPoolExecutor(NTHREADS)
        self._queue = queue.Queue()

    @property
    def should_stop(self):
        return self._should_stop

    @should_stop.setter
    def should_stop(self, new_val):
        self._should_stop = new_val

    def enqueue_request(self, url: str, callback, **kwargs):
        rw = RequestExecutor.RequestWrapper(url, callback, **kwargs)
        self._queue.put(rw)

    def run(self) -> None:
        while not self._should_stop:
            time.sleep(DELAY_SECONDS)  # do not hit the site too hard
            rw = self._queue.get(block=True)
            self._thread_pool.submit(rw.callback, **rw.params)
