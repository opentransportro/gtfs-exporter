import os
import stat
import time
import zipfile
import logging
import shutil

import six


from exporter import __version__ as version, __temp_path__ as tmp_path, __output_path__ as out_path, \
    __cwd_path__ as app_path, __map_path__ as map_path



logger = logging.getLogger('gtfsexporter')

def create_folder(folder: str):
    try:
        logger.info(f" - creating {folder}")
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
    except:
        pass


def init_filesystem():
    logger.info("creating work directories if not exist")
    create_folder(out_path)
    create_folder(tmp_path)
    create_folder(map_path)


def file_age_in_seconds(pathname):
    return int(time.time() - os.stat(pathname)[stat.ST_MTIME])


def generate_gtfs_bundle(source_path, bundle: str = None):
    if not isinstance(bundle, six.string_types):
        # Allow the use of "--bundle" option only
        bundle = "gtfs.zip"
    if not bundle.endswith('.zip'):
        bundle = bundle + '.zip'

    with zipfile.ZipFile(os.path.join(source_path, bundle), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in ["agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt", "calendar_dates.txt",
                  "fare_rules.txt", "fare_attributes.txt", "shapes.txt", "transfers.txt"]:
            archived_file = os.path.join(source_path, f)

            if os.path.isfile(archived_file):
                zipf.write(archived_file, f)
                os.remove(archived_file)
