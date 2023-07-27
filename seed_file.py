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

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = [""]

__doc__ = (
'''
Manages the encryption and decryption of the user's seed file
'''
)

def convert_user_key(key: str) -> bytes:
    '''
    Convert the users string key to a 32 byte hash converted
    to base64 because Fernet requires that key format.

    user_key (str):
        The user provided key

    Returns:
        bytes:
            32 byte hash converted to base64
    '''
    salt = b"f\x9f\xa3\xcbLb\xe2R\x1d\xea\x88\xf7\x96\x7f\x92\xac"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500000,
    )

    return urlsafe_b64encode(kdf.derive(key.encode()))

def encrypt_to_file(data, output_file, key):
    key = convert_user_key(key)

    if type(data) == str:
        data = json.dumps(data).encode()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted_data)

def decrypt_from_file(input_file, key):
    key = convert_user_key(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
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
