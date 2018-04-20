'''

This is a base client that imports functions depending on the API it is 
    using. Currently, it supports github and uservoice

Copyright (C) 2017-2018 Vanessa Sochat.
Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.

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


def get_client(quiet=False, **kwargs):
    '''
       get the correct client depending on the helper of interest. The
       selected client can be chosen based on the environment variable
       HELPME_CLIENT, 

       quiet: if True, suppress most output about the client (e.g. speak)

    '''
    from sregistry.defaults import SREGISTRY_CLIENT

    # If no obvious credential provided, we can use SREGISTRY_CLIENT
    if   SREGISTRY_CLIENT == 'github': from .github import Client
    elif SREGISTRY_CLIENT == 'uservoice': from .uservoice import Client
    else: from .github import Client

    Client.name = SREGISTRY_CLIENT
    Client.quiet = quiet

    # Create credentials cache, if it doesn't exist
    Client._credential_cache = get_credential_cache()

    from helpme.main import ( record, config )
    Client.add = add
    Client._init_db = init_db        

    # Initialize the database
    cli = Client()

    if hasattr(Client, '_init_db'):
        cli._init_db(SREGISTRY_DATABASE)
    return cli

Client = get_client()
