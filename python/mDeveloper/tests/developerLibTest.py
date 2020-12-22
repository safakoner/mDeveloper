#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    mDeveloper/tests/developerLibTest.py @brief [ FILE   ] - Unit test module.
## @package mDeveloper.tests.developerLibTest    @brief [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import types
import unittest

import mDeveloper.developerLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
class DeveloperTest(unittest.TestCase):

    def test_setDeveloper(self):

        _developer = mDeveloper.developerLib.Developer()

        self.assertTrue(_developer.setDeveloper('soner'))

        self.assertRaises(ValueError, _developer.setDeveloper, 'user')

    def test_getDeveloperModule(self):

        self.assertEqual(type(mDeveloper.developerLib.Developer.getDeveloperModule('sonerLib')), types.ModuleType)

        self.assertRaises(ImportError, mDeveloper.developerLib.Developer.getDeveloperModule, 'userLib')

    def test_listDevelopersAsStr(self):

        self.assertTrue('sonerLib' in mDeveloper.developerLib.Developer.listDevelopersAsStr())

        self.assertFalse('userLib' in mDeveloper.developerLib.Developer.listDevelopersAsStr())

    def test_isDeveloper(self):

        self.assertEqual(mDeveloper.developerLib.Developer.isDeveloper('soner'), 'sonerLib')

        self.assertEqual(mDeveloper.developerLib.Developer.isDeveloper('user'), None)

    def test_listDeveloperModules(self):

        _sonerLib = mDeveloper.developerLib.Developer.getDeveloperModule('sonerLib')

        self.assertTrue(_sonerLib in mDeveloper.developerLib.Developer.listDeveloperModules())


#
#-----------------------------------------------------------------------------------------------------
# INVOKE
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    unittest.main()
