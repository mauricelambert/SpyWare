from setuptools import setup, find_packages
from platform import system
import sys

def is_64bit() -> bool:
    return sys.maxsize > 2**32

whl_file = "PyAudio-0.2.11-cp39-cp39-win_amd64.whl" if is_64bit() else "PyAudio-0.2.11-cp39-cp39-win32.whl"
packages = ['pyautogui', 'opencv-python', 'pillow', 'pyperclip', 'pynput']

if system() == "Windows":
    from os import system
    system(f"python -m pip install {whl_file}")
else:
    from os import system
    system("sudo apt-get install portaudio19-dev python-pyaudio")
    packages.append("pyaudio")

setup(
    name = 'SpyWare',
 
    version = "0.0.1",
    packages = find_packages(include=["SpyWare"]),
    install_requires = packages,

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package implement a complete SpyWare.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/SpyWare',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Topic :: Security",
    ],
 
    entry_points = {
        'console_scripts': [
            'SpyWare = SpyWare:spyware'
        ],
    },
    python_requires='>=3.6',
)