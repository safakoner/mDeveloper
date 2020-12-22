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
## @file    mDeveloper/developerCmd.py @brief [ FILE   ] - Command module.
## @package mDeveloper.developerCmd    @brief [ MODULE ] - Command module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import argparse

import mCore.displayLib

import mDeveloper.developerLib



#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief List all developers.
#
#  @exception N/A
#
#  @return None - None.
def listDevelopers():

    developerModuleList = mDeveloper.developerLib.Developer.listDeveloperModules()
    if not developerModuleList:
        mCore.displayLib.Display.displayInfo('No developers found.')
        return

    parser = argparse.ArgumentParser(description='List developers')

    parser.add_argument('-d',
                        '--detail',
                        action='store_true',
                        help='Display details about the developers')

    _args   = parser.parse_args()

    detail  = _args.detail

    if not detail:
        mCore.displayLib.Display.displayBlankLine()

    for module in developerModuleList:

        _developer = mDeveloper.developerLib.Developer(module)

        if detail:
            mCore.displayLib.Display.displayInfo(_developer)
        else:
            mCore.displayLib.Display.displayInfo(_developer.userName())

    if not detail:
        mCore.displayLib.Display.displayBlankLine()

    mCore.displayLib.Display.displayInfo(('{} developer(s) listed.'.format(len(developerModuleList))))

    mCore.displayLib.Display.displayBlankLine()

#
## @brief Search developers.
#
#  @exception N/A
#
#  @return None - None.
def search():

    developerModuleList = mDeveloper.developerLib.Developer.listDeveloperModules()
    if not developerModuleList:
        mCore.displayLib.Display.displayInfo('No developers found.')
        return

    parser = argparse.ArgumentParser(description='Search for developers')

    parser.add_argument('keyword',
                        type=str,
                        help='Keyword to be searched')

    parser.add_argument('-d',
                        '--detail',
                        action='store_true',
                        help='Display details about the developers')

    _args   = parser.parse_args()

    keyword = _args.keyword.lower()
    detail  = _args.detail

    if not detail:
        mCore.displayLib.Display.displayBlankLine()

    developerCount = 0

    for module in developerModuleList:

        _developer = mDeveloper.developerLib.Developer(module)

        if keyword in _developer.userName().lower() or \
           keyword in _developer.name().lower():

            developerCount += 1

            if detail:
                mCore.displayLib.Display.displayInfo(_developer)
            else:
                mCore.displayLib.Display.displayInfo(_developer.userName())

    if not detail:
        mCore.displayLib.Display.displayBlankLine()

    if developerCount:
        mCore.displayLib.Display.displayInfo('{} developer(s) found.'.format(developerCount))
    else:
        mCore.displayLib.Display.displayInfo('No developers found.')

    mCore.displayLib.Display.displayBlankLine()
