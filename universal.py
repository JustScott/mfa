#!/home/administrator/Git/Local/mfa/venv/bin/python
#
# universal.py - part of the mfa project
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

import psutil
import os

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = ["process_is_running"]

__doc__ = (
'''
A bunch of universal variables and functions for importing across
all the rest of the scripts in this project
'''
)

HOME_PATH = os.environ["HOME"]
BASE_PATH = HOME_PATH+"/Git/Local/mfa"
CONFIG_FILE_PATH = BASE_PATH+"/mfa_config.json"


def process_is_running(*command_keywords: str) -> bool:
    '''
    Checks all running system processes for the command used to
    start the process. All keywords must be in the command for
    a match to be made.

    Args:
        *command_keywords:
            Keywords in the command that started the process, used
            to find the exact process.

    Returns:
        bool: True if all command_keywords were found in the process
            command, otherwise False
    '''
    # Loop through each proces
    for process in psutil.process_iter():
        matching_keywords = 0
        process_command = "".join(process.cmdline())
        # Loop through each command keyword
        for keyword in command_keywords:
            # If the keyword is in the command, increment by one
            if keyword in process_command:
                matching_keywords += 1

        if len(command_keywords) == matching_keywords:
            return True

    return False


if __name__=="__main__":
    pass
