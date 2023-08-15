#!/home/administrator/Git/Local/mfa/venv/bin/python
#
# generators.py - part of the mfa project
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


import pyotp
from typing import Union

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = ["verify_totp_seed", "get_totp_code"]

__doc__ = (
'''
Functions for generating and verifying totp codes & seeds
'''
)


def verify_totp_seed(seed: str) -> bool:
    '''
    Verifies the format of a totp seed phrase/key

    Args:
        seed (str): The TOTP seed
    
    Returns:
        bool: True if correctly formatted, otherwise False
    '''
    if get_totp_code(seed):
        return True
    return False

def get_totp_code(seed: str) -> Union[str, bool]:
    '''

    Args:
        seed (str): The TOTP seed

    Returns:
        str or bool: 
            The current TOTP code if a valid seed is given, otherwise False
    '''
    try:
        return str(pyotp.TOTP(seed).now())
    except Exception:
        return False


