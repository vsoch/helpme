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

from helpme.logger import RobotNamer
from helpme.logger import bot
import sys
from requests import Session, Request
import requests
import json


def request_token(board):
    '''send a public key to request a token

       board: the discourse board to post to
    '''
    # Generate client id and load public key
    client_id = 'helpme-%s' % RobotNamer().generate()
    client_id = self._get_and_update_setting('DISCOURSE_CLIENT_ID', client_id)

    pubkey = str(self.keypub).strip('\n')

    data = {'scopes': 'write',
            'client_id': client_id,
            'application_name': 'helpme',
            'public_key': pubkey,
            'nonce': '666401a65ea121858be20f0925524453',
            'auth_redirect':  "%s/user-api-key" % board }

    # Put together url to open for user
    session = Session()
    prompt = Request('GET', "%s/user-api-key/new" % board, params=data).prepare()
    bot.newline()
    bot.info('Open browser to:')
    bot.info(prompt.url)
    bot.newline()
   
    #TODO: the user will open browser, get a token, and then have it saved here.

#So, the URL you need to go to you be this: 
#https://stage.neurostars.org/user-api-key/new?scopes=write&client_id=areallysecureid&auth_redirect=https%3A%2F%2Fstage.neurostars.org%2Fuser-api-key&application_name=helpme&public_key=-----BEGIN+PUBLIC+KEY-----%0AMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDh7BS7Ey8hfbNhlNAW%2F47pqT7w%0AIhBz3UyBYzin8JurEQ2pY9jWWlY8CH147KyIZf1fpcsi7ZNxGHeDhVsbtUKZxnFV%0Ap16Op3CHLJnnJKKBMNdXMy0yDfCAHZtqxeBOTcCo1Vt%2FbHpIgiK5kmaekyXIaD0n%0Aw0z%2FBYpOgZ8QwnI5ZwIDAQAB%0A-----END+PUBLIC+KEY-----%0A&nonce=666401a65ea121858be20f0925524453

def create_post(title, body, board, category, username, token):
    '''create a Discourse post, given a title, body, board, and token.

       Parameters
       ==========
       title: the issue title
       body: the issue body
       board: the discourse board to post to
       token: the user's personal (or global) discourse token

    '''
    category_url = "%s/categories.json" % board
    response = requests.get(category_url)

    if response.status_code != 200:
        print('Error with retrieving %s' % category_url)
        sys.exit(1)

    # Get a list of all categories
    categories = response.json()['category_list']['categories']
    categories = {c['name']:c['id'] for c in categories}

    # And if not valid, warn the user
    if category not in categories:
        bot.warning('%s is not valid, will use default' % category)

    category_id = categories.get(category, None)

    headers = {"Content-Type": "multipart/form-data;"}

    # First get the category ids
    data = {'api_key': token, 
            'api_username': username,
            'title': title,
            'raw': body,
            'category': category_id}

    response = requests.post("%s/posts.json" % board,
                             headers=headers,
                             data=data)


    if response.status_code in [200, 201, 202]:
        topic = response.json()
        url = "%s/t/%s/%s" %(board, topic['topic_slug'], topic['id'])
        bot.info(url)
        return url

    elif response.status_code == 404:
        bot.error('Cannot post to board, not found. Do you have permission?')
        sys.exit(1)

    else:
        bot.error('Cannot post to board %s' % board)
        bot.error(response.content)
        sys.exit(1)
