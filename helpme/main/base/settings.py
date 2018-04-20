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


from helpme.utils import (
    get_installdir
    mkdir_p,
    read_json,
    write_json
)
import configparser
import json
import os
import re
import sys


def get_configfile():
    '''return the full path to the configuration file
    '''
    return os.path.abspath(os.path.join(get_installdir(), 'helpme.cfg'))


def load_config(name):
    '''load config should load the global helpme configuration, and update
       with user configurations from $HOME/helpme.cfg
    '''
    print('WRITEME')


def update_client_secrets(helper, updates, secrets=None, save=True):
    '''update client secrets will update the data structure for a particular
       authentication. This should only be used for a (quasi permanent) token
       or similar. The secrets file, if found, is updated and saved by default.
    '''
    if secrets is None:
        secrets = read_client_secrets()
    if helper not in secrets:
        secrets[helper] = {}
    secrets[helper].update(updates)

    # The update typically includes a save

    if save is True:
        secrets_file = _get_secrets_file()
        if secrets_file is not None:
            write_json(secrets, secrets_file)

    return secrets


def read_client_secrets():
    '''If no secrets are found, we use default github helper
    '''
    secrets = get_secrets_file()
    if secrets is not None:
        client_secrets = read_json(secrets)

    return client_secrets


def get_secrets_file():
    '''Sniff the environment and standard location for client
       secrets file. Otherwise, return None
    '''
    from helpme.defaults import HELPME_CLIENT_SECRETS
    if os.path.exists(HELPME_CLIENT_SECRETS):
        return HELPME_CLIENT_SECRETS



# Secrets and Settings


def get_settings(self, client_name=None):
    '''get all settings, either for a particular client if a name is provided,
       or across clients.

       Parameters
       ==========
       client_name: the client name to return settings for (optional)

    '''
    settings = read_client_secrets()
    if client_name is not None and client_name in settings:
        return settings[client_name]           
    return settings


def get_setting(self, name, default=None):
    '''return a setting from the environment (first priority) and then
       secrets (second priority) if one can be found. If not, return None.

       Parameters
       ==========
       name: they key (index) of the setting to look up
       default: (optional) if not found, return default instead.
    ''' 

    # First priority is the environment
    setting = os.environ.get(name)

    # Second priority is the secrets file
    if setting is None:
        secrets = read_client_secrets()
        if self.client_name in secrets:
            secrets = secrets[self.client_name]
            if name in secrets:
                setting = secrets[name]

    if setting is None and default is not None:
        setting = default
    return setting


def get_and_update_setting(self, name, default=None):
    '''Look for a setting in the environment (first priority) and then
       the settings file (second). If something is found, the settings
       file is updated. The order of operations works as follows:

       1. The user config file is used as a cache for the variable
       2. the environment variable always takes priority to cache, and if
          found, will update the cache.
       3. If the variable is not found and the cache is set, we are good
       5. If the variable is not found and the cache isn't set, return
          default (default is None)

       So the user of the function can assume a return of None equates to
       not set anywhere, and take the appropriate action.
    ''' 

    setting = self._get_setting(name)

    if setting is None and default is not None:
        setting = default

    # If the setting is found, update the client secrets
    if setting is not None:
        updates = {name : setting}
        update_client_secrets(backend=self.client_name, 
                              updates=updates)

    return setting


def update_setting(self, name, value):
    '''Just update a setting, doesn't need to be returned.
    ''' 

    if value is not None:
        updates = {name : value}
        update_client_secrets(backend=self.client_name, 
                              updates=updates)
