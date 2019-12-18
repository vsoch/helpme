"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.logger import bot
import os
import re


def upload_asciinema(filename):
    """a wrapper around generation of an asciinema.api.Api to call the 
       upload command given an already existing asciinema file. 

       Parameters
       ==========
       filename: the asciinema file to upload, can be generated with 
                 function record_asciinema in record.py

    """
    if os.path.exists(filename):

        try:
            from asciinema.commands.upload import UploadCommand
            import asciinema.config as aconfig
            from asciinema.api import Api
        except:
            bot.exit(
                "The asciinema module is required to submit "
                "an asciinema recording. Try pip install helpme[asciinema]"
            )

        # Load the API class

        cfg = aconfig.load()
        api = Api(cfg.api_url, os.environ.get("USER"), cfg.install_id)

        # Perform the upload, return the url

        uploader = UploadCommand(api, filename)

        try:
            url, warn = uploader.api.upload_asciicast(filename)
            if warn:
                uploader.print_warning(warn)

            # Extract just the url, if provided (always is https)
            if url:
                match = re.search("https://.+", url)
                if match:
                    url = match.group()
            return url

        except:
            bot.error("Problem with upload, skipping")

    else:
        bot.warning("Cannot find %s, skipping submission." % filename)
