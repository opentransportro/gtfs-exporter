import logging
import os
import subprocess
import threading
import time


def measure_execution_time(method):
    logger = logging.getLogger("gtfsexporter")

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.debug('%r took %2.2f ms' % (method.__name__, (te - ts) * 1000))
            return result

    return timed


class LogPipe(threading.Thread):
    def __init__(self, level, logger=None):
        """Setup the object with a logger and a loglevel
        and start the thread
        """
        if logger is None:
            self.logger = logging.getLogger("gtfsexporter")
        else:
            self.logger = logger
        threading.Thread.__init__(self)
        self.daemon = False
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe
        """
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything.
        """
        for line in iter(self.pipeReader.readline, ''):
            self.logger.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """Close the write end of the pipe.
        """
        os.close(self.fdWrite)


def run_command(args: [], logger=None) -> int:
    logpipe = LogPipe(logging.INFO, logger)
    # noinspection PyTypeChecker
    _result = 0

    with subprocess.Popen(args, stdout=logpipe, stderr=logpipe) as s:
        _result = s.wait()
        logpipe.close()
        logpipe.join()

    return _result
