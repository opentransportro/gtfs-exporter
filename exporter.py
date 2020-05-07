"""gtfs-exporter - GTFS to GTFS' conversion tool and database loader
Usage:
  gtfs-exporter <database> (--provider=<provider> | --delete | --list ) [--url=<url>] [--file=<file>] [--id=<id>]
                        [--logsql] [--lenient] [--schema=<schema>]
                        [--disablenormalize]
  gtfs-exporter (-h | --help)
  gtfs-exporter --version
Options:
  <database>           The database to use. If a file, assume SQLite.
                       For PostgreSQL: "postgresql://user:pwd@host:port/db".
  --provider=<provider> The provider type. Can be file, url or api.
  --url=<url>
  --file=<file>
  --delete             Delete feed.
  --list               List all feeds.
  --id=<id>            Set the feed ID in case multiple GTFS are to be loaded.
  -h --help            Show help on options.
  --version            Show lib / program version.
  --logsql             Enable SQL logging (very verbose)
  --lenient            Allow some level of brokenness in GTFS input.
  --schema=<schema>    Set the schema to use (for PostgreSQL).
  --disablenormalize   Disable shape and stop times normalization. Be careful
                       if you use this option, as missing stop times will not
                       be interpolated, and shape_dist_traveled will not be
                       computed or converted to meters.
Examples:
  gtfs-exporter db.sqlite --load=sncf.zip --id=sncf
        Load the GTFS sncf.zip into db.sqlite using id "sncf",
        deleting previous data.
  gtfs-exporter db.sqlite --delete --id=moontransit
        Delete the "moontransit" feed from the database.
  gtfs-exporter db.sqlite --list
        List all feed IDs from db.sqlite
  gtfs-exporter postgresql://gtfs@localhost/gtfs --load gtfs.zip
        Load gtfs.zip into a postgresql database,
        using a default (empty) feed ID.
Authors:
"""
import os
import subprocess

from docopt import docopt
from logging import StreamHandler, FileHandler
import logging
import sys
import shutil
from gtfslib.dao import Dao
from gtfslib.model import Route
from exporter.api.Builder import ApiProviderBuilder
from exporter.GtfsWritter import GtfsWritter, WritterContext
from exporter.Providers import DataProvider, FileDataProvider, HttpDataProvider
from exporter import __version__ as version, __temp_path__ as tmp_path, __output_path__ as out_path

class Exporter:
    def __init__(self, arguments, provider: DataProvider):
        self.provider = provider
        self.arguments = arguments

        if arguments['--id'] is None:
            arguments['--id'] = ""

        logging.basicConfig(format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s')
        self.logger = logging.getLogger('grfsexporter')
        self.logger.addHandler(StreamHandler(sys.stderr))
        self.logger.addHandler(FileHandler("export.log"))

        database = arguments['<database>']
        if os.path.exists(database):
            os.remove(database)

        self.dao = Dao(database, sql_logging=arguments['--logsql'], schema=arguments['--schema'])

        if arguments['--list']:
            for feed in self.dao.feeds():
                print(feed.feed_id if feed.feed_id != "" else "(default)")

        if arguments['--delete'] or arguments['--load']:
            feed_id = arguments['--id']
            existing_feed = self.dao.feed(feed_id)
            if existing_feed:
                logger.warning("Deleting existing feed ID '%s'" % feed_id)
                self.dao.delete_feed(feed_id)
                self.dao.commit()

    def generate_shapes(self):
        self.logger.info("searching for pfaedle support for generating shapes")
        if which('pfaedle') is None:
            self.logger.error("no support for generating shapes, pfaedle not found. Please clone from "
                              "https://github.com/opentransportro/pfaedle")
            pass
            # need to clone and build repo since this tool is needed for generating shapes

        # download maps
        self.logger.info("downloading maps required")
        if not os.path.exists(tmp_path + "map.osm"):
            filename = "map.osm.bz2"
            if not os.path.exists("map.osm.bz2"):
                self.logger.info("downloading from https://download.geofabrik.de/europe/romania-latest.osm.bz2")
                import requests
                file = requests.get("https://download.geofabrik.de/europe/romania-latest.osm.bz2", stream=True)

                with open("map.osm.bz2", "wb") as exported_file:
                    total_length = int(file.headers.get('content-length'))
                    from clint.textui import progress
                    for ch in progress.bar(file.iter_content(chunk_size=2391975),
                                           expected_size=(total_length / 1024) + 1):
                        if ch:
                            exported_file.write(ch)

            self.logger.info("expanding map file")

            import bz2
            with open(tmp_path + "map.osm", 'wb') as output:
                with bz2.BZ2File(filename, 'rb') as input:
                    shutil.copyfileobj(input, output)

        # removing not valid shape references
        import pandas as pd
        pd.read_csv(tmp_path + "trips.txt").set_index('shape_id').to_csv(tmp_path + "trips.txt", index=None)

        self.logger.info("generating shapes")
        subprocess.check_call(
            ['pfaedle', '-D', '--inplace', '-ddebug-out', '-o' + out_path, '--write-trgraph', '-mall',
             '-x' + tmp_path + 'map.osm', tmp_path])

    def process_gtfs(self):
        logging.info("Importing data from provided source")
        self.provider.load_data_source(self.dao)

        for route in self.dao.routes():
            print("updating route [%s] setting correct color" % (route.route_long_name))

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

        logging.info("Processing data from provided source")

        # self.processor.process(ruleset)
        class Args:
            filter = None

        writer = GtfsWritter(WritterContext(self.dao, Args()), bundle="feed-new.zip")
        writer.run()


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def main():
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)

    arguments = docopt(__doc__, version='gtfs-exporter %s' % version)

    # db.sqlite --provider=file --file=sncf.zip --id=sncf
    privider_type = arguments['--provider']
    provider = DataProvider()
    if privider_type == "file":
        provider = FileDataProvider(arguments['--file'],
                                    feed_id=arguments['--id'],
                                    lenient=arguments['--lenient'],
                                    disable_normalization=arguments['--disablenormalize'])
    elif privider_type == "url":
        provider = HttpDataProvider(arguments['--url'],
                                    feed_id=arguments['--id'],
                                    lenient=arguments['--lenient'],
                                    disable_normalization=arguments['--disablenormalize'])
    elif privider_type == "api":
        builder = ApiProviderBuilder(arguments['--url'],
                                     feed_id=arguments['--id'],
                                     lenient=arguments['--lenient'],
                                     disable_normalization=arguments['--disablenormalize'])
        provider = builder.build()

    instance = Exporter(arguments, provider)
    instance.generate_shapes()
    instance.process_gtfs()


if __name__ == '__main__':
    main()
