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

__date__ = "July 26, 2023"

__all__ = [""]

__doc__ = (
'''
Manages storing the seed file's encryption key in the users keyring
'''
)


USERNAME = "python_keyring_user"
SERVICE_NAME = "mfa_keyring"

def set_keyring_password(password):
    keyring.set_password(SERVICE_NAME, USERNAME, password)

def get_keyring_password():
    return keyring.get_password(SERVICE_NAME, USERNAME)

