"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.logger import bot
from helpme.defaults import HELPME_HELPERS
import sys
import pwd
import os


def main(args, extra):
    """print the listing of helpers installed, defined by the HELPME_HELPERS
       variable in the default settings flie, and then exit.
    """
    bot.info("Helpers Installed:")
    print("\n".join(HELPME_HELPERS))
