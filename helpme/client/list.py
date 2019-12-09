"""

Copyright (C) 2018-2020 Vanessa Sochat.

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
