"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
