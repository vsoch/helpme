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


def main(args, extras):
    """This is the actual driver for the helper.
    """

    from helpme.main import get_helper

    name = args.command

    if name in HELPME_HELPERS:

        # Get the helper, do the recording, submit

        helper = get_helper(name=name)

        if args.asciinema is not None:
            if os.path.exists(args.asciinema):
                helper.data["record_asciinema"] = args.asciinema

        helper.run(positionals=extras)
