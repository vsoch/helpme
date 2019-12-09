"""

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

"""

from helpme.logger import RobotNamer, bot
from helpme.utils import get_installdir, mkdir_p, read_config, write_config
import configparser
import json
import os
import re
import sys


# Config File (User and System) ################################################


def get_configfile():
    """return the full path to the configuration file
    """
    return os.path.abspath(os.path.join(get_installdir(), "helpme.cfg"))


def get_configfile_user():
    """return the full path for the user configuration file. If doesn't
       exist, create it for the user.
    """
    from helpme.defaults import HELPME_CLIENT_SECRETS

    # The inital file has a funny username

    if not os.path.exists(HELPME_CLIENT_SECRETS):
        bot.debug("Generating settings file at %s" % HELPME_CLIENT_SECRETS)
        config_dir = os.path.dirname(HELPME_CLIENT_SECRETS)

        # The configuration directory might be needed for different clients
        if not os.path.exists(config_dir):
            mkdir_p(config_dir)

        name = RobotNamer().generate()

        # Generate the user config

        config = configparser.ConfigParser()
        config["DEFAULT"] = {"Alias": name}
        write_config(HELPME_CLIENT_SECRETS, config)

    return HELPME_CLIENT_SECRETS


def load_config_user(self):
    """Get and load the file. This function is the primary point of interaction
       between the get_configfile_user and various get/set settings functions.
    """
    configfile = get_configfile_user()
    return _load_config(configfile)


def load_config(self):
    """load config should load the global helpme configuration, and update
       with user configurations from $HOME/helpme.cfg
    """
    configfile = get_configfile()
    return _load_config(configfile)


def _remove_setting(section, name, configfile, save=False):
    """remove a setting from the global config
    """
    removed = False
    config = _load_config(configfile)
    if section in config:
        if name.lower() in config[section]:
            removed = config.remove_option(section, name)

    # Does the user want to save the file?
    if removed and save:
        write_config(configfile, config)

    return removed


def remove_setting(self, section, name, save=False):
    """remove a setting from the global config
    """
    configfile = get_configfile()
    return _remove_setting(section, name, configfile, save)


def remove_user_setting(self, section, name, save=False):
    """remove a setting from the user config
    """
    configfile = get_configfile_user()
    return _remove_setting(section, name, configfile, save)


def _load_config(configfile, section=None):
    """general function to load and return a configuration given a helper
       name. This function is used for both the user config and global help me
       config files.
    """
    if os.path.exists(configfile):
        config = read_config(configfile)
        if section is not None:
            if section in config:
                return config._sections[section]
            else:
                bot.warning("%s not found in %s" % (section, configfile))
        return config


# Environment ##################################################################


def load_envars(self, items):
    """load a tuple of environment variables, to add to the user settings
    
        Example:
 
        items = [('HELPME_DISCOURSE_BOARD', 'user_prompt_board'),
                 ('HELPME_DISCOURSE_CATEGORY', 'user_prompt_category')]

        # Note that it's added to the client with an underscore:
        self._load_envars()
    """
    for item in items:
        envar = item[0]
        key = item[1]
        value = self._get_and_update_setting(envar)

        if value != None:
            self.data[key] = value
            self.config.remove_option(self.name, key)


# Get and Update ###############################################################


def get_setting(self, name, section=None, default=None, user=True):
    """return a setting from the environment (first priority) and then
       secrets (second priority) if one can be found. If not, return None.

       Parameters
       ==========
       section: the section in the config, defaults to self.name
       name: they key (index) of the setting to look up
       default: (optional) if not found, return default instead.
       user: if True, load from user config. Otherwise, main config

    """
    loader = self._load_config_user
    if not user:
        loader = self._load_config

    if section is None:
        section = self.name

    # First priority is the environment

    setting = os.environ.get(name)

    # Second priority is the secrets file

    if setting is None:

        # Loads user config on level of helper (already indexed)
        config = loader()
        if section in config:
            if name.lower() in config[section]:
                setting = config[section][name.lower()]

    # Third priority, return a default

    if setting is None and default is not None:
        setting = default

    return setting


def get_settings(self):
    """get all settings for a client, if defined in config.
    """
    config = self._load_config_user()
    if self.name in config:
        return config[self.name]


def update_settings(self, updates, config=None):
    """update client secrets will update the data structure for a particular
       authentication. This should only be used for a (quasi permanent) token
       or similar. The secrets file, if found, is updated and saved by default.

       Parameters
       ==========
       helper: the name of the helper to look up in the config
       updates: a dictionary of key:value pairs to add to the config
       config: a configparser.ConfigParser(), if already loaded

    """
    if config is None:
        config = self._load_config_user()

    if self.name not in config:
        config[self.name] = {}

    config[self.name].update(updates)

    # Update the saved file

    configfile = get_configfile_user()
    write_config(configfile, config)
    return config


def get_and_update_setting(self, name, default=None, user=True):
    """Look for a setting in the environment (first priority) and then
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
    """

    setting = self._get_setting(name, user=user)

    if setting is None and default is not None:
        setting = default

    # If the setting is found, update the client secrets
    if setting is not None:
        updates = {name: setting}
        self._update_settings(updates)

    return setting
