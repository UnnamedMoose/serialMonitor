#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2017 Artur K. Lidtke
---------------

Graphical interface program that allows the user to communicate with an
Arduino or other piece of hardware via a serial port.

Requires wxWidgets 2.8 or newer. To install on Ubuntu Linux:
    apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n libwxgtk2.8-dev libgtk2.0-dev

GUI built with wxFormbuilder 3.5.1 (https://github.com/wxFormBuilder/wxFormBuilder)
To install on Ubuntu Linux:
    add-apt-repository ppa:wxformbuilder/release
    apt-get install wxformbuilder

Tested on Ubuntu 14.04 with Pyton 2.7.6

---------------
Distributed under the MIT licence:

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import serialMonitorBaseClasses

import wx, string
import os, sys, time
import serial
import glob
import logging

# Create a logger for the application.
logger = logging.getLogger("SMLog") # It stands for Serial Monitor, right ;)
logger.setLevel(logging.INFO)
handler=logging.StreamHandler() # Will output to STDERR.
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
# TODO Attach the handler to the logger later, when user specifies the level.

class serialMonitorGuiMainFrame( serialMonitorBaseClasses.mainFrame ):

    #============================
    # CONSTRUCTOR
    #============================

    def __init__(self):
        """ Create the main frame, deriving from a baseline object which has all the panels, buttons, etc.
        already defined. """
        # initialise the underlying object
        serialMonitorBaseClasses.mainFrame.__init__( self, None )

        # File logger name.
        self.fileLoggerName=None # Overwrite with a file name when user chooses to log to a file.

        # serial communication
        self.portOpen = False # indicates if the serial communication port is open
        self.currentPort = 'None' # currently chosen port
        self.arduinoSerialConnection = 0 # holds the serial connection object once it has been initialised
        self.arduinoOutputBuffer = '' # buffer for storing inbound data if it arrives in chunks

        # set default values
        self.readDelay = int(self.readDelayTxtCtrl.GetValue())
        self.BaudRate = int(self.baudRateTxtCtrl.GetValue())

        # initialise the timing function for receiving the data from Arduino at a specific interval
        self.parseOutputsTimer.Start(int(self.readDelay))

        # update the ports available at start-up
        self.updatePorts(suppressWarn=True)
        self.portChoice.SetSelection(0)

        self.Layout() # Make sure everything is nicely located in the sizers on startup.

    #============================
    # EVENT HANDLING FUNCTIONS
    #============================

    def onClose(self, event):
        """ close the serial port before terminating, need to make sure it isn't left hanging """
        if self.portOpen:
            self.arduinoSerialConnection.close()
            logger.info('Disconnected from port before shutdown.')
        self.Destroy()

    def onSendInput(self, event):
        """ pass the message from the txtControl to the message parsing method that
        links with the comms protocol. """
        self.sendMessage( self.inputTextControl.GetLineText(0) )
        self.inputTextControl.Clear()

    def onChoseSerialPort(self, event):
        """ picks up the newly selected port and attempts to connect to Arduino via it """
        # ignore the None option
        if self.portChoice.GetStringSelection() != 'None':
            try:
                # don't re-open a working stream
                if self.portChoice.GetStringSelection() != self.currentPort:
                    # close any open ports if present
                    if self.portOpen:
                        self.arduinoSerialConnection.close()

                    self.arduinoSerialConnection = serial.Serial(self.portChoice.GetStringSelection(),
                                                                 self.BaudRate, timeout = 2)

                    if self.checkConnection():
                        self.portOpen = True
                        self.currentPort = self.portChoice.GetStringSelection()
                        logger.info('Connected to port {}'.format(self.currentPort))

            except:
                wx.MessageBox('Unknown problem occurred while establishing connection using the chosen port!', 'Error',
                          wx.OK | wx.ICON_ERROR)
                self.arduinoSerialConnection = 0
                self.portOpen = False
                self.updatePorts()
                logger.error('Failed to connect to a port.')

        # if None is chosen then close the current port
        else:
            self.disconnect()
            # if self.portOpen:
            #     self.arduinoSerialConnection.close()
            # self.arduinoSerialConnection = 0
            # self.portOpen = False
            # self.currentPort = 'None'

    def onUpdatePorts(self, event):
        """ call the update ports method - need a wrapper to be able to call it during initialisation """
        self.updatePorts()
        self.Layout() # makes sure the choice dropdown is big enough to fit all the choice options

    def onDisconnect(self, event):
        """ Call the disconnect method """
        self.disconnect()

    def onParseOutputs(self, event):
        """ Get information from the Arduino, if there is anything available """
        self.parseOutputs()

    def onUpdateBaudRate(self, event):
        """ Update the Baud rate but do not restart the connection; the change will take effect
        when the next connection gets established """
        # attempt to retrieve the entire contenst of the txtCtrl. If they are
        # an int, use them. otherwise, revert back to the old value and let the
        # user figure out they're making a mistake
        try:
            newValue = int(self.baudRateTxtCtrl.GetValue())
            self.BaudRate = newValue
        except ValueError:
            self.baudRateTxtCtrl.SetValue("{:d}".format(self.BaudRate))

    def onUpdateReadDelay(self, event):
        """ Update the rate at which outputs are being read from the serial port
        and restart the timer for the changes to take effect """
        try:
            newValue = int(self.readDelayTxtCtrl.GetValue())
            self.readDelay = newValue
            self.parseOutputsTimer.Start(int(self.readDelay))
        except ValueError:
            self.readDelayTxtCtrl.SetValue("{:d}".format(self.readDelay))

    def onClearConsole(self, event):
    	""" Clear the output/input console """
    	self.logFileTextControl.Clear()

    def onToggleLogFile(self, event):
        """ Open a log file if none is active, or close the existing one. """
        if self.fileLoggerName is None:
        	fileDialog=wx.FileDialog(self,"Choose log file",os.getcwd(),
        						    time.strftime("%Y%m%d%H%M%S_SM.log"),
        						    "Log files (*.log)|*.log",
		  		           		    wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        	fileDialog.ShowModal() # Wait for response.
        	self.fileLoggerName=fileDialog.GetPath() # User-chosen log file.
        	fileHandler=logging.FileHandler(self.fileLoggerName)
        	fileHandler.setFormatter(formatter) # Default log formatter.
        	logger.addHandler(fileHandler) # Already logs to STDERR, now also the file.
    	else:
        	# Remove the file handler from the logger.
        	for handler in logger.handlers:
        		if isinstance(handler,logging.FileHandler): # Only one file handler foreseen.
        			logger.removeHandler(handler)
        	self.fileLoggerName=None # Reset.

    #============================
    # OTHER FUNCTIONS
    #============================

    def getActivePorts(self):
		""" find the open ports - main part of the code from:
		http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
		"""
		if sys.platform.startswith('win'):
		    candidatePorts = ['COM' + str(i + 1) for i in range(256)]

		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		    candidatePorts = glob.glob('/dev/tty[A-Za-z]*')

		elif sys.platform.startswith('darwin'):
		    candidatePorts = glob.glob('/dev/tty.*')

		else:
		    raise EnvironmentError('Unsupported platform')

		ports = []
		for port in candidatePorts:
		    try:
		        s = serial.Serial(port)
		        s.close()
		        ports.append(port)
		    except (OSError, serial.SerialException):
		        pass

		return ports

    def updatePorts(self,suppressWarn=False):
        """ Checks the list of open serial ports and updates the internal list
        and the options shown in the dropdown selection menu.

        Args
        -----
        suppressWarn (bool): whether to suppress showing a wx.MessageBox with
        	a warning if no active ports are found.
    	"""

        # check what ports are currently open
        ports = self.getActivePorts()
        if (len(ports) <= 0) and not suppressWarn:
            wx.MessageBox('Check connection and port permissions.', 'Found no active ports!',
                wx.ICON_ERROR, None)

        # save current selection
        currentSelection = self.portChoice.GetStringSelection()

        # Remove the current options
        for i in range(len(self.portChoice.GetStrings())-1, -1, -1):
            self.portChoice.Delete(i)

        # add the newly found ports
        self.portChoice.Append('None')
        for port in ports:
            self.portChoice.Append(port)

        # attempt to return to the last selected port, use None if it's not found
        if currentSelection in ports:
            for i in range(len(ports)):
                if ports[i] == currentSelection:
                    self.portChoice.SetSelection(i+1)
        else:
            self.portChoice.SetSelection(0)
            self.currentPort = 'None'

    def disconnect(self):
        """ Drop the current connection with the Arduino """
        if self.portOpen:
            self.arduinoSerialConnection.close()
        self.arduinoSerialConnection = 0
        self.portOpen = False
        self.portChoice.SetSelection(0)
        self.currentPort = 'None'
        logger.info('User disconnected from port.')

    def checkConnection(self):
        """ Checks if the Arduino is still connected. """

        testMsgGood = True
        try:
            self.arduinoSerialConnection.inWaiting()
        except:
            testMsgGood = False

        if not self.arduinoSerialConnection or not self.arduinoSerialConnection.readable() or not testMsgGood:
            logger.error('Lost port connection.')
            wx.MessageBox('Arduino isn\'t readable! Check the connection...', 'Error',
                wx.OK | wx.ICON_ERROR)

            # close the connection
            self.arduinoSerialConnection.close()
            self.arduinoSerialConnection = 0
            self.portOpen = False
            self.currentPort = 'None'

            # check what ports are open - will set choice as None if current port has been lost
            self.updatePorts()

            return False
        else:
            return True

    def sendMessage(self, msg):
        """ Sends a message to the Arduino via the serila conneciton, but also takes
        care of any additional operations, such as logging the message

        Parameters
        ----------
            msg - string representation of the message to be sent
        """

        # make sure the connection has not been broken
        if self.portOpen:
            if self.checkConnection():
                # send the message; need to pass as a regular string to avoid compatibility
                # issues with new wxWidgets which use unicode string formatting
                self.arduinoSerialConnection.write(r'{}'.format(msg))
                # move to the end of the text control in case the user has clicked somewhere
                # since the last message
                self.logFileTextControl.MoveEnd()
                # add it to the port comms logger
                self.logFileTextControl.WriteText(msg+"\n")
                # scroll to the end
                self.logFileTextControl.ShowPosition(self.logFileTextControl.GetLastPosition())

    def parseOutputs(self):
        """ Check the serial connection for any inbound information and read it if it's
        available. Pass it to the respective handlers accordingly  """
        if self.portOpen:
            if self.checkConnection():
                # use a non-blocking approach to read the data - this is generally
                # much less disruptive to the overall program flow than relying
                # on Serial.readline()

                # if incoming bytes are waiting to be read from the serial input buffer
                if (self.arduinoSerialConnection.inWaiting()>0):
                    # Read the bytes.
                    dataStr=self.arduinoSerialConnection.read(
                        self.arduinoSerialConnection.inWaiting() )

                    # Pass to the buffer and convert from binary array to ASCII
                    # and split the output on EOL characters, unless the user
                    # desires to see the raw, undecoded output. In such case,
                    # don't expect end of line characters and replace unkown bytes
                    # with unicode replacement character. Also allow the user
                    # to see the hex code of the received bytes, not unicode.
                    if not self.rawOutputCheckbox.GetValue(): # No raw output.
                    	try:
			                self.arduinoOutputBuffer += dataStr.decode('ascii')

			                # extract any full lines and log them - there can be more than
			                # one, depending on the loop frequencies on either side of the
			                # serial conneciton
			                lines = self.arduinoOutputBuffer.rpartition("\n")
			                if lines[0]:
			                    for line in lines[0].split("\n"):
			                    	# go to the end of the console in case the user has moved the cursor
			                    	self.logFileTextControl.MoveEnd()
			                        # Write the line to text ctrl and log it.
			                        self.logFileTextControl.WriteText(line+"\n")
			                        logger.info(line)

			                        # TODO TODO TODO
			                        # this is where one can pass the outputs to where they need to go

			                    # scroll the output txtControl to the bottom
			                    self.logFileTextControl.ShowPosition(self.logFileTextControl.GetLastPosition())

			                    # only leave the last chunk without any EOL chars in the buffer
                                # this part of lines will contain no characters if full lines have
                                # been read or left-over pieces of a line that had not been fully
                                # sent when the outputBuffer was last refreshed - it is added at the
                                # beginning of the next stream of data
			                    self.arduinoOutputBuffer = lines[2]

                    	except UnicodeDecodeError as uderr:
					        # Sometimes rubbish gets fed to the serial port.
					        # Print the error in the console to let the user know something's not right.
					        self.logFileTextControl.MoveEnd()
					        self.logFileTextControl.BeginTextColour((255, 0, 0))
					        self.logFileTextControl.WriteText("!!!   ERROR DECODING ASCII STRING   !!!\n")
					        self.logFileTextControl.EndTextColour()

					        # Log the error and the line that caused it.
					        logger.warning('UnicodeDecodeError :( with string:\n\t{}'.format(dataStr))

                    elif not self.hexOutputCheckbox.GetValue(): # Raw but not hex ouptut.
	                    # Just print whatever came out of the serial port.
	                    # Writing unicode(dataStr) to logFileTextControl will sometimes
	                    # skip characters (e.g. for 0x00) and the remaining parts of the dataStr.
	                    # Write one character at the time and repalce invalid bytes manually.
	                    for c in dataStr:
	                        try:
	                            self.logFileTextControl.MoveEnd()
	                            self.logFileTextControl.WriteText(unicode(c,errors='strict'))
	                        except UnicodeDecodeError: # c was an unknown byte - replace it.
	                            self.logFileTextControl.MoveEnd()
	                            self.logFileTextControl.WriteText(u'\uFFFD')

	                    # Log the line that we received.
	                    logger.info(unicode(dataStr,errors='replace'))
	                    # Scroll the output txtControl to the bottom
	                    self.logFileTextControl.ShowPosition(self.logFileTextControl.GetLastPosition())

                    else: # Hex output.
	                    # Hex encoding of the datStr.
	                    hexDataStr=":".join("{:02x}".format(ord(c)) for c in dataStr)
	                    self.logFileTextControl.MoveEnd()
	                    self.logFileTextControl.WriteText(hexDataStr)
	                    # Log the line that we received.
	                    logger.info(hexDataStr)
	                    # Scroll the output txtControl to the bottom
	                    self.logFileTextControl.ShowPosition(self.logFileTextControl.GetLastPosition())

# implements the GUI class to run a wxApp
class serialMonitorGuiApp(wx.App):
    def OnInit(self):
        self.frame = serialMonitorGuiMainFrame()
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True

def main():
    """ Used by an entry-point script. """
    # need an environment variable on Ubuntu to make the menu bars show correctly
    env = os.environ
    if not(('UBUNTU_MENUPROXY' in env) and (env['UBUNTU_MENUPROXY'] == 0)):
        os.environ["UBUNTU_MENUPROXY"] = "0"

    # start the app
    app = serialMonitorGuiApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
