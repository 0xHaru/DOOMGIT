<div align="center">
<h1>DOOMGIT</h1>
</div>

![](https://raw.githubusercontent.com/0xHaru/DOOMGIT/master/media/example.png)

A CLI tool to download any file or directory from GitHub.

## Prerequisites

-   Linux

-   Python 3.6+

-   [Requests](https://docs.python-requests.org/en/latest/user/install/#install)

-   GNU Wget 1.20.3+ (it might work on earlier versions but it's not been tested)

## Installation

`pip install doomgit`

## Usage

`doomgit <url>`

\<url\> - url of a file or directory

## Example

`doomgit https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/JetBrainsMono`

## Configuration

Edit the config file to be able to make authenticated requests.

For unauthenticated requests, the rate limit allows for up to 60 requests per hour.

For authenticated requests, the rate limit allows for up to 5000 requests per hour.

Authentication will allow you to download files and directories from your private repositories.

This command will output the full path of the config file:

`pip show doomgit | grep 'Location' | grep -o -E '[/].+' | xargs printf '%s/DOOM/config.py\n'`

### Links

-   [docs.github.com/authentication](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#authentication)

-   [docs.github.com/creating-a-personal-access-token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

-   [docs.github.com/scopes-for-oauth-apps](https://docs.github.com/en/developers/apps/scopes-for-oauth-apps)

-   [docs.github.com/rate-limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)

## Troubleshooting

### doomgit: command not found

Execute this command: `echo "$PATH" | grep -q "/.local/bin" && echo "true" || echo "false"`

If it returns "false" add this line to your .bashrc/.zshrc: `export PATH="$HOME/.local/bin:$PATH"`

## Inspiration

This project was inspired by DownGit - [github.com/MinhasKamal/DownGit](https://github.com/MinhasKamal/DownGit)

The name of the project was inspired by Doom Emacs - [github.com/hlissner/doom-emacs](https://github.com/hlissner/doom-emacs)

## License

This project uses the following license: [GPLv3](https://github.com/0xHaru/DOOMGIT/blob/master/LICENSE).
