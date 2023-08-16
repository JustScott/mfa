#!/home/administrator/Git/Local/mfa/venv/bin/python
#
# mfa.py - part of the mfa project
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


import typer
import json
import generators
import keyring_storage
import seed_file
from seed_file import SeedDict
from getpass import getpass
import shutil
import os
import universal
import config
from pprint import pprint
import typing

__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "July 26, 2023"

__all__ = []

__doc__ = (
'''
A simple TOTP MFA CLI authenticator
'''
)


app = typer.Typer()
settings = config.Config(universal.CONFIG_FILE_PATH)

# Returns True if running directly, False if imported. Helpful for suppressing
#  stdout during
def output(
        print_statement: str=None, return_code: int=0, raw_data: typing.Any=None
    ) -> typing.Union[typing.Any, None]:
    '''
    prints the print_statement if being run direcly, or returns the data
    if being imported

    Args:
        print_statement (str, *optional): 
            The string to print when the script is ran directly
        
        return_code (int, *optional):
            DEFAULT 0

            This code is returned to the terminal after the script is ran
            directly. 0 signifies the command was successful, while 1
            through 254 mean the command couldn't do what it's expected to
            do given the user input (or lack of input).

        raw_data (Any, *optional):
            The data to return when the scripts modules are being imported
            by another script

    Returns:
        Any OR None: Any raw data type if imported, or none if ran directly
    '''
    # If script is imported
    if __name__!="__main__":
        return raw_data

    if print_statement:
        pprint(print_statement)
    quit(return_code)




@app.command()
def show(name: str) -> typing.Union[str, bool]:
    '''
    Show a single name and generated TOTP code

    Args:\n
        name (str): The name used to refence the seed phrase in the seed file
    '''
    seed_dict = SeedDict()

    if name in seed_dict:
        code = generators.get_totp_code(seed_dict[name])
        return output(f"{name} - {code}", 0, str(code))
    else:
        return output(f"{name} not in seed file", 1, False)

@app.command()
def show_all() -> typing.Union[dict, bool]:
    '''
    Show all the names and generated TOTP codes
    '''
    seed_dict = SeedDict()
    seed_names_codes = {}

    if seed_dict:
        seed_names_codes = {
            name:generators.get_totp_code(seed_dict[name])
            for name in seed_dict
        }
        
        if __name__=="__main__":
            for name,code in seed_names_codes.items():
                print(f"{name} - {code}")

        return output(
            None,
            0,
            seed_names_codes
        )

    else:
        return output(" - Seed file is empty - ", 1, False)

@app.command()
def show_seed(name: str) -> typing.Union[str, bool]:
    '''
    Show a seed phrase from your seed file

    Args:\n
        name (str): The name used to reference the seed phrase in the seed file
    '''
    seed_dict = SeedDict()

    if name in seed_dict:
        return output(f"{name} - {seed_dict[name]}", 0, seed_dict[name])
    else:
        return output(f"{name} not in seed file", 1, False)

@app.command()
def add(name: str, seed: str, force: bool=False) -> typing.Union[dict, bool]:
    '''
    Add a new entry to your seed file

    Args:\n
        name (str): The name to reference your seed by
        \n
        seed (str): The TOTP seed phrase given by the application or service
        \n
        force (str): Forcibly change/update your entry's seed phrase
    '''
    seed_dict = SeedDict()

    if name in seed_dict and force == False:
        return output(f"{name} already exists, pass '--force' to true to overwrite", 0, False)
    else:
        seed_dict[name] = seed
        if seed_dict.get(name) == seed:
            show(name)
        else:
            return output("Incorrect seed format", 0, False)
        seed_dict.write()

@app.command()
def delete(name: str) -> typing.Union[str, bool]:
    '''
    Delete an entry from your seed file

    Args:\n
        name (str): The name of the entry
    '''
    seed_dict = SeedDict()

    if name in seed_dict:
        seed = seed_dict[name]
        del seed_dict[name]
        seed_dict.write()
        return output(f"Deleted seed for '{name}'", 0, seed)
    else:
        return output(f"No seed named '{name}'", 1, False)


@app.command()
def export_seeds(encrypt: bool=True, file_path: str="") -> typing.Union[dict, str, bool]:
    '''
    Export seed file content to a file or stdout in an encrypted or plain format

    Args:\n
        encrypt (bool, *optional):\n
            Whether to export the file as encrypted or plain
        \n
        file_path (str, *optional):\n
            The name of the file to export to. Output is directed to
            stdout if no file_path is provided.

    '''
    if not file_path:
        if encrypt:
            # print the seed files encrypted content to stdout
            with open(SeedDict.SEED_FILE_PATH, 'r') as file:
                encrypted_file_content = file.read()
                return output(encrypted_file_content, 0, encrypted_file_content)
        # print the unencrypted seeds to stdout
        return output(dict(SeedDict()), 0, dict(SeedDict()))
    
    if file_path:
        if encrypt:
            # Copy the seed files encrypted content to the export file
            shutil.copyfile(SeedDict.SEED_FILE_PATH, file_path)
            return True
        # Write the un-encrypted seed dict to the file
        with open(file_path, 'w') as export_file:
            json.dump((dict(SeedDict())), export_file)
            return True

