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
import sys


def auth_flow(self, url):
    '''auth flow is a function to present the user with a url to retrieve
       some token/code, and then copy paste it back in the terminal.

        Parameters
        ==========
        url should be a url that is generated for the user to go to and accept
        getting a credential in the browser.
    
    '''
    print('Please go to this URL and login: {0}'.format(url))
    get_input = getattr(__builtins__, 'raw_input', input)
    message = 'Please enter the code you get after login here: '
    code = get_input(message).strip()
    return code
