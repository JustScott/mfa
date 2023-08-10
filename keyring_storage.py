#!/home/administrator/Git/Local/mfa/venv/bin/python
#
# keyring_storage.py - part of the mfa project
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


import keyring

#from keyring.backends.libsecret import Keyring
#keyring = Keyring()

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__created__ = "July 26, 2023"

__updated__ = "July 27, 2023"

__all__ = [
    "set_keyring_password",
    "get_keyring_password",
    "delete_keyring_password"
]

__doc__ = (
'''
Manages storing the seed file's encryption password in the users keyring
'''
)

# Arbitrary variables for locating the password in the keyring
USERNAME = "python_keyring_user"
SERVICE_NAME = "mfa_keyring"

# Check if there's a suitable keyring available for the program to use
try:
    keyring.get_password("test", "test")
except keyring.errors.NoKeyringError:
    print(
"""

!-Missing a compatible keyring backend-!

Install one of the packages below from your system's package manager.


Linux:
------
* KWallet (requires dbus)
* SecretService (requires secretstorage)

Mac:
----
* Keychain

Windows:
--------
* Windows Credential Locker

"""
    )



def set_keyring_password(password):
    '''
    Set the seed file encryption password in the keyring
    '''
    keyring.set_password(SERVICE_NAME, USERNAME, password)

def get_keyring_password():
    '''
    Get the seed file encryption password from the keyring
    '''
    return keyring.get_password(SERVICE_NAME, USERNAME)

def delete_keyring_password():
    '''
    Delete the seed file encryption password from the keyring
    '''
    try:
        return keyring.delete_password(SERVICE_NAME, USERNAME)
    except keyring.errors.PasswordDeleteError:
        return True

