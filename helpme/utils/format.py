"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


from helpme.logger import bot

import hashlib
import os
import sys
import re


# Markdown formatting


def envars_to_markdown(envars, title="Environment"):
    """generate a markdown list of a list of environment variable tuples

       Parameters
       ==========
       title: A title for the section (defaults to "Environment"
       envars: a list of tuples for the environment, e.g.:

            [('TERM', 'xterm-256color'),
             ('SHELL', '/bin/bash'),
             ('USER', 'vanessa'),
             ('LD_LIBRARY_PATH', ':/usr/local/pulse')]

    """
    markdown = ""
    if envars not in [None, "", []]:
        markdown += "\n## %s\n" % title
        for envar in envars:
            markdown += " - **%s**: %s\n" % (envar[0], envar[1])
    return markdown


def format_code_block(code, language="python"):
    """format a chunk of code (usually a dictionary) into a code block.
    """
    return """```%s
%s
```""" % (
        language,
        code,
    )


## Identifier hashes


def generate_identifier_hash(identifier):
    """generate a unique identifier (hash) for the issue"""
    hash_object = hashlib.md5(identifier.encode("utf-8"))
    return "md5.%s" % hash_object.hexdigest()
