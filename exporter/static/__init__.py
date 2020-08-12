"""gtfs-exporter - GTFS to GTFS' conversion tool and database loader
Usage:
  gtfs-exporter (--provider=<provider> | --delete | --list ) [--url=<url>] [--file=<file>] [--id=<id>]
                        [--logsql] [--lenient] [--schema=<schema>]
                        [--disablenormalize]
  gtfs-exporter (-h | --help)
  gtfs-exporter --version
Options:
  --provider=<provider> The provider type. Can be file, url or providers.
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
  gtfs-exporter --provider=url --url=https://api.opentransport.ro/gtfs/v1/static --id=timisoara
        Load GTFS from url using id "sncf", deleting previous data.
  gtfs-exporter --delete --id=moontransit
        Delete the "moontransit" feed from the database.
  gtfs-exporter --list
        List all feed IDs from database
Authors:
"""
import glob
import logging
import os

from docopt import docopt

from exporter import __version__ as version, __output_path__ as out_path, __cwd_path__ as cwd_path
from exporter.gtfs.dao import Dao
from exporter.gtfs.model import Route
from exporter.static.processor import Processor
from exporter.static.providers import ApiProviderBuilder
from exporter.static.providers import DataProvider, FileDataProvider, HttpDataProvider
from exporter.settings import GH_REPO, GH_TOKEN
from exporter.util.logging import init_logging
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import ShapeGenerator
from exporter.util.storage import init_filesystem
from exporter.vcs.github import ReleaseGenerator
from exporter.writer import Context, Writer


class StaticExporter:
    def __init__(self, arguments):
        self.logger = logging.getLogger('gtfsexporter')
        self._arguments = arguments

        if arguments['--id'] is None:
            arguments['--id'] = "default"

        database_path = os.path.join(cwd_path, arguments['--id'] + ".sqlite")

        self._dao = Dao(database_path, sql_logging=arguments['--logsql'], schema=arguments['--schema'])

        if arguments['--list']:
            for feed in self._dao.feeds():
                print(feed.feed_id if feed.feed_id != "" else "(default)")

        if arguments['--delete']:
            feed_id = arguments['--id']
            existing_feed = self._dao.feed(feed_id)
            if existing_feed:
                self.logger.warning("Deleting existing feed ID '%s'" % feed_id)
                self._dao.delete_feed(feed_id)
                self._dao.commit()

    @property
    def dao(self):
        return self._dao

    def load(self, provider: DataProvider):
        self.logger.info("Importing data from provided source")
        provider.load_data_source(self._dao)

    def process(self, processor: Processor = None):
        self.logger.info("Processing data from provided source")

        # Here we should use a rule providers to have more flexibility when processing data
        # providers.process(ruleset)

        for route in self._dao.routes():
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

        self._dao.commit()

    def export(self, bundle = False, out_path: str = out_path) -> str:
        self.logger.info(f"Generating archive with name gtfs-{self._arguments['--id']}.zip")

        class __Args:
            filter = None

        context = Context(self._dao, __Args(), out_path)

        if bundle:
            w = Writer(context, bundle=f"gtfs-{self._arguments['--id']}.zip")
        else:
            w = Writer(context)

        w.run()

        return out_path


@measure_execution_time
def main():
    init_logging()
    init_filesystem()

    arguments = docopt(__doc__, version='gtfs-exporter %s' % version)
    provider_type = arguments['--provider']
    provider = DataProvider()
    if provider_type == "file":
        provider = FileDataProvider(arguments['--file'],
                                    feed_id=arguments['--id'],
                                    lenient=arguments['--lenient'],
                                    disable_normalization=arguments['--disablenormalize'])
    elif provider_type == "url":
        provider = HttpDataProvider(arguments['--url'],
                                    feed_id=arguments['--id'],
                                    lenient=arguments['--lenient'],
                                    disable_normalization=arguments['--disablenormalize'])
    elif provider_type == "providers":
        builder = ApiProviderBuilder(arguments['--url'],
                             feed_id=arguments['--id'],
                             lenient=arguments['--lenient'],
                             disable_normalization=arguments['--disablenormalize'])
        provider = builder.build()

    exporter = StaticExporter(arguments)
    # exporter.addProcessor()
    sg = ShapeGenerator("https://download.geofabrik.de/europe/romania-latest.osm.bz2", out_path)

    # flow needs to be different when receiving data from providers
    #  - load
    #  - process
    #  - generate initial gtfs files
    #  - generate shapes for gtfs
    #  - generate bundle
    # for zip, url
    #  - generation of shapes
    #  - load all the feed to process & interpolate
    #  - generate feed (bundle)
    if provider.is_from_api():
        exporter.load(provider)
        exporter.process()
        exporter.export(bundle=False)

        sg.generate()
        from exporter.util.storage import generate_gtfs_bundle
        generate_gtfs_bundle(out_path, bundle=f"gtfs-{arguments['--id']}.zip")
    else:
        sg.generate()
        exporter.load(provider)
        exporter.process()
        exporter.export(bundle=True)

    rg = ReleaseGenerator(GH_REPO, GH_TOKEN)

    rg.generate([
                    os.path.join(out_path, f"gtfs-{arguments['--id']}.zip"),
                ] + glob.glob(os.path.join(out_path, "*.json")))


if __name__ == '__main__':
    main()