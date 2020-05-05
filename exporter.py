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

from docopt import docopt
from logging import StreamHandler
import logging
import sys
from gtfslib.dao import Dao
from gtfslib.model import Route
from sqlalchemy import update
from exporter.Providers import DataProvider, FileDataProvider, HttpDataProvider
from exporter.api.Builder import ApiProviderBuilder
import exporter


class Exporter:
    def __init__(self, arguments, provider: DataProvider):
        self.provider = provider
        self.arguments = arguments

        if arguments['--id'] is None:
            arguments['--id'] = ""

        logger = logging.getLogger('gtfs-exporter')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(StreamHandler(sys.stdout))

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
                self.logger.warning("Deleting existing feed ID '%s'" % feed_id)
                self.dao.delete_feed(feed_id)
                self.dao.commit()

    def export(self):
        logging.info("Importing data from provided source")
        self.provider.load_data_source(self.dao)
        update(Route).where(Route.route_type == Route.TYPE_BUS).values(route_color='user #5')

        for route in self.dao.routes(fltr=Route.route_type == Route.TYPE_BUS):
            print("%s: %d trips" % (route.route_long_name, len(route.trips)))
            route.route_color = "abcabc"
        self.dao.session().commit()

        logging.info("Processing data from provided source")

        # self.processor.process(ruleset)


def main():
    arguments = docopt(__doc__, version='gtfs-exporter %s' % exporter.__version__)

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
    instance.export()


if __name__ == '__main__':
    main()
