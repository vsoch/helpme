'''

Copyright (C) 2018-2019 Vanessa Sochat.

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
from helpme.action import ( record_asciinema, upload_asciinema )
from helpme.utils import ( 
    envars_to_markdown, 
    generate_keypair, 
    load_keypair
)
from helpme.logger import bot
from .utils import( create_post, request_token )
import os
import sys

class Helper(HelperBase):

    def __init__(self, **kwargs):
 
        self.name = "discourse"

        # Discourse needs a keypair, generate if not found, before token
        self._generate_keys()
        super(Helper, self).__init__(**kwargs)

    def load_secrets(self):
        self.token = self._get_and_update_setting('HELPME_DISCOURSE_TOKEN')

        # Generate client id with application name and version, if not provided
        cid = 'helpme-%s' % self._version
        env = 'HELPME_DISCOURSE_CLIENT_ID'
        self.client_id = self._get_and_update_setting(env, cid)

        # Load additional parameters for board category and name
        self._update_envars()

    def _update_envars(self):
        '''load additional variables from the environment, including a board
           and a category. If not set, we will then look at positionals for
           the board. If not set after positions, we prompt the user.
        '''
                  # Environment variable     # config setting under discourse
        items = [('HELPME_DISCOURSE_BOARD', 'user_prompt_board'),
                 ('HELPME_DISCOURSE_CATEGORY', 'user_prompt_category'),
                 ('HELPME_DISCOURSE_USERNAME', 'user_prompt_username')]

        self._load_envars(items)
        
    def check_env(self, envar, value):
        '''ensure that variable envar is set to some value, 
           otherwise exit on error.
        
           Parameters
           ==========
           envar: the environment variable name
           value: the setting that shouldn't be None
        '''
        if value is None:
            bot.error('You must export %s to use Discourse' % envar)
            print('https://vsoch.github.io/helpme/helper-discourse')
            sys.exit(1)


    def _generate_keys(self):
        '''the discourse API requires the interactions to be signed, so we 
           generate a keypair on behalf of the user
        '''
        from helpme.defaults import HELPME_CLIENT_SECRETS
        keypair_dir = os.path.join(os.path.dirname(HELPME_CLIENT_SECRETS),
                                   'discourse')

        # Have we generated a keypair file before?
        self.keypair_file = os.path.join(keypair_dir, 'private.pem')

        # We likely won't have generated it on first use!
        if not hasattr(self, 'key'):
            self.key = generate_keypair(self.keypair_file)           

        # If we generated the keypair file, we will have already loaded the key
        if not hasattr(self, 'public_key'):
            self.public_key = load_keypair(self.keypair_file)


    def _start(self, positionals):

        # If the user provides a discourse board, use it.

        if positionals:

            # Let's enforce https. If the user wants http, they can specify it
            board = positionals.pop(0)
            if not board.startswith('http'):
                board = 'https://%s' % board

            self.data['user_prompt_board'] = board
            self.config.remove_option('discourse','user_prompt_board')

            # If the user provides another argument, it's the category
            if len(positionals) > 0:
                category = positionals.pop(0)
                self.data['user_prompt_category'] = category
                self.config.remove_option('discourse','user_prompt_category')
             

    def _submit(self):
        '''submit the question to the board. When we get here we should have 
           (under self.data)
           
                {'record_environment': [('DISPLAY', ':0')],
                 'user_prompt_board': 'http://127.0.0.1',
                 'user_prompt_issue': 'I want to know why dinosaurs are so great!',
                 'user_prompt_title': 'Why are dinosaurs so great?'}

           self.token should be propogated with the personal access token
        ''' 
        body = self.data['user_prompt_issue']
        title = self.data['user_prompt_title']
        board = self.data['user_prompt_board']
        username = self.data['user_prompt_username']
        category = self.data['user_prompt_category']

        # Step 1: Token
        if self.token == None:
            self.token = self.request_token(board)
            self._get_and_update_setting('HELPME_DISCOURSE_TOKEN', self.token)

        # Step 1: Environment

        envars = self.data.get('record_environment')        
        body = body + envars_to_markdown(envars)

        # Step 2: Asciinema

        asciinema = self.data.get('record_asciinema')
        if asciinema not in [None, '']:
            url = upload_asciinema(asciinema)

            # If the upload is successful, add a link to it.

            if url is not None:
                body += "\n[View Asciinema Recording](%s)" % url
 
        # Add other metadata about client

        body += "\n\ngenerated by [HelpMe](https://vsoch.github.io/helpme/)"
        body += "\nHelpMe Discourse Id: %s" %(self.run_id)

        # Submit the issue

        post = self.create_post(title, body, board, category, username)
        return post


Helper.request_token = request_token
Helper.create_post = create_post
