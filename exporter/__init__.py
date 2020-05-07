import os

__version__ = "1.0.0"
__app_path__ = os.path.dirname(os.path.abspath(__file__)) + "/../"
__temp_path__ = __app_path__ + "tmp/"
__output_path__ = __app_path__ + "out/"

import subprocess
import logging
import threading


class LogPipe(threading.Thread):
    def __init__(self, level, logger = None):
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


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        logging.info('got line from subprocess: %r', line)


def run_command(args: [], logger=None) -> bool:
    logpipe = LogPipe(logging.INFO, logger)
    # noinspection PyTypeChecker
    with subprocess.Popen(args, stdout=logpipe, stderr=logpipe) as s:
        s.wait()
        logpipe.close()

    return True


def remove_column(file: str, column: str):
    import pandas as pd
    try:
        pd.read_csv(file).set_index(column).to_csv(file, index=None)
    except:
        pass
