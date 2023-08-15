#!/home/administrator/Git/Local/mfa/venv/bin/python
#
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
# Ignores Resource warning errors, which are supposedly a bug
from universal import ignore_warnings
import mfa
import generators


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
        Ensures new seeds can be added to the mfa file.

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



if __name__=="__main__":
    unittest.main()
