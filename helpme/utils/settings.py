"""

Copyright (C) 2017-2018 Vanessa Sochat.

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

from helpme.utils import get_installdir, mkdir_p, read_file
import configparser
import getpass
import os

try:
    from urllib.parse import quote_plus
except:
    from urlparse import quote_plus


def get_configfile():
    """return the full path to the configuration file
    """
    return os.path.abspath(os.path.join(get_installdir(), "helpme.cfg"))


def load_keypair(keypair_file):
    """load a keypair from a keypair file. We add attributes key (the raw key)
       and public_key (the url prepared public key) to the client.

       Parameters
       ==========
       keypair_file: the pem file to load.
    """
    from Crypto.PublicKey import RSA

    # Load key
    with open(keypair_file, "rb") as filey:
        key = RSA.import_key(filey.read())

    return quote_plus(key.publickey().exportKey().decode("utf-8"))


def generate_keypair(keypair_file):
    """generate_keypair is used by some of the helpers that need a keypair.
       The function should be used if the client doesn't have the attribute 
       self.key. We generate the key and return it.

       We use pycryptodome (3.7.2)       

       Parameters
       =========
       keypair_file: fullpath to where to save keypair
    """

    from Crypto.PublicKey import RSA

    key = RSA.generate(2048)

    # Ensure helper directory exists
    keypair_dir = os.path.dirname(keypair_file)
    if not os.path.exists(keypair_dir):
        os.makedirs(keypair_dir)

    # Save key
    with open(keypair_file, "wb") as filey:
        filey.write(key.exportKey("PEM"))

    return key
