import os
import sys
import urllib.parse as url_parser

from DOOM import doom
from DOOM.utils import prompt_util, url_util, util


def download_file(resource, json_obj):
    file_ = doom.File.constructor(resource, json_obj)
    path = doom.CWD + file_.name

    if os.path.isfile(path):
        choice = prompt_util.prompt(file_.name)
        prompt_util.file_handler(choice, path, file_)
    else:
        file_.download(doom.CWD[0:-1])


def main():
    try:
        util.args_parser(sys.argv)

        url = sys.argv[1]
        url_util.github_validator(url)
        sanitized_url = url_parser.unquote(url)

        resource = doom.Resource.constructor(sanitized_url)
        json = resource.get_json()

        if isinstance(json, list):
            resource.traversal(json, resource.name)
        else:
            download_file(resource, json)
    except util.HelpException:
        exit(0)
    except url_util.UrlError as e:
        url_util.UrlError.handler(e)
        exit(1)
    except url_util.UrlException as e:
        url_util.UrlException.handler(e, url)
        exit(0)
    except prompt_util.PromptException:
        exit(1)
    except Exception as e:
        util.exception_handler(e, json)
        exit(1)


if __name__ == "__main__":
    main()
