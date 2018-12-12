'''

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

'''

from helpme.utils import ( get_installdir, mkdir_p )
import configparser
import getpass
import os

def get_configfile():
    '''return the full path to the configuration file
    '''
    return os.path.abspath(os.path.join(get_installdir(), 'helpme.cfg'))


def generate_keypair(name, keypair_dir, keypair_name):
    '''generate_keypair is used by some of the helpers that need a keypair.
       Since pgpy is a dependency of not all, we import within the function
       we return the key object, which has the key (private and public)

       Parameters
       ==========
       name: the name of the client (e.g., discourse)
       keypair_dir: the directory to store the keypair
       keypair_name: the name of the file (defaults to hmpgp)
    '''
    from pgpy.constants import ( PubKeyAlgorithm,
                                 KeyFlags, 
                                 HashAlgorithm, 
                                 SymmetricKeyAlgorithm, 
                                 CompressionAlgorithm )

    import pgpy

    # Get the username to generate the key for
    username = getpass.getuser()

    # If the directory doesn't exist, create it
    if not os.path.exists(keypair_dir):
        mkdir_p(keypair_dir)

    # This is a primary key, RSA
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)

    # create a user id for helpme-discourse
    uid = pgpy.PGPUID.new(username, comment='Helpme %s' % name)

    # Add the new user id to the key, we need to add all because PGPy doesn't have
    # built in defaults. These are similar to defaults from GNU PG 2.1.x
    # (no expiration or key server)

    key.add_uid(uid, 
                usage = { KeyFlags.Sign, 
                          KeyFlags.EncryptCommunications, 
                          KeyFlags.EncryptStorage },

                hashes= [ HashAlgorithm.SHA256, 
                          HashAlgorithm.SHA384, 
                          HashAlgorithm.SHA512, 
                          HashAlgorithm.SHA224 ],

                ciphers = [ SymmetricKeyAlgorithm.AES256, 
                            SymmetricKeyAlgorithm.AES192, 
                            SymmetricKeyAlgorithm.AES128 ],

                compression=[ CompressionAlgorithm.ZLIB,
                              CompressionAlgorithm.BZ2, 
                              CompressionAlgorithm.ZIP, 
                              CompressionAlgorithm.Uncompressed ] )

    # Save private
    keypair_private = os.path.join(keypair_dir, "%s.priv" % keypair_name)
    with open(keypair_private, 'w') as filey:
        filey.write(str(key))

    # Save public
    keypair_public = os.path.join(keypair_dir, "%s.pub" % keypair_name)
    with open(keypair_public, 'w') as filey:
        filey.write(str(key.pubkey))

    return key.pubkey, key
