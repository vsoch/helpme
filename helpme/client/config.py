"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.logger import bot
import sys
import pwd
import os


def main(args, extra):
    """Configure a client for the user"""
    from helpme.main.base.settings import get_configfile_user

    config_file = get_configfile_user()
    bot.info("Configuration file is generated at %s" % config_file)
