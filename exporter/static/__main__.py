"""gtfs-exporter - GTFS to GTFS' conversion tool and database loader
Usage:
  gtfs-exporter (--provider=<provider> | --delete | --list ) [--url=<url>] [--file=<file>] [--id=<id>] [--processors=<processors>]
                        [--logsql] [--lenient] [--schema=<schema>]
                        [--disablenormalize]
  gtfs-exporter (-h | --help)
  gtfs-exporter --version
Options:
  --provider=<provider>         The provider type. Can be file, url or providers.
  --url=<url>
  --file=<file>
  --id=<id>                     Set the feed ID in case multiple GTFS are to be loaded.
  --processors=<processors>     The list of processors as the following: 'processorA, processorB, ...'.
  -h --help                     Show help on options.
  --version                     Show lib / program version.
  --logsql                      Enable SQL logging (very verbose)
  --lenient                     Allow some level of brokenness in GTFS input.
  --schema=<schema>             Set the schema to use (for PostgreSQL).
  --disablenormalize            Disable shape and stop times normalization. Be careful
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
from exporter.static.processors import Processor, OSRMTimeProcessor, RouteColorProcessor
from exporter.static.providers import ApiProviderBuilder
from exporter.static.providers import DataProvider, FileDataProvider, HttpDataProvider
from exporter.settings import GH_REPO, GH_TOKEN
from exporter.util.logging import init_logging
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import ShapeGenerator
from exporter.util.storage import init_filesystem, ReleaseGenerator
from exporter.writer import Context, Writer


class StaticExporter:
    def __init__(self, arguments):
        self.logger = logging.getLogger('gtfsexporter')
        self._arguments = arguments

        if arguments['--id'] is None:
            arguments['--id'] = "default"

        database_path = os.path.join(cwd_path, arguments['--id'] + ".sqlite")

        self._dao = Dao(database_path, sql_logging=arguments['--logsql'], schema=arguments['--schema'])


    @property
    def dao(self):
        return self._dao

    def load(self, provider: DataProvider):
        self.logger.info("Importing data from provided source")
        provider.load_data_source(self._dao)

    def process(self, processors: [Processor] = []):
        self.logger.info("Applying processors on the obtained dataset")

        for processor in processors:
            processor.process(self._dao)

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


class ProcessorArgsParser:
    def __init__(self, argument):
        self._processors = list()

        parsed_processors = argument.replace(' ', '').split(',')

        if 'stop_time' in parsed_processors:
            self._processors.append(OSRMTimeProcessor())

        if 'route_color' in parsed_processors:
            self._processors.append(RouteColorProcessor())


    def get_all(self):
        return self._processors


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
    elif provider_type == "api":
        builder = ApiProviderBuilder(arguments['--url'],
                             feed_id=arguments['--id'],
                             lenient=arguments['--lenient'],
                             disable_normalization=arguments['--disablenormalize'])
        provider = builder.build()

    exporter = StaticExporter(arguments)
    
    sg = ShapeGenerator("https://download.geofabrik.de/europe/romania-latest.osm.bz2", out_path)

    processors = []
    if arguments['--processors'] is not None:
        processors_parser = ProcessorArgsParser(arguments['--processors'])
        processors = processors_parser.get_all()

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
        exporter.process(processors=processors)

        exporter.export(bundle=False)

        sg.generate()
        from exporter.util.storage import generate_gtfs_bundle
        generate_gtfs_bundle(out_path, bundle=f"gtfs-{arguments['--id']}.zip")
    else:
        sg.generate()
        exporter.load(provider)
        exporter.process(processors=processors)
        exporter.export(bundle=True)

    rg = ReleaseGenerator(GH_REPO, GH_TOKEN)

    rg.generate([
                    os.path.join(out_path, f"gtfs-{arguments['--id']}.zip"),
                ] + glob.glob(os.path.join(out_path, "*.json")))


if __name__ == '__main__':
    main()