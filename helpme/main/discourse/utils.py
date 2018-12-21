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
import uuid
from requests import Session, Request
import requests
import json


enter_input = getattr(__builtins__, 'raw_input', input)

def request_token(board, client_id):
    '''send a public key to request a token

       board: the discourse board to post to
    '''
    nonce = str(uuid.uuid4())

    data = {'scopes': 'write',
            'client_id': client_id,
            'application_name': 'HelpMe',
            'public_key': self.keypub,
            'nonce': nonce }

    # Put together url to open for user
    session = Session()
    prompt = Request('GET', "%s/user-api-key/new" % board, params=data).prepare()
    bot.newline()
    bot.info('Open browser to:')
    bot.info(prompt.url)
    bot.newline()
   
    # the user will open browser, get a token, and then have it saved here.
    bot.info('Copy paste token:')

    lines = []

    # The token is multi line, so collect until user presses enter (empty line)
    while True:
        line = enter_input().strip()
        if line:
            lines.append(line)
        else:
            break

    token = '\n'.join(lines)
    return token


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
    data = {'api_key': self.token, 
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
