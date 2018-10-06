Overview
=========

This is a graphical interface program that allows the user to communicate with a
microcontroller or other piece of hardware via a serial port. It provides:

- a simple output window which contains all of the information being routed through the serial port
- a text box which allows the user to type in an arbitrary command and send it by pressing return
- a drop-down menu used to select the serial port
- a button used to update the list of available ports (e.g. after resetting the physical connection)
- text boxes used to update the refresh rate of the GUI and the connection Baud rate
- ability to display hex codes of the received bytes instead of their unicode representations
- logging facilities that can record the data received over serial port into a file

Usage
======

Installation
-------------

There are the two options to use the SerialMonitor:

- install using pip and run from Python or an entry-point script,
- run directly from source by importing the SerialMonitor modul and calling main()

Pip is, by far, the easiest option that should also install all the dependencies
for you. In order to install with pip, just download the newest ``tar.gz``
distribution, and run:
```pip2.7 install SerialMonitor--X.Y.Z.tar.gz```
On Linux, you might need to prepend ```sudo -H``` to the pip call in order allow
pip to install in write-protected directories. On Windows, you need to prepend
```python -m``` and possibly start the command line as an administrator.

Prerequisites
--------------

SerialMonitor requires wxWidgets 4.0.1 or newer. Installing with pip should
install the newest version of wxWidgets. However, pip might struggle to install
all the wxWidgets dependencies (see `this post
<https://github.com/wxWidgets/Phoenix/issues/465>`_),
so these have to be installed by hand. A complete list of dependencies can be
found `here
<https://github.com/wxWidgets/Phoenix/issues/465>`_. Installing the
following dependencies worked on Ubuntu 16 (pip successfully installed the
SerialMonitor and the newest wxWidgets afterwards):

```	apt-get install libgtk-3-dev libgstreamer-plugins-base0.10-dev libwebkit-dev libwebkitgtk-3.0-dev```

If all else fails, install the above mentioned dependencies manually. Then,
wxWidgets and other Python dependencies can be installed with pip individually
as well:

```sudo pip3 install pySerial```

```sudo pip3 install wxPython```

Running
--------

If you install with pip on Ubuntu, an entry-point script will be automatically
installed in ``/usr/local/bin/serialMonitor`` and added to the ``PATH``.
So simply typing ``serialMonitor`` in the command line will launch it. If the
script doesn't work (I don't know where it'll be located on Windows or OSX...),
you can run the monitor from Python terminal (or put the call in a script yourself):

>>> import SerialMonitor
>>> SerialMonitor.main()

There is a script ```runSerialMonitor``` provided which does exactly the above.

Tested on Ubuntu 16.04 with Pyton 2.7.12 and on Ubuntu 14.04 with Python 3.4.3.

GUI maintenance
================
The GUI was originally built with `wxFormbuilder 3.5.1
<https://github.com/wxFormBuilder/wxFormBuilder>`_.
It does not support the newest wxWidgets, it seems, but to install it on Ubuntu Linux:

    add-apt-repository ppa:wxformbuilder/release
    apt-get install wxformbuilder

**Further GUI edits should be done manually** on the ```serialMonitorBaseclasses.py```, until
wxFormBuilder starts to support wx4. Exporting the code from the form builder right now
will break the GUI.

Example
========

![Alt text](screenshot.png?raw=true "Main window of the program")
