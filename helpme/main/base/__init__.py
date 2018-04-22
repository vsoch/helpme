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
from helpme.utils import ( confirm_prompt, regexp_prompt )
from helpme.action import record_asciinema

from configparser import NoOptionError

from .settings import (
    get_setting,
    get_settings,
    get_and_update_setting,
    load_config,
    load_config_user,
    update_settings
)

import os
import sys


class HelperBase(object):

    def __init__(self, name=None, **kwargs):
        '''the helper base loads configuration files for the user (in $HOME)
           and module, and then stores any arguments given from the caller

           Parameters
           ==========
           name: the helper name, defaults to github
           kwargs: should include command line arguments from the client.

        '''

        self.name = 'github' or name
        self.config = self._load_config()
        self.config_user = self._load_config_user()
        self.load_secrets()

        # Data and variables collected from the user
        self.data = kwargs or dict()

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

        # Step 1: get config steps
        steps = self.config._sections[self.name]

        # Step 2: Start the helper (announce and run start, which is init code)
        self.start()

        # Step 3: Iterate through flow, check each step for known record/prompt,
        #         and collect outputs appropriately

        for step, content in steps.items():
            self.collect(step, content)
        
        # Step 4: When data collected, pass data structures to submit
        self.submit()


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

    def _submit(self):
        '''if this function is called, it indicates the helper submodule
           doesn't have a submit function, so no submission is done.
        '''
        bot.error('_submit() not implemented in helper %s.' %self.name)
        sys.exit(1)

# Collectors


    def collect(self, step, content):
        '''given a name of a configuration key and the provided content, collect
           the required metadata from the user.
 
           Parameters
           ==========
           step: the key in the configuration. Can be one of:
                   user_message_<name>
                   runtime_arg_<name>
                   record_asciinema
                   record_environment
                   user_prompt_<name>
           content: the default value or boolean to indicate doing the step.
        '''

        # Option 1: The step is just a message to print to the user
        if step.startswith('user_message'):
            print(content)   
     
        # Option 2: The step is to collect a user prompt (if not at runtime)
        elif step.startswith('user_prompt'):
            self.collect_argument(step, content)

        # Option 3: The step is to record an asciinema!
        elif step == 'record_asciinema':
            self.record_asciinema()

        # Option 4: Record the user environment
        elif step == "record_environment":
            self.record_environment()

        bot.debug(self.data)

    def collect_argument(self, step, message):
        '''given a key in the configuration, collect the runtime argument if
           provided. Otherwise, prompt the user for the value.

           Parameters
           ==========
           step: the name of the step, should be 'runtime_arg_<name>'
           message: the content of the step, the message to show the user if the
                    argument <name> is not found under args.

        '''
        print(step)
        print(message)
        argname = step.replace('user_prompt_', '')
        if argname not in self.data:
            self.data[argname] = regexp_prompt(message)


# Recorders

    def record_environment(self):
        '''collect a limited set of environment variables based on the list
           under record_envirionment in the configuration file.
        '''

        # whitelist is a newline separated list under record_environment

        envars = self._get_setting('whitelist', 'record_environment')

        if envars is not None:
        
            envars = envars.split('\n')

            # Make transparent for the user

            print('Capturing subset of whitelisted environment:')
            bot.info('|'.join(envars))

            # Iterate through and collect based on name

            keep = [(k,v) for k,v in os.environ.items() if k.lower() in envars]

            # Ask the user for permission

            if confirm_prompt('Is this list ok?'):
                self.data['record_environment'] = keep


    def record_asciinema(self):
        '''record an asciinema from the user session, saving the file to
           a temporary file and showing the user so if he/she needs to do it
           again, the file can be provided. The flow of events below makes
           the following checks:

           1. The user confirms it is ok to record
           2. The record_asciinema setting is present and True in the config
           3. An asciinema file path has not been provided by the user

        '''

        if confirm_prompt("Would you like to send a terminal recording?"):

            # The config has a confirmatory value

            try:
                record = self.config.getboolean(self.name, 'record_asciinema')
            except  from NoOptionError:
                record = False

            # The user provided a file, and it exists
            if "asciinema" in self.data:
                if os.path.exists(self.data['asciinema']):
                    record = False
                    
            if record is True:
                self.data['asciiname'] = record_asciinema()

            message = '''recorded! File at %s. If you need to run helpme again
                         you can supply the path to this file with the 
                         --asciinema flag''' %filename

            bot.custom(prefix="Asciinema ", message=message, color="CYAN")



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
HelperBase._load_config_user = load_config_user
HelperBase._get_setting = get_setting
HelperBase._get_settings = get_settings
HelperBase._get_and_update_setting = get_and_update_setting
HelperBase._update_settings = update_settings
