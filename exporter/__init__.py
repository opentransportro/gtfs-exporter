import logging
import os

from exporter.gtfs.dao import Dao
from exporter.gtfs.model import Route

from exporter.provider import DataProvider
from exporter.writer import Writer, Context
from exporter.processor import Processor

__version__ = "1.0.0"
__cwd_path__ = os.path.abspath(os.getcwd())
__temp_path__ = os.path.join(__cwd_path__, "tmp")
__map_path__ = os.path.join(__cwd_path__, "map")
__output_path__ = os.path.join(__cwd_path__, "out")


class Exporter:
    def __init__(self, arguments):
        self.logger = logging.getLogger('gtfsexporter')
        self._arguments = arguments

        if arguments['--id'] is None:
            arguments['--id'] = "default"

        database_path = os.path.join(__cwd_path__, arguments['--id'] + ".sqlite")

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

        # Here we should use a rule processor to have more flexibility when processing data
        # processor.process(ruleset)

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

    def export(self, bundle = False, out_path: str = __output_path__) -> str:
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
