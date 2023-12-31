# mfa_test.py - part of the mfa project
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


import unittest
from random import randint
import mfa
import generators
import keyring_storage

import json
import os


__author__ = "Scott Wyman (development@scottwyman.me)"

__license__ = "GPLv3"

__date__ = "August 15, 2023"

__all__ = []

__doc__ = (
'''
A script for testing all the commands/functions within mfa.py
'''
)


random_str = lambda length: "".join([chr(randint(40,90)) for _ in range(length)])

class MFATests(unittest.TestCase):
    EXAMPLE_MFA_SEED="E2AXR2QIHC26R45A"

    def __init__(self, *args, **kwargs):
        super(MFATests, self).__init__(*args, **kwargs)

    def test_add_show_delete(self):
        '''
        Tests: mfa [add, show, show-all, show-seed, delete]
        '''
        random_seed_name = random_str(20)
        random_seed_name2 = random_str(20)
        EXAMPLE_MFA_SEED2 = self.EXAMPLE_MFA_SEED.replace('X', '3')

        mfa.add(random_seed_name, self.EXAMPLE_MFA_SEED, force=False)
        mfa.add(random_seed_name2, EXAMPLE_MFA_SEED2, force=False)

        # Test showing a single code
        self.assertTrue(
            mfa.show(random_seed_name) == generators.get_totp_code(self.EXAMPLE_MFA_SEED),
            msg="The code generated in mfa.py, and the code generated here don't match"
        )

        # Test showing all codes
        all_names_codes = mfa.show_all()
        for name in [random_seed_name, random_seed_name2]:
            self.assertTrue(
                len(all_names_codes.get(name, "")) == 6,
                msg=f"The code name '{name}' isn't in the seed file"
            )

        # Test showing a seed phrase
        self.assertTrue(
            mfa.show_seed(random_seed_name2) == EXAMPLE_MFA_SEED2,
            msg="The test seed phrase isn't showing in the seed file"
        )


        # Test deleting a seed phrase
        if (
            random_seed_name in all_names_codes 
            and random_seed_name2 in all_names_codes
        ):
            mfa.delete(random_seed_name)
            mfa.delete(random_seed_name2)
            all_names_codes = mfa.show_all()

            self.assertTrue(
                (
                random_seed_name not in all_names_codes
                and random_seed_name2 not in all_names_codes
                ),
                msg="Seeds weren't deleted from the seed file"
            )
        else:
            self.assertTrue(False, msg="Test seed names not in seed file")

    def test_lock(self):
        '''
        Tests: mfa [lock]
        '''
        # Unlock the seed file if it's locked
        mfa.show_all()

        # Check that the password is in the keyring
        self.assertTrue(
            keyring_storage.get_keyring_password() != None,
            msg="The password failed to add to the keyring"
        )

        # Remove it from the keyring
        mfa.lock()

        # Check that the password is no longer in the keyring
        self.assertTrue(
            keyring_storage.get_keyring_password() == None,
            msg="The password failed to remove from the keyring"
        )

    def test_export_import_seeds(self):
        '''
        Tests: mfa [export-seeds, import-seeds]

        Ensures the export and import were successful by checking
        that all the names and codes returned by `mfa.show_all` are
        the same before and after each export and import
        '''
        random_test_file = 'export_import_seeds.test'
        
        # Test export/import with & without encryption, with file_path
        for encryption_bool,assert_message in zip([True,False],["with","without"]):
            all_names_codes_before = mfa.show_all()
            
            mfa.export_seeds(encrypt=encryption_bool, file_path=random_test_file)
            mfa.import_seeds(file_path=random_test_file)

            self.assertTrue(
                all_names_codes_before == mfa.show_all(),
                msg=f"Exporting/Importing to file {assert_message} encryption failed"
            )

            os.remove(random_test_file) # Remove the test file

            # Test export/import with & without encryption, without file_path
            #
            all_names_codes_before = mfa.show_all()

            exported_seeds = mfa.export_seeds(encrypt=encryption_bool)
            with open(random_test_file, 'w') as file:
                if encryption_bool:
                    file.write(exported_seeds)
                else:
                    json.dump(exported_seeds, file)
            mfa.import_seeds(random_test_file)

            self.assertTrue(
                all_names_codes_before == mfa.show_all(),
                msg=f"Exporting/Importing to stdout {assert_message} encryption failed"
            )

            os.remove(random_test_file) # Remove the test file

    def test_export_import_settings_config(self):
        '''
        Tests: mfa [export-config, import-confg, config-settings]
        '''
        random_test_file = 'export_import_config.test'

        # Test exporting to stdout
        config_dict_before = dict(mfa.export_config())

        # Test both export and importing to file
        mfa.export_config(random_test_file)
        mfa.import_config(random_test_file)

        self.assertTrue(
            config_dict_before == dict(mfa.export_config()),
            msg="Config before export & import test doesn't match config after"
        )

        
        # Get the original value for setting it back after the test
        original_lock_interval = mfa.settings["auto_lock_interval"]

        # Test config settinegs
        mfa.config_settings(auto_lock_interval=5)

        self.assertTrue(
            mfa.settings["auto_lock_interval"] == 5,
            msg="Failed to set auto_lock_interval in config"
        )

        # Set auto_lock_interval back to its origionval vlaue
        mfa.config_settings(auto_lock_interval=original_lock_interval)


if __name__=="__main__":
    unittest.main()
