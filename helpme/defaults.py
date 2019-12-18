"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.utils import get_userhome
import tempfile
import os
import sys


################################################################################
# environment / options
################################################################################


def convert2boolean(arg):
    """
    convert2boolean is used for environmental variables
    that must be returned as boolean
    """
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


def getenv(variable_key, default=None, required=False, silent=True):
    """
    getenv will attempt to get an environment variable. If the variable
    is not found, None is returned.

    :param variable_key: the variable name
    :param required: exit with error if not found
    :param silent: Do not print debugging information for variable
    """
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." % variable_key)
        sys.exit(1)

    if not silent and variable is not None:
        bot.verbose("%s found as %s" % (variable_key, variable))

    return variable


################################################################################
# Helpme

USERHOME = get_userhome()
HELPME_CLIENT = getenv("HELPME_CLIENT", "github")
HELPME_WORKERS = int(getenv("HELPME_PYTHON_THREADS", 9))

# The configuration directory can hold the default config, along with keys
_config = os.path.join(USERHOME, ".helpme")
HELPME_CONFIG_DIR = getenv("HELPME_CONFIG_DIR", _config)

_secrets = os.path.join(HELPME_CONFIG_DIR, "helpme.cfg")
HELPME_CLIENT_SECRETS = getenv("HELPME_CLIENT_SECRETS", _secrets)
HELPME_HELPERS = ["github", "uservoice", "discourse"]
