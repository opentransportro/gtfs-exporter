import errno
import logging
import os
import shutil
import stat
import time
import zipfile
from datetime import date

import six
from github import Github
from paramiko.sftp_client import SFTPClient
from paramiko.transport import Transport

from exporter import __temp_path__ as tmp_path, __output_path__ as out_path, \
    __map_path__ as map_path

logger = logging.getLogger('gtfsexporter')


def create_folder(folder: str, forced: bool = False):
    try:
        if not os.path.exists(folder) or forced:
            logger.info(f" - creating {folder}")
            if forced:
                logger.info(f" - creating {folder}")
            os.mkdir(folder)
    except:
        pass


def init_filesystem():
    logger.info("creating work directories if not exist")
    create_folder(out_path, forced=True)
    create_folder(tmp_path, forced=True)
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


class ReleaseGenerator(object):
    def __init__(self, repo: str, token: str = None):
        self.token = token
        self.repo = repo

    def generate(self, files=None):
        if files is None:
            files = []

        if not (self.token is None or self.repo is None):
            g = Github(self.token)
            repo = g.get_repo(self.repo)

            self.__delete_release(str(date.today()), repo)
            self.__delete_release("latest", repo)

            self.__make_release(str(date.today()), repo, files)
            self.__make_release("latest", repo, files)
        else:
            logger.warning(
                "Skipping release generation since provided repo and tokens do no exist")

    @staticmethod
    def __make_release(name: str, repo, files):
        release = repo.create_git_release(name, "", "")
        import os
        for file in files:
            release.upload_asset(file, os.path.basename(file))

    @staticmethod
    def __delete_release(name, repo):
        try:
            release = repo.get_release(name)
            if not release is None:
                release.delete_release()
        except:
            pass


class SFTPReleaseGenerator(object):
    _connection = None
    _remote_path = "/var/www/data.opentransport.ro/routing/gtfs/"

    def __init__(self, address, port, user, password, path):
        self.create_connection(address, port, user, password)
        self._remote_path = path

    @classmethod
    def create_connection(cls, host, port, username, password):

        transport = Transport(sock=(host, port))
        transport.connect(username=username, password=password)
        cls._connection = SFTPClient.from_transport(transport)

    @staticmethod
    def uploading_info(uploaded_file_size, total_file_size):

        logger.info('uploaded_file_size : {} total_file_size : {}'.
                    format(uploaded_file_size, total_file_size))

    def upload(self, local_path, remote_path):

        self._connection.put(localpath=local_path,
                             remotepath=remote_path,
                             callback=self.uploading_info,
                             confirm=True)

    def file_exists(self, remote_path):
        try:
            print('remote path : ', remote_path)
            self._connection.stat(remote_path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True

    def generate(self, files=None):
        if files is None:
            files = []
        timestr = time.strftime("-%Y%m%d")
        for local_file in files:
            remote_file = self._remote_path + os.path.basename(local_file)
            filename, ext = os.path.splitext(os.path.basename(local_file))

            if self.file_exists(remote_file):
                if self.file_exists(self._remote_path + filename + timestr + ext):
                    self._connection.remove(self._remote_path + filename + timestr + ext)
                self._connection.rename(remote_file, self._remote_path + filename + timestr + ext)

            self.upload(local_file, remote_file)
