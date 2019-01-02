'''

Copyright (C) 2018 Vanessa Sochat.

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

'''

from helpme.logger import bot
from helpme.defaults import HELPME_HELPERS
import sys
import pwd
import os


def main(args, extras):
    '''This is the actual driver for the helper.
    '''

    from helpme.main import get_helper
    name = args.command

    if name in HELPME_HELPERS:

        # Get the helper, do the recording, submit

        helper = get_helper(name=name)

        if args.asciinema is not None:
            if os.path.exists(args.asciinema):
                helper.data['record_asciinema'] = args.asciinema
 
        helper.run(positionals=extras)
