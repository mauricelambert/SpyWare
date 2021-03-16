#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement a SpyWare to get all connection destination. """

###################
#    This file implement a SpyWare to get all connection destination.
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

__all__ = ["Daemon", "main", "CacheDNS", "CacheBrowser", "config_load"]

from os import path, environ, device_encoding, environ
from configparser import ConfigParser
from subprocess import Popen, PIPE
from platform import system
from re import finditer
from time import sleep
from glob import iglob
from enum import Enum
from sys import argv


def config_load() -> None:

    """ This function load the config file. """

    global Constantes

    CONFIG = ConfigParser()
    env_conf_file = environ.get("domainsSpy.conf")

    if len(argv) == 2:
        CONFIG.read(argv[1])
    elif env_conf_file:
        CONFIG.read(env_conf_file)
    else:
        CONFIG.read(
            path.join(
                path.dirname(__file__), "domainsSpy.conf"
            )
        )


    class Constantes(Enum):

        regex_domain = "[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\.[a-zA-Z]{2,4})"
        regex_ip = "([0-9]{1,3}[.]){3}[0-9]{0,3}"

        save_filename = CONFIG["SAVE"]["filename"]

        if system() == "Windows":
            commandes = (["ipconfig", "/displaydns"],)
            browser_directories = path.join(environ["APPDATA"], "..")
        else:
            commandes = (
                ["strings", "/var/cache/nscd/hosts"],
                ["sudo", "killall", "-USR1", "systemd-resolved"],
                ["sudo", "journalctl", "-u", "systemd-resolved"],
            )
            browser_directories = path.join(path.expandser("~"), ".locals")

        timeDns: float = CONFIG.getfloat("TIME", "dnsSleep")
        timeBrowser: float = CONFIG.getfloat("TIME", "browserSleep")
        timeBetweenReadingFile: float = CONFIG.getfloat("TIME", "readingFileSleep")
        timeBetweenGetDomain: float = CONFIG.getfloat("TIME", "getDomainSleep")


class Daemon:

    """ This class launch DNS this script as service for ever. """

    def __init__(self):
        self.timeBrowser = Constantes.timeBrowser.value
        self.timeDns = Constantes.timeDns.value
        self.cacheAppData = CacheBrowser()
        self.cacheDns = CacheDNS()
        self.run = True

    def run_CacheDns(self) -> None:

        """ This function launch the loop to get DnsCache. """

        create_file()

        while self.run:
            self.cacheDns.launch()
            self.cacheDns.research()
            self.cacheDns.save()
            if self.run:
                sleep(self.timeDns)

    def run_AppData(self) -> None:

        """ This function launch the loop to get BrowserCache. """

        create_file()

        while self.run:
            self.cacheAppData.get_filenames(
                path.join(Constantes.browser_directories.value, "..")
            )
            if self.run:
                sleep(self.timeBrowser)


class CacheDNS:

    """ This class get DNS cache and find all domains and IP. """

    def __init__(self):
        self.commandes = Constantes.commandes.value
        self.process = None
        self.out = None
        self.ip = []
        self.domains = []

    def launch(self) -> None:

        """ This function execute the command to get DNS cache. """

        self.out = ""
        errors = ""
        for commande in self.commandes:
            self.process = Popen(commande, stdout=PIPE, stderr=PIPE)
            out, err = self.process.communicate()
            self.out += out.decode(device_encoding(0))
            errors += err.decode(device_encoding(0))

        if errors or self.process.returncode:
            print(f"Error: {err}")

    def research(self) -> None:

        """ This function research IP and domains from stdout. """

        for ip in finditer(Constantes.regex_ip.value, self.out):
            sleep(Constantes.timeBetweenGetDomain.value)
            self.ip.append(ip.group())

        for domain in finditer(Constantes.regex_domain.value, self.out):
            sleep(Constantes.timeBetweenGetDomain.value)
            self.domains.append(domain.group())

    def save(self):

        """ This function save ip and domains. """

        write_if_not_in_file(*(self.domains + self.ip))


class CacheBrowser:

    """ This class get domains and IP in Browser and Application cache. """

    def __init__(self):
        self.data = None
        self.temp_data = None
        self.regex_ip = Constantes.regex_ip.value.encode()
        self.regex_domain = Constantes.regex_domain.value.encode()
        self.save_filename = Constantes.save_filename.value
        self.time_between_reading_file = Constantes.timeBetweenReadingFile.value

    def save(self, *data) -> None:

        """ This function save data. """

        with open(self.save_filename) as file:
            self.data = file.read()

        file = open(self.save_filename, "a")
        for domain in data:
            domain = domain.decode()
            if domain not in self.data:
                file.write(domain + "\n")
                self.data += domain + "\n"
        file.close()

        self.data = None

    def get_filenames(self, directory: str) -> None:

        """ This function get recursives filenames. """

        for filename in iglob(path.join(directory, "*")):
            if path.isdir(filename):
                self.get_filenames(path.join(directory, filename))
            elif path.isfile(filename):
                try:
                    self.get_data(path.join(directory, filename))
                except Exception as e:
                    print(e)
                sleep(self.time_between_reading_file)

    def get_data(self, filename: str) -> None:

        """ This function get domain and IP from data file. """

        with open(filename, "rb") as file:
            data = file.read()

        datas = []
        for ip in finditer(self.regex_ip, data):
            sleep(Constantes.timeBetweenGetDomain.value)
            datas.append(ip.group())

        for domain in finditer(self.regex_domain, data):
            sleep(Constantes.timeBetweenGetDomain.value)
            datas.append(domain.group())

        self.save(*datas)


def create_file():

    """ This function create the file to save if is not exist. """

    if not path.exists(Constantes.save_filename.value):
        with open(Constantes.save_filename.value, "w") as file:
            file.write("")

def write_if_not_in_file(*list_to_write) -> None:

    """ This function write data if this data is not in file. """

    with open(Constantes.save_filename.value, "r") as file:
        texte = file.read()

    with open(Constantes.save_filename.value, "a") as file:
        for element in list_to_write:
            if element not in texte:
                file.write(element + "\n")
                texte += element + "\n"


def main() -> None:
    from threading import Thread

    config_load()

    daemon = Daemon()
    thread = Thread(target=daemon.run_CacheDns)
    thread.start()
    try:
        daemon.run_AppData()
    except KeyboardInterrupt:
        daemon.run = False

    thread.join()

if __name__ == "__main__":
    main()
