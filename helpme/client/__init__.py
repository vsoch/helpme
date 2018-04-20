#!/usr/bin/env python

'''

Copyright (C) 2017-2018 Vanessa Sochat.
Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.

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

import helpme
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="HelpMe Command Line Tool")

    # Global Variables

    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--quiet', dest="quiet", 
                        help="suppress additional output.", 
                        default=False, action='store_true')

    description = 'actions for HelpMe Command Line Tool'

    subparsers = parser.add_subparsers(help='helpme actions',
                                       title='actions',
                                       description=description,
                                       dest="command")

    # list helpers and exit

    ls = subparsers.add_parser("list",
                               help="show installed helpers")

    # print version and exit

    version = subparsers.add_parser("version",
                                    help="show software version")
 
    config = subparsers.add_parser("config",
                                   help="configure a helper")

    config.add_argument('-i', dest="interactive", 
                        help="interactive configuration", 
                        default=False, action='store_true')

    # TODO: import choices here?
    parser.add_argument('client', choices=['github', 'uservoice'])

    return parser


def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers



def main():
    '''the main entry point for the HelpMe Command line application. Currently,
       the user can request help or set config values for a particular helper.
    '''

    # Customize parser depending on client

    from helpme.main import Client as cli
    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''

        version = helpme.__version__
        
        print("\nHelpMe Command Line Tool v%s [%s]" %(version, name))
        parser.print_help()
        sys.exit(return_code)
    
    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # if environment logging variable not set, make silent

    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "INFO"

    # Show the version and exit
    if args.command == "version":
        print(helpme.__version__)
        sys.exit(0)

    if args.command == "config": from .config import main
    if args.command == "list": from .list import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args,
             parser=parser,
             subparser=subparsers[args.command])
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)

if __name__ == '__main__':
    main()
