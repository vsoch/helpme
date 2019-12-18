"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.logger import bot
import sys


def auth_flow(self, url):
    """auth flow is a function to present the user with a url to retrieve
       some token/code, and then copy paste it back in the terminal.

        Parameters
        ==========
        url should be a url that is generated for the user to go to and accept
        getting a credential in the browser.
    
    """
    print("Please go to this URL and login: {0}".format(url))
    get_input = getattr(__builtins__, "raw_input", input)
    message = "Please enter the code you get after login here: "
    code = get_input(message).strip()
    return code
