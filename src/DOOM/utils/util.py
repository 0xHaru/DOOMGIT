import traceback

from DOOM.utils import url_util

VERSION = "0.1.0"

HELP = ["-h", "--help"]


class HelpException(Exception):
    pass


class Color:
    RED = "\033[1;31m"
    YELLOW = "\033[1;33m"
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    END = "\033[0m"


def exception_handler(e, json):
    # Rate limit reached
    if not isinstance(json, list) and "documentation_url" in json.keys():
        print(
            f"{Color.RED}Error:{Color.END} {json['message']}\n"
            f"{Color.BLUE}Documentation:{Color.END} {json['documentation_url']}"
        )
    else:
        traceback.print_exception(type(e), e, e.__traceback__)


def help():
    print(
        f"doomgit {VERSION}\n0xHaru <0xharu.git@gmail.com>\n"
        "Project home page: https://github.com/0xHaru/DOOMGIT\n\n"
        "A CLI tool to download any file or directory from GitHub.\n\n"
        f"{Color.BLUE}USAGE:{Color.END}\n\tdoomgit <url>\n\n"
        f"{Color.BLUE}ARGS:{Color.END}\n\t<url>\turl of a file or directory\n\n"
        f"{Color.BLUE}EXAMPLE:{Color.END}\n\tdoomgit "
        "https://github.com/ryanoasis/nerd-fonts/tree/master"
        "/patched-fonts/JetBrainsMono\n\n"
        f"{Color.BLUE}CONFIG:{Color.END}\n\t"
        "Edit the config file to be able to make authenticated requests.\n\n\t"
        "For unauthenticated requests, "
        "the rate limit allows for up to 60 requests per hour.\n\t"
        "For authenticated requests, "
        "the rate limit allows for up to 5000 requests per hour.\n\n\t"
        "Authentication will allow you to download files and directories "
        "from your private repositories.\n\n\t"
        "This command will output the full path of the config file:\n\t    "
        f"{Color.GREEN}pip show doomgit | "
        "grep 'Location' | grep -o -E '[/].+' | "
        r"xargs printf '%s/DOOM/config.py\n'"
        f"{Color.END}\n{Color.BLUE}LINKS:{Color.END}\n\t"
        "https://docs.github.com/en/rest/overview"
        "/resources-in-the-rest-api#authentication\n\t"
        "https://docs.github.com/en/github/authenticating-to-github"
        "/creating-a-personal-access-token\n\t"
        "https://docs.github.com/en/developers/apps/scopes-for-oauth-apps\n\t"
        "https://docs.github.com/en/rest/overview"
        "/resources-in-the-rest-api#rate-limiting"
    )


def args_parser(argv):
    if len(argv) < 2:
        raise url_util.UrlError("missing URL")

    if argv[1] in HELP:
        help()
        raise HelpException()
