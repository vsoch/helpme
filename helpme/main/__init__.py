"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .base import HelperBase


def get_helper(name=None, quiet=True, **kwargs):
    """
       get the correct helper depending on the environment variable
       HELPME_CLIENT

       quiet: if True, suppress most output about the client (e.g. speak)

    """
    # Second priority, from environment
    from helpme.defaults import HELPME_CLIENT

    # First priority, from command line
    if name is not None:
        HELPME_CLIENT = name

    # If no obvious credential provided, we can use HELPME_CLIENT
    if HELPME_CLIENT == "github":
        from .github import Helper
    elif HELPME_CLIENT == "uservoice":
        from .uservoice import Helper
    elif HELPME_CLIENT == "discourse":
        from .discourse import Helper
    else:
        from .github import Helper

    Helper.name = HELPME_CLIENT
    Helper.quiet = quiet

    # Initialize the database
    return Helper(**kwargs)
