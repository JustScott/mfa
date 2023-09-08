# seed_file.py - part of the mfa project
# Copyright (C) 2023, Scott Wyman, development@scottwyman.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
import json
from typing import Union
import universal
import config
import keyring_storage
from getpass import getpass
import generators

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = ["encrypt_to_file", "decrypt_from_file"]

__doc__ = (
'''
Manages the encryption and decryption of the user's seed file

Uses the built-in cryptography library to encrypt and decrypt
the seed file using Fernet and the PBKDF2 algorithm 
'''
)


def convert_user_key(key: str) -> bytes:
    '''
    Convert the users string key to a 32 byte hash converted
    to base64 because Fernet requires that key format.

    user_key (str): The user provided key

    Returns:
        bytes: 32 byte hash converted to base64
    '''
    salt = b"f\x9f\xa3\xcbLb\xe2R\x1d\xea\x88\xf7\x96\x7f\x92\xac"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500000,
    )

    return urlsafe_b64encode(kdf.derive(key.encode()))

def encrypt_to_file(data: dict, output_file: str, key: str) -> None:
    '''
    Encrypts a dictionary to an output file using 256 bit AES in CBC mode

    Args:
        data (dict): The dictionary to be encrypted

        output_file (str): The file/path to encrypt the dictionary to

        key (str): The key used to encrypt the file

    Returns: None

    Raises:
        TypeError: If the data arg isn't a dict
    '''
    # Convert the key to a format acceptable by Fernet
    key = convert_user_key(key)

    # Convert the stringified dict 
    if type(data) != dict:
        raise TypeError("data must be a python dict")

    # Convert dict to string and encode it
    data = json.dumps(data).encode()

    # Encrypt the data
    #
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted_data)

def decrypt_from_file(input_file: str, key: str) -> Union[dict, bool]:
    '''
    Decrypts the files content to a dictionary

    Args:
        input_file (str): The file/path of the encrypted file

        key (str): The files decryption key

    Returns:
        dict or bool: The origional dictionary before it was encrypted,
        otherwise False if the incorrect decryption key was used
    '''
    # Convert the key to a format acceptable by Fernet
    key = convert_user_key(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()
    
    # Decrypt the data
    #
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    # Incorrect decryption key was given
    except InvalidToken:
        return False

    # Probably an uneccessarily complex way to get rid of the double quotes
    #  at the start and end of decrypted_data if they exist. Can't use replace
    #  as that will replace all double quotes in dictionary
    decrypted_data = decrypted_data.decode()
    if decrypted_data[:1] == '"' and decrypted_data[-1:] == '"':
        decrypted_data = decrypted_data[1:][:-1]
        decrypted_data = decrypted_data.replace("\\", "")

    return json.loads(decrypted_data)


class SeedDict(dict):
    _settings = config.Config(universal.CONFIG_FILE_PATH)
    # Get the seed_file_path from the config file if it exists
    SEED_FILE_PATH = _settings.get("seed_file_path")
    if 'mfa_secrets.aes' not in SEED_FILE_PATH:
        if SEED_FILE_PATH[-1] != "/":
            SEED_FILE_PATH += "/"
        SEED_FILE_PATH += "mfa_secrets.aes"
    # If the seed_file_path key doesn't exist in the database, and doesn't
    #  have a valid value
    if not SEED_FILE_PATH:
        # Set the seed file path in the config file to the default path
        _settings['seed_file_path'] = universal.HOME_PATH+"/mfa_secrets.aes"
        # Set the SEED_FILE_PATH class attribute
        SEED_FILE_PATH = _settings['seed_file_path']
    '''
    Instances operate as a dictionary with extra methods for
    checking keys and values, encrypting and writing the dictionary
    content to an aes file, etc.

    Attributes:
        SEED_FILE_PATH (str):
            The file name/path of the encrypted seed file 
    '''
    def __init__(self):
        '''
        The initialization handles decrypting the content of the seed file
        with the password stored in the keychain. It prompts the user for
        the password if it can't be found in the keychain.
        '''
        # Decrypt and add the contents of the seed_file to this
        #  instances dict
        #
        # Get the password from the keyring if it exists
        password = keyring_storage.get_keyring_password()
        seed_file_content = None
        getpass_message = "Enter the seed file's decryption key: "
        while True:
            # If there isn't a password in the keyring, or the
            #  wrong decryption password was used
            if not password or seed_file_content == False:
                # Ask the user for a password
                try:
                    password = getpass(getpass_message)
                except KeyboardInterrupt: # except a keyboard interrupt
                    print('\nCanceled')
                    quit(1)
            try:
                # Decrypt the seed file
                seed_file_content = decrypt_from_file(self.SEED_FILE_PATH, password)
            except FileNotFoundError:
                self.password = password
                self.write()
                seed_file_content = decrypt_from_file(self.SEED_FILE_PATH, password)

            # If the incorrect key is given
            if seed_file_content == False:
                getpass_message = "Incorrect Password, Try Again: "
                # Loop to decrypt again
                continue
            # If the file is decrypted successfully, update the
            #  keyring password and break
            keyring_storage.set_keyring_password(password)
            self.password = password
            break
       
        # If the seed file has any seeds, add them to instance dict
        if seed_file_content:
            for key,value in seed_file_content.items():
                self[key] = value


    def __setitem__(self, key, value):
        if generators.verify_totp_seed(value):
            super().__setitem__(key, value)

    def __getitem__(self, key):
        if key not in self:
            raise KeyError('Key not found')

        return super().__getitem__(key)

    def write(self):
        '''
        Write current seed dictionary to encrypted file
        '''
        data = dict(self)
        encrypt_to_file(data, self.SEED_FILE_PATH, self.password)

