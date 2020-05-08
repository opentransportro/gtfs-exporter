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
import sys
import os
import glob
from docopt import docopt
import logging
import logging.handlers
from exporter.api.builder import ProviderBuilder
from exporter.provider import DataProvider, FileDataProvider, HttpDataProvider
from exporter import Exporter
from exporter import __version__ as version, __temp_path__ as tmp_path, __output_path__ as out_path, \
    __cwd_path__ as app_path, __map_path__ as map_path
from environs import Env


def main():
    env = Env()
    env.read_env(app_path)  # read .env file, if it exists

    logger = logging.getLogger('grfsexporter')
    logger.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler('../export.log', mode="w", maxBytes=10240, backupCount=5)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    logger.addHandler(sh)

    # if os.path.exists(tmp_path):
    #     shutil.rmtree(tmp_path)

    logger.info("creating work directories if not exist")
    try:
        logger.info(" - creating out")
        os.mkdir(out_path)
    except:
        pass

    try:
        logger.info(" - creating tmp")
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

    instance = Exporter(arguments, provider)
    instance.generate_shapes()
    instance.process_gtfs()

    from exporter.vcs.github import ReleaseGenerator
    gh_repo = env.str("GH_REPO", None)
    gh_token = env.str("GH_TOKEN", None)

    if not (gh_repo is None or gh_token is None):
        rg = ReleaseGenerator(gh_repo, gh_token)

        rg.generate([
                        os.path.join(app_path, f"gtfs-{arguments['--id']}.zip"),
                    ] + glob.glob(os.path.join(tmp_path, "*.json")))
    else:
        logger.warning("Skipping release generation since provided repo and tokens do no exist")


if __name__ == '__main__':
    main()
