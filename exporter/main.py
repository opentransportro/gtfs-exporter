"""gtfs-exporter - GTFS to GTFS' conversion tool and database loader
Usage:
  gtfs-exporter (--provider=<provider> | --delete | --list ) [--url=<url>] [--file=<file>] [--id=<id>]
                        [--logsql] [--lenient] [--schema=<schema>]
                        [--disablenormalize]
  gtfs-exporter (-h | --help)
  gtfs-exporter --version
Options:
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
  gtfs-exporter --provider=url --url=https://api.opentransport.ro/gtfs/v1/static --id=timisoara
        Load GTFS from url using id "sncf", deleting previous data.
  gtfs-exporter --delete --id=moontransit
        Delete the "moontransit" feed from the database.
  gtfs-exporter --list
        List all feed IDs from database
Authors:
"""
import glob
import os

from docopt import docopt

from exporter import Exporter, __version__ as version, __output_path__ as out_path
from exporter.api import ApiBuilder
from exporter.provider import DataProvider, FileDataProvider, HttpDataProvider
from exporter.settings import GH_REPO, GH_TOKEN
from exporter.util.logging import init_logging
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import ShapeGenerator
from exporter.util.storage import init_filesystem
from exporter.vcs.github import ReleaseGenerator


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
        builder = ApiBuilder(arguments['--url'],
                             feed_id=arguments['--id'],
                             lenient=arguments['--lenient'],
                             disable_normalization=arguments['--disablenormalize'])
        provider = builder.build()

    exporter = Exporter(arguments)
    sg = ShapeGenerator("https://download.geofabrik.de/europe/romania-latest.osm.bz2", out_path)

    # flow needs to be different when receiving data from api
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
