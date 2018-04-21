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
from .auth import ( auth_flow )

from .headers import (
    basic_auth_header,
    get_headers,
    reset_headers,
    update_headers
)

from .http import ( 
    call, delete, download, get, head, healthy, 
    paginate_get, post, put, stream, 
    stream_response
)

from .settings import (
    get_setting,
    get_settings,
    get_and_update_setting,
    load_config
)

import os
import sys


class HelperBase(object):

    def __init__(self, name=None):
 
        self.name = 'github' or name
        self._load_config()
        self.load_secrets()

    def load_secrets(self):
        '''the subclass helper should implement this function to load 
           environment variables, etc. from the user.
        '''
        pass


# Actions

    def run(self):
        '''run the entire helper procedure, including:

             - start: initialize the helper, collection preferences
             - record: record any relevant features for the environment / session
             - interact: interact with the user for additional informatoin
             - submit: submit the completed request
 
             Each of the above functions for a helper can determine global
             collection preferences from the system helpme.cfg in the module
             root. After performing global actions, each function then calls
             a class specific function of the same name (e.g., start calls
             _start) that is implemented by the helper class to do custom
             operations for the helper.

             

        '''

    def start(self):
        '''start the helper flow. We check helper system configurations to
           determine components that should be collected for the submission.
        '''
        self.speak()
        self._start()

    def submit(self):
        '''submit is the final call to submit the helper request'''
        bot.info('[submit|%s]' %(self.name))
        self._submit()


# identification

    def speak(self):
        '''
           a function for the helper to announce him or herself, depending
           on the level specified. If you want your client to have additional
           announced things here, then implement the class `_speak` for your
           client.

        '''
        if self.quiet is False:
            bot.info('[helper|%s]' %(self.name))
            self._speak()


    def _speak(self):
        '''this function should be subclassed if the helper has additional
           information to give the user.
        '''
        pass


    def __repr__(self):
        return "[helper|%s]" %self.name

    def __str__(self):
        return "[helper|%s]" %self.name


# Settings
HelperBase._load_config = load_config
HelperBase._get_setting = get_setting
HelperBase._get_settings = get_settings
HelperBase._get_and_update_setting = get_and_update_setting

# Metadata
#ApiConnection.get_metadata = get_metadata

# Auth
#ApiConnection.require_secrets = require_secrets
#ApiConnection._auth_flow = auth_flow

# Http and Requests
#ApiConnection._call = call
#ApiConnection._delete = delete
#ApiConnection.download = download
#ApiConnection._get = get
#ApiConnection._head = head
#ApiConnection._healthy = healthy
#ApiConnection._paginate_get = paginate_get
#ApiConnection._post = post
#ApiConnection._put = put
#ApiConnection.stream = stream
#ApiConnection._stream = stream_response
#ApiConnection._verify = verify
