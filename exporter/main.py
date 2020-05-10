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
import logging
import logging.handlers
import os
import shutil

from docopt import docopt
from environs import Env

from exporter import Exporter
from exporter import __version__ as version, __temp_path__ as tmp_path, __output_path__ as out_path, \
    __cwd_path__ as app_path, __map_path__ as map_path
from exporter.api.builder import ProviderBuilder
from exporter.provider import DataProvider, FileDataProvider, HttpDataProvider
from exporter.util.perf import measure_execution_time
from exporter.util.spatial import ShapeGenerator
from exporter.vcs.github import ReleaseGenerator


def init_logging():

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger('gtfsexporter')
    logger.setLevel(logging.INFO)

    # sh = logging.StreamHandler(sys.stdout)
    # logger.addHandler(sh)


@measure_execution_time
def main():
    env = Env()
    env.read_env(app_path)  # read .env file, if it exists

    init_logging()

    logger = logging.getLogger('gtfsexporter')
    logger.info("creating work directories if not exist")
    try:
        logger.info(" - creating out")
        if os.path.exists(out_path):
            shutil.rmtree(out_path)
        os.mkdir(out_path)
    except:
        pass

    try:
        logger.info(" - creating tmp")
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        os.mkdir(tmp_path)
    except:
        pass

    try:
        logger.info(" - creating map")
        os.mkdir(map_path)
    except:
        pass

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
        builder = ProviderBuilder(arguments['--url'],
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
    if provider.is_from_api():
        exporter.load(provider)
        exporter.process()
        exporter.export(bundle=False)

        sg.generate()
        from exporter.util.storage import generate_gtfs_bundle
        generate_gtfs_bundle(out_path, bundle=f"gtfs-{arguments['--id']}.zip")

    # for zip, url
    #  - generation of shapes
    #  - load all the feed to process & interpolate
    #  - generate feed (bundle)
    else:
        sg.generate()
        exporter.load(provider)
        exporter.process()
        exporter.export(bundle=True)

    gh_repo = env.str("GH_REPO", None)
    gh_token = env.str("GH_TOKEN", None)

    if not (gh_repo is None or gh_token is None):
        rg = ReleaseGenerator(gh_repo, gh_token)

        rg.generate([
                        os.path.join(out_path, f"gtfs-{arguments['--id']}.zip"),
                    ] + glob.glob(os.path.join(out_path, "*.json")))
    else:
        logger.warning("Skipping release generation since provided repo and tokens do no exist")


if __name__ == '__main__':
    main()
