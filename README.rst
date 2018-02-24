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

## Requirements

Requires wxWidgets 2.8 or newer. To install on Ubuntu Linux:
```
    apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n libwxgtk2.8-dev libgtk2.0-dev
```

To use wxWidgets 4.0 or newer, install the following prerequisites:
```
	apt-get install libgtk-3-dev libgstreamer-plugins-base0.10-dev libwebkit-dev libwebkitgtk-3.0-dev
```
According to [this post](https://github.com/wxWidgets/Phoenix/issues/465), the
wx installer cannot handle all the dependencies itself, so these have to be
installed by hand. A complete list of dependencies can be found
[here](https://github.com/wxWidgets/Phoenix/issues/465).

GUI built with wxFormbuilder 3.5.1 (https://github.com/wxFormBuilder/wxFormBuilder)
To install on Ubuntu Linux:
```
    add-apt-repository ppa:wxformbuilder/release
    apt-get install wxformbuilder
```

Tested on Ubuntu 14.04 with Python 2.7.6

## Example

![Alt text](screenshot.png?raw=true "Main window of the program")
