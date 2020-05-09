from datetime import date
from github import Github


class ReleaseGenerator(object):
    def __init__(self, repo: str, token: str = None):
        self.token = token
        self.repo = repo

    def generate(self, files=None):
        if files is None:
            files = []

        g = Github(self.token)
        repo = g.get_repo(self.repo)

        self.__delete_release("latest", repo)
        self.__delete_release(str(date.today()), repo)

        self.__make_release("latest", repo, files)
        self.__make_release(str(date.today()), repo, files)

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