@app.command()
def import_seeds(file_path: str) -> bool:
    '''
    Import a previously exported file, overwriting the existing seeds

    Args:\n
        file_path (str):\n
            The previously exported file needs to either have a .aes or .json
            file suffix/extension.
    '''
    seed_dict = SeedDict()

    try:
        # Try loading as json
        try:
            # If plaintext, read in file content, create a new SeedDict instance
            #  which will encrypt the content to the mfa_secrets.aes file
            with open(file_path, 'r') as file:
                file_content = json.load(file)

            new_seed_dict = SeedDict()
            for name,seed in file_content.items():
                new_seed_dict[name] = seed
            new_seed_dict.write()
            return output(f"'{file_path}' imported successfully", 0, True)

        # If the file doesn't contain valid json data
        except (AttributeError,json.decoder.JSONDecodeError):
            # If the file decrypts successfully
            if seed_file.decrypt_from_file(file_path, seed_dict.password):
                # Copy the encrypted file directly
                shutil.copyfile(file_path, seed_dict.SEED_FILE_PATH)
                return output("Import Successful!", 0, True)

            # If the file didn't decrypt correctly
            return output(
                f"Either the incorrect password was used, or '{file_path}' is corrupt", 
                1,
                False
            )

    except FileNotFoundError:
        return output(f"'{file_path}' doesn't exists", 1, False)


@app.command()
def lock() -> typing.Union[bool, None]:
    '''
    Lock the seed file, AKA remove the password from the keyring
    '''
    keyring_storage.delete_keyring_password()
    return output("Seed file locked!", 0, True)

@app.command()
def auto_lock(minutes: int) -> typing.Union[int, bool]:
    '''
    Lockout access to the seed file in x minute intervals

    Starts a background script that runs the lock command at user set intervals
    
    Args:\n
        minutes (int):
            Access to the MFA codes will be locked every time this number
            of minutes passes.

            Set minutes to zero to turn off the locking
    '''
    # If the user passes a zero or a negative number,
    #  set the config files auto_lock_interval to 0
    if minutes < 1:
        settings['auto_lock_interval'] = 0
        settings.write()
        return output("Auto locking turned off", 0, True)

    # Start the auto_lock.py script if it's not already running
    if not universal.process_is_running('python3', 'auto_lock.py'):
        os.system(f'{universal.BASE_PATH}/venv/bin/python3 {universal.BASE_PATH}/auto_lock.py &')

    settings['auto_lock_interval'] = int(minutes)
    settings.write()
    return output(f"Access to the MFA codes will be locked every {minutes} minute(s)", 0, int(minutes))


@app.command()
def config_settings(
        seed_file_path: str=None, config_file_path: str=None, 
        auto_lock_interval: str=None
    ) -> typing.Union[dict, None]:
    '''
    Change any setting in the config file

    Args:\n
        seed-file-path (str, *optional): The encrypted seed file's new full path, not including the file name

        auto-lock-interval (int, *optional):\n 
            Minutes between automatic locking intervals. Set to zero to turn off.
    '''
    for setting,value in locals().items():
        # If the user changes auto_lock_interval, just pass the value
        #  to the auto_lock function since it already has the logic to
        #  check and set the value
        if setting == 'auto_lock_interval' and value != None and value.isdigit():
            auto_lock(int(value))
        if setting == 'seed_file_path' and value:
            shutil.move(SeedDict.SEED_FILE_PATH, value)
            

        # Otherwise, if another value is passed, set it in the config file
        if value:
            settings[setting] = value

    settings.write()
    return output(f"Settings Changed:\n{dict(settings)}", 0, dict(settings))

@app.command()
def export_config(export_file_path: str="") -> typing.Union[dict, None]:
    '''
    Export your json config settings to a file or stdout
    
    Args:
        export_file_path (str, *optional):
            The file to export your json config settings to, leave empty
            to print the json to stdout
    '''
    if export_file_path:
        shutil.copyfile(universal.CONFIG_FILE_PATH, export_file_path)
        return

    return output(settings, 0, settings)

@app.command()
def import_config(file_path: str) -> bool:
    '''
    Import a previously exported config file

    Args:
        file_path (str):
            The full path of the config file, including the file's name
    '''
    try:
        # Make sure the file is valid json
        with open(file_path, 'r') as config_file:
            json.load(config_file)

        # Overwrite the existing config file if it exists, with the user
        #  provided config file
        shutil.copyfile(file_path, universal.CONFIG_FILE_PATH)
        return output("Import Successful!", 0, True)
    except FileNotFoundError:
        return output(f"Can't open the file '{file_path}'", 1, False)
    except json.decoder.JSONDecodeError:
        return output(f"'{file_path}' is not a valid MFA configuration file", 1, False)


if __name__=="__main__":
    # If the auto lock is on in the config file and the auto_lock.py script isn't running
    if settings.get('auto_lock_interval') and not universal.process_is_running('python3', 'auto_lock.py'):
        # Turn on auto locking with the saved interval
        auto_lock(settings['auto_lock_interval'])

    app()
