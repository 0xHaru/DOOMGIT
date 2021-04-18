import os
import shutil

from DOOM import doom
from DOOM.utils import util

POSITIVE_REPLY = ["y", "Y", "yes", "Yes", "YES"]


class PromptException(Exception):
    pass


def prompt(path):
    choice = input(
        f"{util.Color.YELLOW}{path}{util.Color.END} already exists, "
        f"do you want to remove it? [y/N] "
    )

    return choice


def traversal_handler(choice, path, json, resource):
    if choice in POSITIVE_REPLY:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

        doom.Resource.traversal(resource, json, path)
    else:
        raise PromptException()


def file_handler(choice, path, file_):
    if choice in POSITIVE_REPLY:
        os.remove(path)
        file_.download(doom.CWD[0:-1])
    else:
        raise PromptException()
