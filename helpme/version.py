"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

__version__ = "0.0.43"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "helpme"
PACKAGE_URL = "http://www.github.com/researchapps/helpme-client"
KEYWORDS = "hpc, help, asciinema, questions, answers, client"
DESCRIPTION = "command line client for helping you out."
LICENSE = "LICENSE"


################################################################################
# Global requirements


INSTALL_REQUIRES = (("requests", {"min_version": "2.18.4"}),)
INSTALL_GITHUB = INSTALL_REQUIRES

################################################################################
# Submodule Requirements

INSTALL_ASCIINEMA = (("asciinema", {"min_version": "2.0.1"}),)
INSTALL_USERVOICE = (("uservoice", {"min_version": "0.0.23"}),)
INSTALL_DISCOURSE = (("pycryptodome", {"min_version": "3.7.2"}),)

INSTALL_ALL = (
    INSTALL_REQUIRES + INSTALL_USERVOICE + INSTALL_DISCOURSE + INSTALL_ASCIINEMA
)
