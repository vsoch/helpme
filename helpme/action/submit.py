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

from asciinema.commands.upload import UploadCommand
import os

def upload_asciinema(filename):
    '''a wrapper around generation of an asciinema.api.Api to call the 
       upload command given an already existing asciinema file. 

       Parameters
       ==========
       filename: the asciinema file to upload, can be generated with 
                 function record_asciinema in record.py

    '''
    if os.path.exists(filename):

        import asciinema.config as aconfig
        from asciinema.api import Api

        # Load the API class

        cfg = aconfig.load()
        api = Api(cfg.api_url, os.environ.get("USER"), cfg.install_id)

        # Perform the upload, return the url

        uploader = UploadCommand(api, filename)
    
        try:
            url, warn = uploader.api.upload_asciicast(filename)
            if warn:
                uploader.print_warning(warn)
            return url

        except:
            bot.error('Problem with upload, skipping')

    else:
        bot.warning('Cannot find %s, skipping submission.' %filename)
