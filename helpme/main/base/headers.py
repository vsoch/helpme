"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.logger import bot
import json
import re
import os
import sys

# Headers


def get_headers(self):
    """simply return the headers
    """
    return self.headers


def reset_headers(self):
    """reset headers to a reasonable default to specify content type of json
    """
    self.headers = {"Content-Type": "application/json"}


def update_headers(self, fields=None):
    """update headers with a token & other fields
    """
    do_reset = True
    if hasattr(self, "headers"):
        if self.headers is not None:
            do_reset = False

    if do_reset is True:
        self._reset_headers()

    if fields is not None:
        for key, value in fields.items():
            self.headers[key] = value

    header_names = ",".join(list(self.headers.keys()))
    bot.debug("Headers found: %s" % header_names)


def basic_auth_header(username, password):
    """generate a base64 encoded header to ask for a token. This means
                base64 encoding a username and password and adding to the
                Authorization header to identify the client.

    Parameters
    ==========
    username: the username
    password: the password
   
    """
    s = "%s:%s" % (username, password)
    if sys.version_info[0] >= 3:
        s = bytes(s, "utf-8")
        credentials = base64.b64encode(s).decode("utf-8")
    else:
        credentials = base64.b64encode(s)
    auth = {"Authorization": "Basic %s" % credentials}
    return auth
