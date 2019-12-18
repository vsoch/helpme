"""

Copyright (C) 2017-2020 Vanessa Sochat.

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

from helpme.main import HelperBase
from helpme.action import record_asciinema, upload_asciinema
from helpme.logger import bot, RobotNamer
from helpme.utils import envars_to_markdown, format_code_block, generate_identifier_hash
from .utils import create_issue, open_issue
import os
import re
import sys


class Helper(HelperBase):
    def __init__(self, **kwargs):

        self.name = "github"
        super(Helper, self).__init__(**kwargs)

    def load_secrets(self):
        self.token = self._get_and_update_setting("HELPME_GITHUB_TOKEN")

        # If the user wants to use a token for the GitHub API
        if not self.token:
            bot.warning(
                "HELPME_GITHUB_TOKEN not found, "
                "will attempt to open browser manually "
                "If you have trouble submitting an issue, export it."
            )

    def check_env(self, envar, value):
        """ensure that variable envar is set to some value, 
           otherwise exit on error.
        
           Parameters
           ==========
           envar: the environment variable name
           value: the setting that shouldn't be None
        """
        if value is None:
            bot.error("You must export %s to use Github" % envar)
            print("https://vsoch.github.io/helpme/helper-github")
            sys.exit(1)

    def run_headless(self, repo, title, body, identifier=None):
        """run a headless helper procedure, meaning that the title, body,
           and other content must be provided to the function. Command line
           arguments such a a GitHub repository or discourse board must 
           also be provided.

           Parameters
           ==========
           repo: the repository (full name) to submit to
           title: the title of the issue to open
           body: additional content for the body of the request
           identifier: if provided, generate hash based on identifier
        """
        self.run_id = RobotNamer().generate()
        self.data["user_prompt_repo"] = repo
        self.config.remove_option("github", "user_prompt_repo")

        # Update config with other user provided variables
        self.data["user_prompt_issue"] = body
        self.data["user_prompt_title"] = title

        # If the identifier is provided, add to data.
        if identifier is not None:
            self.data["md5"] = generate_identifier_hash(identifier)
            self.data["md5_source"] = identifier

        # We can only run steps that don't require user interaction
        skip = "^(%s)" % "|".join(["record_asciinema", "user_"])
        for step, content in self.steps:
            if not re.search(skip, step):
                self.collect(step, content)

        self.submit()

    def _start(self, positionals):
        """If the user provides a repository name, use it
        """
        if positionals:
            self.data["user_prompt_repo"] = positionals[0]
            self.config.remove_option("github", "user_prompt_repo")

    def _submit(self):
        """submit the issue to github. When we get here we should have:
           
           {'user_prompt_issue': 'I want to do the thing.', 
            'user_prompt_repo': 'vsoch/hello-world', 
            'user_prompt_title': 'Error with this thing',
            'record_asciinema': '/tmp/helpme.93o__nt5.json',
            'record_environment': ((1,1),(2,2)...(N,N))}

           self.token should be propogated with the personal access token,
           or None if one was not provided.
        """
        body = self.data["user_prompt_issue"]
        title = self.data["user_prompt_title"]
        repo = self.data["user_prompt_repo"]

        # Step 1: Environment and System

        envars = self.data.get("record_environment", [])
        system = self.data.get("record_system")
        body = body + envars_to_markdown(envars)

        if system is not None:
            body = body + "## System\n %s" % format_code_block(system)

        # Step 2: Identifier

        identifier = self.data.get("md5", self.run_id)

        # Step 3: Asciinema

        asciinema = self.data.get("record_asciinema")
        if asciinema not in [None, ""]:
            url = upload_asciinema(asciinema)

            # If the upload is successful, add a link to it.

            if url is not None:
                body += "\n[View Asciinema Recording](%s)" % url

        # Add other metadata about client

        body += "\n\ngenerated by [HelpMe](https://vsoch.github.io/helpme/)"
        body += "\nHelpMe Github Issue: %s" % (identifier)

        # Submit the issue

        if self.token is not None:
            issue = create_issue(title, body, repo, self.token)
        else:
            issue = open_issue(title, body, repo)
        return issue
