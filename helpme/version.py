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

__version__ = "0.0.39"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "helpme"
PACKAGE_URL = "http://www.github.com/researchapps/helpme-client"
KEYWORDS = "hpc, help, asciinema, questions, answers, client"
DESCRIPTION = "command line client for helping you out."
LICENSE = "LICENSE"


################################################################################
# Global requirements


INSTALL_REQUIRES = (
    ("requests", {"min_version": "2.18.4"}),
    ("asciinema", {"min_version": "2.0.1"}),
)

################################################################################
# Submodule Requirements


INSTALL_USERVOICE = (("uservoice", {"min_version": "0.0.23"}),)


INSTALL_DISCOURSE = (("pycryptodome", {"min_version": "3.7.2"}),)

INSTALL_ALL = INSTALL_REQUIRES + INSTALL_USERVOICE + INSTALL_DISCOURSE
