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
import requests
import json


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

    headers = { "Content-Type": "multipart/form-data;"}

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
