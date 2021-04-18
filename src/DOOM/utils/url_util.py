import os
import re

from DOOM.utils import util

VALID_PARAMS = ["tree", "blob"]


class UrlException(Exception):
    @staticmethod
    def handler(e, url):
        if str(e) == "repository":
            os.popen(f"git clone {url}").readline()
        else:
            clean_url = "/".join(url.split("/")[0:-2])
            os.popen(f"git clone --single-branch --branch {e} {clean_url}").readline()


class UrlError(TypeError):
    @staticmethod
    def handler(e):
        print(f"{util.Color.RED}Error:{util.Color.END} {str(e)}")


def get_params(url):
    return list(filter(lambda x: x, url.split("/")))


def github_validator(url):
    pattern = "https?://github.com/.+/.+"
    result = re.match(pattern, url)

    url_params = get_params(url)

    if (
        not result
        or len(url_params) == 5
        or (len(url_params) > 5 and url_params[4] not in VALID_PARAMS)
    ):
        raise UrlError("bad URL")

    repo = url_params[3]
    name = url_params[-1]

    if repo == name:
        raise UrlException("repository")

    if len(url_params) == 6 and url_params[4] == "tree":
        branch = url_params[5]
        raise UrlException(branch)

    return True
