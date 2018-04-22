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
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import os


# User Prompts

def confirm_prompt(prompt, choice=None):
    '''Ask the user for a prompt, and only return when one of the requested
       options is provided.

       Parameters
       ==========
       prompt: the prompt to ask the user
    
    '''
    print(prompt)
    get_input = getattr(__builtins__, 'raw_input', input)
    message = 'Please enter your choice [Y/N]: '
    while choice not in ['Y',"N","n","y"]:
        choice = get_input(message).strip()
        message = "Please enter a valid option in [Y/N]"    
    return choice



# Terminal Commands

def which(software, strip_newline=True):
    '''get_install will return the path to where an executable is installed.
    '''
    if software is None:
        software = "singularity"
    cmd = ['which', software ]
    try:
        result = run_command(cmd)
        if strip_newline is True:
            result['message'] = result['message'].strip('\n')
        return result

    except: # FileNotFoundError
        return None


def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def run_command(cmd, sudo=False):
    '''run_command uses subprocess to send a command to the terminal.

    Parameters
    ==========
    cmd: the command to send, should be a list for subprocess
    error_message: the error message to give to user if fails,
    if none specified, will alert that command failed.

    '''
    if sudo is True:
        cmd = ['sudo'] + cmd

    try:
        output = Popen(cmd,stderr=STDOUT,stdout=PIPE)

    except FileNotFoundError:
        cmd.pop(0)
        output = Popen(cmd,stderr=STDOUT,stdout=PIPE)

    t = output.communicate()[0],output.returncode
    output = {'message':t[0],
              'return_code':t[1]}

    if isinstance(output['message'], bytes):
        output['message'] = output['message'].decode('utf-8')

    return output
