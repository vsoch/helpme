"""

Copyright (C) 2018-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from helpme.logger import RobotNamer
from helpme.logger import bot
import sys
from tempfile import mktemp
from base64 import b64decode
import uuid
import requests
import json

enter_input = getattr(__builtins__, "raw_input", input)


def request_token(self, board):
    """send a public key to request a token. When we call this function,
       we already have an RSA key at self.key

       board: the discourse board to post to
    """
    nonce = str(uuid.uuid4())

    data = {
        "scopes": "write",
        "client_id": self.client_id,
        "application_name": "HelpMe",
        "public_key": self.public_key.replace("'", ""),
        "nonce": nonce,
    }

    url = (
        board
        + "/user-api-key/new?scopes=write&application_name=HelpMe&public_key="
        + self.public_key.replace("'", "")
        + "&client_id="
        + self.client_id
        + "&nonce="
        + nonce
    )

    bot.newline()
    bot.info("Open browser to:")
    bot.info(url)
    bot.newline()

    # the user will open browser, get a token, and then have it saved here.
    bot.info("Copy paste token, press Ctrl-D to save it:")

    lines = []

    # The message is multiple lines
    while True:
        try:
            line = enter_input()
        except EOFError:
            break
        if line:
            lines.append(line)

    message = "\n".join(lines)

    # Write to temporary file, we only need to get key
    tmpfile = mktemp()
    with open(tmpfile, "w") as filey:
        filey.write(message)

    # Read in again, and get token **important** is binary
    with open(tmpfile, "rb") as filey:
        message = filey.read()

    # uses pycryptodome (3.7.2)
    cipher = Cipher_PKCS1_v1_5.new(self.key)
    decrypted = json.loads(cipher.decrypt(b64decode(message), None).decode())

    # Validate nonce is in response
    if "nonce" not in decrypted:
        bot.exit("Missing nonce field in response for token, invalid.")

    # Must return nonce that we sent
    if decrypted["nonce"] != nonce:
        bot.exit("Invalid nonce, exiting.")

    return decrypted["key"]


def create_post(self, title, body, board, category, username):
    """create a Discourse post, given a title, body, board, and token.

       Parameters
       ==========
       title: the issue title
       body: the issue body
       board: the discourse board to post to

    """

    category_url = "%s/categories.json" % board
    response = requests.get(category_url)

    if response.status_code != 200:
        print("Error with retrieving %s" % category_url)
        sys.exit(1)

    # Get a list of all categories
    categories = response.json()["category_list"]["categories"]
    categories = {c["name"]: c["id"] for c in categories}

    # And if not valid, warn the user
    if category not in categories:
        bot.warning("%s is not valid, will use default" % category)

    category_id = categories.get(category, None)

    headers = {
        "Content-Type": "application/json",
        "User-Api-Client-Id": self.client_id,
        "User-Api-Key": self.token,
    }

    # First get the category ids
    data = {"title": title, "raw": body, "category": category_id}

    response = requests.post(
        "%s/posts.json" % board, headers=headers, data=json.dumps(data)
    )

    if response.status_code in [200, 201, 202]:
        topic = response.json()
        url = "%s/t/%s/%s" % (board, topic["topic_slug"], topic["topic_id"])
        bot.info(url)
        return url

    elif response.status_code == 404:
        bot.error("Cannot post to board, not found. Do you have permission?")
        sys.exit(1)

    else:
        bot.error("Cannot post to board %s" % board)
        bot.error(response.content)
        sys.exit(1)
