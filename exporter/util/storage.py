import os
import stat
import time
import zipfile

import six


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