"""

Copyright (C) 2017-2020 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from helpme.logger import bot
import sys
import requests
import json
import urllib
import webbrowser


def create_issue(title, body, repo, token):
    """create a Github issue, given a title, body, repo, and token.

       Parameters
       ==========
       title: the issue title
       body: the issue body
       repo: the full name of the repo
       token: the user's personal Github token

    """
    owner, name = repo.split("/")
    url = "https://api.github.com/repos/%s/%s/issues" % (owner, name)

    data = {"title": title, "body": body}

    headers = {
        "Authorization": "token %s" % token,
        "Accept": "application/vnd.github.symmetra-preview+json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code in [201, 202]:
        url = response.json()["html_url"]
        bot.info(url)
        return url

    elif response.status_code == 404:
        bot.error("Cannot create issue. Does your token have scope repo?")
        sys.exit(1)

    else:
        bot.error("Cannot create issue %s" % title)
        bot.error(response.content)
        sys.exit(1)


def open_issue(title, body, repo):
    """open a GitHub issue given a title, body, and repository. Does not
       rely on the GitHub API, but instead opens a browser URL.

       Parameters
       ==========
       title: the issue title
       body: the issue body
       repo: the full name of the repo
    """
    owner, name = repo.split("/")

    # Title is best separated with +
    title = title.replace(" ", "+")
    body = urllib.parse.quote(body)
    url = "https://github.com/%s/%s/issues/new?labels=bug&title=%s&body=%s" % (
        owner,
        name,
        title,
        body,
    )
    bot.info("Browser opening to:")
    bot.info(webbrowser.open_new(url))
