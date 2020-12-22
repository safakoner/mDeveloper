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
## @file    mDeveloper/developerLib.py @brief [ FILE   ] - Developer related module.
## @package mDeveloper.developerLib    @brief [ MODULE ] - Developer related module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import importlib

from   getpass import getuser
from   types   import ModuleType

import mDeveloper.enumLib

import mFileSystem.directoryLib

import mMecoPackage.enumLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on developers.
class Developer(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  Developer module instance could be passed as user argument as well as user name of the developer as a string.
    #
    #  Developer module can be obtained from mDeveloper.developerLib.Developer.getDeveloperModule method.
    #
    #  @param developer [ str, module | getpass.getuser | in  ] - User name or the module of the developer.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, developer=getuser()):

        ## [ str ] - User name.
        self._userName = None

        ## [ str ] - Name.
        self._name     = None

        ## [ str ] - Position.
        self._position = None

        ## [ str ] - E-mail address.
        self._email    = None

        ## [ str ] - Site.
        self._site     = None

        ## [ str ] - URL.
        self._url      = None

        if developer:
            self.setDeveloper(developer)

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def __str__(self):

        info = '\n'

        info = '{}User Name: {}\n'.format(info, self._userName)
        info = '{}Name     : {}\n'.format(info, self._name)
        info = '{}Position : {}\n'.format(info, self._position)
        info = '{}E-mail   : {}\n'.format(info, self._email)
        info = '{}Site     : {}\n'.format(info, self._site)
        info = '{}URL      : {}\n'.format(info, self._url)

        return info

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def userName(self):

        return self._userName

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def name(self):

        return self._name

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def position(self):

        return self._position

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def email(self):

        return self._email

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def site(self):

        return self._site

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    def url(self):

        return self._url

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set developer.
    #
    #  Developer module instance can be provided for `developer` argument as well as user name of the developer as a string.
    #
    #  @param developer [ str, module | None | in  ] - Developer user name or the module of the developer.
    #
    #  @exception ValueError     - If given developer doesn't exist.
    #  @exception NameError      - If developer module doesn't have all the attributes.
    #  @exception ValueError     - If an attribute ID empty and this attribute is not person website URL.
    #  @exception AttributeError - If INFO dictionary doesn't match with attributes in developer module.
    #
    #  @return bool - Result.
    def setDeveloper(self, developer):

        _developerModule = None

        if isinstance(developer, ModuleType):
            _developerModule = developer

        else:

            developerLibName = Developer.isDeveloper(developer)
            if not developerLibName:
                raise ValueError('{} is not a valid developer.'.format(developer))

            _developerModule = Developer.getDeveloperModule(developerLibName)


        for attr in mDeveloper.enumLib.DeveloperModuleAttribute.listAttributes():

            if not hasattr(_developerModule, attr):
                raise NameError("Attribute {0} doesn't exist in the developer module: {1}".format(attr, getattr(_developerModule, '__name__')))

            if not getattr(_developerModule, attr) and attr is not mDeveloper.enumLib.DeveloperModuleAttribute.kURL:
                raise ValueError('Attribute {} cannot be empty in the module: {}'.format(attr, getattr(_developerModule, '__name__')))

        infoItems = sorted(['userName', 'position', 'url', 'name', 'email'])
        if sorted(_developerModule.__dict__['INFO'].keys()) != infoItems:
            errorMessage = 'INFO attribute should contain all the other static attributes in the developer module: {}'.format(getattr(_developerModule, '__name__'))
            raise AttributeError(errorMessage)

        self._userName = getattr(_developerModule, mDeveloper.enumLib.DeveloperModuleAttribute.kUserName)
        self._name     = getattr(_developerModule, mDeveloper.enumLib.DeveloperModuleAttribute.kName)
        self._position = getattr(_developerModule, mDeveloper.enumLib.DeveloperModuleAttribute.kPosition)
        self._email    = getattr(_developerModule, mDeveloper.enumLib.DeveloperModuleAttribute.kEmail)
        self._site     = getattr(_developerModule, mDeveloper.enumLib.DeveloperModuleAttribute.kSite)
        self._url      = getattr(_developerModule, mDeveloper.enumLib.DeveloperModuleAttribute.kURL)

        return True

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get developer module for given user.
    #
    #  @param developerLib [ str | None | in  ] - Developer module name.
    #
    #  @return module - Developer module.
    @staticmethod
    def getDeveloperModule(developerLib):

        if not developerLib.endswith(mMecoPackage.enumLib.PackagePythonFileSuffix.kLib):
            developerLib = '{}{}'.format(developerLib, mMecoPackage.enumLib.PackagePythonFileSuffix.kLib)

        _developerModule = importlib.import_module('mDeveloper.developers.{}'.format(developerLib))

        return _developerModule

    #
    ## @brief List developer user names.
    #
    #  Method returns the user name of the developers with Lib postfix which represents
    #  the python modules for the developers.
    #
    #  @exception N/A
    #
    #  @return list of str - User name of the developers.
    @staticmethod
    def listDevelopersAsStr():

        filesToIgnoreList = ['__init__.py']

        _directory = mFileSystem.directoryLib.Directory(directory=os.path.join(os.path.dirname(__file__), 'developers'))
        developerModuleList = _directory.listFiles(extension='py')
        developerModuleList = [x for x in developerModuleList if x not in filesToIgnoreList]
        developerModuleList = [x for x in developerModuleList if not x.endswith('{}.py'.format(mMecoPackage.enumLib.PackagePythonFileSuffix.kTest))]
        developerModuleList = [os.path.splitext(x)[0] for x in developerModuleList]

        return developerModuleList

    #
    ## @brief Check whether given user is valid developer with a developer module.
    #
    #  @param user [ str, module | getpass.getuser | in  ] - User name of the user.
    #
    #  @exception N/A
    #
    #  @return None - If user is not a valid developer.
    #  @return str  - Developer module name if user is a developer.
    @staticmethod
    def isDeveloper(user=getuser()):

        userLib = None

        if isinstance(user, ModuleType):
            userLib = user.__name__.split('.')[1]

        elif not user.endswith(mMecoPackage.enumLib.PackagePythonFileSuffix.kLib):
            user = user.split('@')[0] if '@' in user else user
            userLib = '{}{}'.format(user, mMecoPackage.enumLib.PackagePythonFileSuffix.kLib)

        if userLib not in Developer.listDevelopersAsStr():
            return None

        return userLib

    #
    ## @brief List developer modules.
    #
    #  @exception N/A
    #
    #  @return list of module - Developer modules.
    @staticmethod
    def listDeveloperModules():

        developerModuleNameList = Developer.listDevelopersAsStr()

        developerModuleList = []

        for i in developerModuleNameList:
            devModule = importlib.import_module('mDeveloper.developers.{}'.format(i))
            developerModuleList.append(devModule)

        return developerModuleList
