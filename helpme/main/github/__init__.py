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

from helpme.main import HelperBase
from helpme.action import record_asciinema
from helpme.logger import bot
import os
import sys

class Helper(HelperBase):

    def __init__(self, **kwargs):
 
        self.name = "github"
        super(Helper, self).__init__(**kwargs)

    def load_secrets(self):
        self.token = self._get_and_update_setting('HELPME_GITHUB_TOKEN')

        if self.token is None:
            bot.error('You must export HELPME_GITHUB_TOKEN to use Github')
            print('https://researchapps.github.io/helpme/helper-github')
            sys.exit(1)

    def _start(self):
        print('Start the helper flow.')

    def _submit(self):
        print('Submit the Helper flow....')

