# auto_lock.py - part of the mfa project
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

# Imports work different depending on whether this is ran as a
#  system application, or as an importable library
try:
    # For importing as a module
    from mfa import universal
    from mfa import config
    from mfa import keyring_storage
except ImportError:
    # For running as a system application
    import universal
    import config
    import keyring_storage

import time
import os

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = [""]

__doc__ = (
'''
A simple background script that continuously removes the
seed encryption password from the systems keyring
'''
)


def loop():
    while True:
        settings = config.Config(universal.CONFIG_FILE_PATH)
        minutes = int(settings.get("auto_lock_interval", 0))

        seconds = minutes*60
        time.sleep(seconds)

        # If the minute value is zero, that's a single to stop
        #  the script
        if int(minutes) < 1:
            quit()

        keyring_storage.delete_keyring_password()


if __name__=="__main__":
    loop()    

