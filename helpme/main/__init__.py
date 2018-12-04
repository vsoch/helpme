'''

Copyright (C) 2017-2018 Vanessa Sochat.

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

from .base import HelperBase


def get_helper(name=None, quiet=True, **kwargs):
    '''
       get the correct helper depending on the environment variable
       HELPME_CLIENT

       quiet: if True, suppress most output about the client (e.g. speak)

    '''
    # Second priority, from environment
    from helpme.defaults import HELPME_CLIENT

    # First priority, from command line
    if name is not None:
        HELPME_CLIENT = name

    # If no obvious credential provided, we can use HELPME_CLIENT
    if   HELPME_CLIENT == 'github': from .github import Helper;
    elif HELPME_CLIENT == 'uservoice': from .uservoice import Helper
    elif HELPME_CLIENT == 'discourse': from .discourse import Helper
    else: from .github import Helper

    Helper.name = HELPME_CLIENT
    Helper.quiet = quiet

    # Initialize the database
    return Helper()

Helper = get_helper()
