#!/home/administrator/Git/Local/mfa/venv/bin/python
#
# config.py - part of the mfa project
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


import json

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = ["Config"]

__doc__ = (
'''
For interracting with a json config file
'''
)



class Config(dict):
    def __init__(self, config_path: str):
        self.config_path = config_path

        # Opens the existing, or creates a new config file if one
        #  didn't already exist
        while True:
            try:
                with open(self.config_path, 'r') as config_file:
                    config_file_content = json.load(config_file)
                    break
            except FileNotFoundError:
                with open(self.config_path, 'w') as config_file:
                    json.dump("{}", config_file)

        # Convert the config file content to a dict if its of the type str
        if isinstance(config_file_content, str):
            config_file_content = json.loads(config_file_content) 

        # Merge the instance dict with the config file's dict 
        for key,value in config_file_content.items():
            self[key] = value



    def __setitem__(self, key, value):
        super().__setitem__(key,value)

    def __getitem__(self, key):
        return super().__getitem__(key)   

    
    def write(self):
        with open(self.config_path, 'w') as config_file:
            json.dump(dict(self), config_file)


if __name__=="__main__":
    settings = Config('test.json')
    
