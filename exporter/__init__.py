import os
import shutil
import logging
import threading
import subprocess
import time, os, stat

from gtfslib.dao import Dao
from gtfslib.model import Route

from exporter.provider import DataProvider
from exporter.writer import Writer, Context

__version__ = "1.0.0"
__cwd_path__ = os.path.abspath(os.getcwd())
__temp_path__ = os.path.join(__cwd_path__, "tmp")
__map_path__ = os.path.join(__cwd_path__, "map")
__output_path__ = os.path.join(__cwd_path__, "out")


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


def file_age_in_seconds(pathname):
    return int(time.time() - os.stat(pathname)[stat.ST_MTIME])


def run_command(args: [], logger=None) -> bool:
    logpipe = LogPipe(logging.INFO, logger)
    # noinspection PyTypeChecker
    with subprocess.Popen(args, stdout=logpipe, stderr=logpipe) as s:
        s.wait()
        logpipe.close()
        logpipe.join()

    return True


def remove_column(file: str, column: str):
    import pandas as pd
    try:
        pd.read_csv(file).set_index(column).to_csv(file, index=None)
    except:
        pass


class Exporter:
    def __init__(self, arguments, provider: DataProvider):
        self.provider = provider
        self.arguments = arguments
        self.logger = logging.getLogger('grfsexporter')

        if arguments['--id'] is None:
            arguments['--id'] = ""

        database_path = os.path.join(__cwd_path__, self.provider.feed_id + ".sqlite")
        if os.path.exists(database_path):
            os.remove(database_path)

        self.dao = Dao(database_path, sql_logging=arguments['--logsql'], schema=arguments['--schema'])

        if arguments['--list']:
            for feed in self.dao.feeds():
                print(feed.feed_id if feed.feed_id != "" else "(default)")

        if arguments['--delete']:
            feed_id = arguments['--id']
            existing_feed = self.dao.feed(feed_id)
            if existing_feed:
                self.logger.warning("Deleting existing feed ID '%s'" % feed_id)
                self.dao.delete_feed(feed_id)
                self.dao.commit()

    def generate_shapes(self):
        self.logger.info("searching for pfaedle support for generating shapes")
        if shutil.which('pfaedle') is None:
            self.logger.error("no support for generating shapes, pfaedle not found. Please clone from "
                              "https://github.com/opentransportro/pfaedle")
            # need to clone and build repo since this tool is needed for generating shapes
            return

        # download maps
        self.logger.info("downloading maps required")
        map_file = os.path.join(__map_path__, "map.osm")
        map_archive = os.path.join(__map_path__, "map.osm.bz2")

        if not os.path.exists(map_file) or file_age_in_seconds(map_file) > 604800:
            if file_age_in_seconds(map_file) > 604800 and os.path.exists(map_file):
                self.logger.warning("Map file to old removing and fetching new one")
                os.remove(map_file)
            else:
                self.logger.info("Map file is okey, using the cached one")

            if not os.path.exists(map_archive) or file_age_in_seconds(map_file) > 604800:
                self.logger.info("downloading from https://download.geofabrik.de/europe/romania-latest.osm.bz2")
                import requests
                file = requests.get("https://download.geofabrik.de/europe/romania-latest.osm.bz2", stream=True)

                with open(map_archive, "wb") as exported_file:
                    total_length = int(file.headers.get('content-length'))
                    from clint.textui import progress
                    for ch in progress.bar(file.iter_content(chunk_size=2391975),
                                           expected_size=(total_length / 1024) + 1):
                        if ch:
                            exported_file.write(ch)

            self.logger.info("expanding map file")

            import bz2
            with open(map_file, 'wb') as output:
                with bz2.BZ2File(map_archive, 'rb') as input:
                    shutil.copyfileobj(input, output)

            # cleanup the archive as we dont use it
            os.remove(map_archive)

        # removing not valid shape references
        remove_column(os.path.join(__temp_path__, "trips.txt"), "shape_id")

        self.logger.info("generating shapes")
        run_command(
            ['pfaedle', '-D', '--inplace', '-dtmp', '-o' + __temp_path__, '--write-trgraph', '--write-graph',
             '--write-cgraph', '-mall',
             '-x' + map_file, __temp_path__], self.logger)

    def process_gtfs(self):
        self.logger.info("Importing data from provided source")
        self.provider.load_data_source(self.dao)

        for route in self.dao.routes():
            print("updating route [%s] setting correct color" % route.route_long_name)

            route.route_text_color = "FFFFFF"

            if route.route_type == Route.TYPE_BUS:
                route.route_color = "195BAD"
            elif route.route_type == Route.TYPE_TRAM:
                route.route_color = "FFAD33"
            elif route.route_type == Route.TYPE_RAIL:
                route.route_color = "FF5B33"
            elif route.route_type == Route.TYPE_CABLECAR:
                route.route_color = "FF8433"
            elif route.route_type == Route.TYPE_SUBWAY:
                route.route_color = "D13333"
            elif route.route_type == Route.TYPE_FERRY:
                route.route_color = "62A9DD"

        self.dao.session().commit()

        self.logger.info("Processing data from provided source")

        # Here we should use a rule processor to have more flexibility when processing data
        # self.processor.process(ruleset)
        class Args:
            filter = None

        self.logger.info(f"Generating archive with name gtfs-{self.provider.feed_id}.zip")
        w = Writer(Context(self.dao, Args()), bundle=f"gtfs-{self.provider.feed_id}.zip")
        w.run()
