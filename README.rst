## Overview

This is a graphical interface program that allows the user to communicate with an
Arduino or other piece of hardware via a serial port. It provides:
- a simple output window which contains all of the information being routed through
    the serial port
- a text box which allows the user to type in an arbitrary command and send it
    by pressing return
- a drop-down menu used to select the serial port
- a button used to update the list of available ports (e.g. after resetting the
    physical connection)
- text boxes used to update the refresh rate of the GUI and the conenction Baud rate

## Installation and running

There are two options:
- install using pip
- run directly by setting ```SerialMonitor/__init__.py``` as an executable using
    ```chmod +x __init__py.``` and then executing it as ```./__init__.py```;
    can also use the symbolic link in the main directory for it

## Requirements

Requires wxWidgets 2.8 or newer. To install on Ubuntu Linux:
```
    apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n libwxgtk2.8-dev libgtk2.0-dev
```
GUI built with wxFormbuilder 3.5.1 (https://github.com/wxFormBuilder/wxFormBuilder)
To install on Ubuntu Linux:
```
    add-apt-repository ppa:wxformbuilder/release
    apt-get install wxformbuilder
```

Tested on Ubuntu 14.04 with Pyton 2.7.6

## Example

![Alt text](screenshot.png?raw=true "Main window of the program")
