"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from asciinema.commands.record import RecordCommand
from asciinema.commands.command import Command
import asciinema.asciicast.v2 as v2
import asciinema.asciicast.raw as raw
import tempfile
import os

# Create subclass of RecordCommand to pass in arguments


class HelpMeRecord(RecordCommand):
    def __init__(
        self,
        api,
        filename=None,
        quiet=False,
        env=None,
        env_whitelist="",
        record_stdin=False,
        command=None,
        title="HelpMe Recording",
        append=False,
        overwrite=False,
        record_raw=False,
    ):

        # If no custom file selected, create for user
        if filename is None:
            filename = self.generate_temporary_file()

        Command.__init__(self, quiet=quiet)
        self.api = api
        self.filename = filename
        self.rec_stdin = record_stdin
        self.command = command or os.environ["SHELL"]
        self.env_whitelist = ""
        self.title = title
        self.assume_yes = quiet
        self.idle_time_limit = 10
        self.append = append
        self.overwrite = overwrite
        self.raw = record_raw
        self.recorder = raw.Recorder() if record_raw else v2.Recorder()
        self.env = env if env is not None else os.environ

    def generate_temporary_file(self, folder="/tmp", prefix="helpme", ext="json"):

        """write a temporary file, in base directory with a particular extension.
      
           Parameters
           ==========
           folder: the base directory to write in. 
           prefix: the prefix to use
           ext: the extension to use.

        """
        tmp = next(tempfile._get_candidate_names())
        return "%s/%s.%s.%s" % (folder, prefix, tmp, ext)


def record_asciinema():
    """a wrapper around generation of an asciinema.api.Api and a custom 
       recorder to pull out the input arguments to the Record from argparse.
       The function generates a filename in advance and a return code
       so we can check the final status. 
    """

    import asciinema.config as aconfig
    from asciinema.api import Api

    # Load the API class

    cfg = aconfig.load()
    api = Api(cfg.api_url, os.environ.get("USER"), cfg.install_id)

    # Create dummy class to pass in as args
    recorder = HelpMeRecord(api)
    code = recorder.execute()

    if code == 0 and os.path.exists(recorder.filename):
        return recorder.filename
    print("Problem generating %s, return code %s" % (recorder.filename, code))
