import json
import os

import requests

from DOOM import config
from DOOM.utils import prompt_util, url_util, util

# Full path of the current working directory
CWD = str(os.path.abspath(os.getcwd())) + "/"
# Name of the current working directory
NCWD = list(filter(lambda x: x, CWD.split("/")))[-1]

session = requests.Session()
if config.USERNAME and config.TOKEN:
    session.auth = (config.USERNAME, config.TOKEN)


class Resource:
    def __init__(self, user, repo, branch, path, name):
        self.user = user
        self.repo = repo
        self.branch = branch
        self.path = path
        self.name = name

    def __repr__(self):
        return (
            f"Resource({self.user}, {self.repo}, {self.branch}, "
            f"{self.path}, {self.name})"
        )

    def __str__(self):
        return (
            f"User: {self.user} - Repo: {self.repo} - Branch: {self.branch} - "
            f"Path: {self.path} - Name: {self.name}"
        )

    @staticmethod
    def constructor(url):
        url_params = url_util.get_params(url)

        user = url_params[2]
        repo = url_params[3]
        name = url_params[-1]
        branch = url_params[5]
        path = "/".join(url_params[6:-1]) if url_params[6:-1] else None

        return Resource(user, repo, branch, path, name)

    @staticmethod
    def request(url):
        response = session.get(url)
        return json.loads(response.text)

    def get_json(self):
        if self.path is None:
            url = (
                f"https://api.github.com/repos/{self.user}/{self.repo}"
                f"/contents/{self.name}?ref={self.branch}"
            )
            json = Resource.request(url)
        else:
            url = (
                f"https://api.github.com/repos/{self.user}/{self.repo}"
                f"/contents/{self.path}/{self.name}?ref={self.branch}"
            )
            json = Resource.request(url)

        return json

    def traversal(self, json, path):
        try:
            download_path = CWD + path
            os.mkdir(download_path)

            for obj in json:
                if obj["type"] == "file":
                    file_ = File.constructor(self, obj)
                    file_.download(download_path)
                else:
                    directory = Directory.constructor(self, obj)

                    dir_json = Resource.request(directory.url)
                    Resource.traversal(self, dir_json, path + "/" + directory.name)
        except FileExistsError:
            choice = prompt_util.prompt(path)
            prompt_util.traversal_handler(choice, path, json, self)
        except TypeError as e:
            util.exception_handler(e, json)
            exit(1)


class Directory(Resource):
    def __init__(self, user, repo, branch, path, name, url):
        super().__init__(user, repo, branch, path, name)
        self.url = url

    def __repr__(self):
        return (
            f"Directory({self.user}, {self.repo}, {self.branch}, {self.path}, "
            f"{self.name}, {self.url})"
        )

    def __str__(self):
        return (
            f"User: {self.user} - Repo: {self.repo} - Branch: {self.branch} - "
            f"Path: {self.path} - Name: {self.name} - URL: {self.url}"
        )

    @staticmethod
    def constructor(resource, json_obj):
        return Directory(
            resource.user,
            resource.repo,
            resource.branch,
            json_obj["path"],
            json_obj["name"],
            json_obj["url"],
        )


class File(Resource):
    def __init__(self, user, repo, branch, path, name, download_url):
        super().__init__(user, repo, branch, path, name)
        self.download_url = download_url

    def __repr__(self):
        return (
            f"File({self.user}, {self.repo}, {self.branch}, {self.path}, "
            f"{self.name}, {self.download_url})"
        )

    def __str__(self):
        return (
            f"User: {self.user} - Repo: {self.repo} - Branch: {self.branch} - "
            f"Path: {self.path} - Name: {self.name} - Download_URL: {self.download_url}"
        )

    @staticmethod
    def constructor(resource, json_obj):
        return File(
            resource.user,
            resource.repo,
            resource.branch,
            json_obj["path"],
            json_obj["name"],
            json_obj["download_url"],
        )

    def download(self, path):
        os.popen(f"wget -q -O '{path}/{self.name}' '{self.download_url}'")

        clean_path = path[path.find(NCWD) + len(NCWD) + 1 :]

        if not clean_path:
            clean_path = "."

        print(f"{util.Color.GREEN}Downloaded:{util.Color.END} {clean_path}/{self.name}")
