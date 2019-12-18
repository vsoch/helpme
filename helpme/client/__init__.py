#!/usr/bin/env python

"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from helpme.logger import bot
from helpme.defaults import HELPME_HELPERS
import helpme
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="HelpMe Command Line Tool")

    # Global Variables

    parser.add_argument(
        "--debug",
        dest="debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="show version and exit.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--quiet",
        dest="quiet",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    description = "actions for HelpMe Command Line Tool"

    subparsers = parser.add_subparsers(
        help="helpme actions", title="actions", description=description, dest="command"
    )

    # list helpers and exit

    ls = subparsers.add_parser("list", help="show installed helpers")

    config = subparsers.add_parser("config", help="configure a helper")

    config.add_argument(
        "-i",
        dest="interactive",
        help="interactive configuration",
        default=False,
        action="store_true",
    )

    # Add helpers as commands

    for helper in HELPME_HELPERS:
        sub = subparsers.add_parser(helper)
        sub.add_argument(
            "--asciinema",
            dest="asciinema",
            help="""full path to asciinema video json file, if you
                         want to use one again on a subsequent request.""",
            default=None,
        )

    return parser


def get_subparsers(parser):
    """get_subparser will get a dictionary of subparsers, to help with printing help
    """

    actions = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers


def main():
    """the main entry point for the HelpMe Command line application. Currently,
       the user can request help or set config values for a particular helper.
    """

    # Customize parser

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        """print help, including the software version and active client 
           and exit with return code.
        """

        version = helpme.__version__

        bot.custom(
            message="Command Line Tool v%s" % version,
            prefix="\n[HelpMe] ",
            color="CYAN",
        )

        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args, unknown = parser.parse_known_args()
    except:
        sys.exit(0)

    extras = None
    if args.command in HELPME_HELPERS and len(unknown) > 0:
        extras = unknown

    # if environment logging variable not set, make silent

    if args.debug is False:
        os.environ["MESSAGELEVEL"] = "INFO"

    # Show the version and exit
    if args.version is True:
        print(helpme.__version__)
        sys.exit(0)

    if args.command == "config":
        from .config import main
    if args.command == "list":
        from .list import main
    if args.command in HELPME_HELPERS:
        from .help import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args, extras)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
