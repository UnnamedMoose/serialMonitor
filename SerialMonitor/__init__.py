#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2017-2018 Artur K. Lidtke and Aleksander Lidtke
---------------

Graphical interface program that allows the user to communicate with an
Arduino or other piece of hardware via a serial port.

GUI built with wxFormbuilder 3.5.1 (https://github.com/wxFormBuilder/wxFormBuilder)
To install on Ubuntu Linux:
    add-apt-repository ppa:wxformbuilder/release
    apt-get install wxformbuilder

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

import SerialMonitor.serialMonitorBaseClasses as baseClasses
import SerialMonitor.commsInterface as commsInterface

import wx, string
import os, sys, time
import serial
import glob
import logging

# Set the module version consistent with pip freeze. Handle exception if didn't
# install with pip
import pkg_resources as pkg
try:
    __version__ = pkg.get_distribution("SerialMonitor").version.lstrip('-').rstrip('-')
except:
    __version__ = "unknown_version"

# Create a logger for the application.
logger = logging.getLogger("SMLog") # It stands for Serial Monitor, right ;)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # Will output to STDERR.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
# TODO Attach the handler to the logger later, when user specifies the level.

class PleaseReconnectDialog(wx.Dialog):
    def __init__(self,parent):
        """ Tells the user to reconnect to the serial port for the new connection
        settings to take effect."""
        wx.Dialog.__init__(self,parent,-1,'Please reconnect',size=(300,120))
        self.CenterOnScreen(wx.BOTH)

        okButton = wx.Button(self, wx.ID_OK, 'OK')
        okButton.SetDefault()
        text = wx.StaticText(self, -1, 'Please reconnect to the serial port for the changes to take effect.')

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(text, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox.Add(okButton, 1, wx.ALIGN_CENTER|wx.BOTTOM, 10)
        self.SetSizer(vbox)

class serialDetailsDialog( baseClasses.serialDetailsDialog ):
    def __init__(self, parent, currentStopBits, currentParity, currentByteSize):
        """ Parent is the parent object, currentStopBits, currentPartiy and
        currentByte size are the currently used serial.Serial settings, which
        will be selected when the dialog is opened.
        """
        # initialise the underlying object
        baseClasses.serialDetailsDialog.__init__( self, parent )

        # create bespoke fields for holding the vailable choices
        self.stopBitsChoices = []
        self.parityChoices = []
        self.byteSizeChoices = []

        # Add the selections to the dropdown menus (defined by the pySerial module).
        for stopBit in serial.Serial.STOPBITS:
            self.stopBitsChoice.Append(str(stopBit))
            self.stopBitsChoices.append(stopBit)
        self.stopBitsChoice.SetSelection(self.stopBitsChoices.index(currentStopBits))

        for key, val in serial.PARITY_NAMES.items():
            self.parityChoice.Append(val)
            self.parityChoices.append(key)
        self.parityChoice.SetSelection(self.parityChoices.index(currentParity))

        for byteSize in serial.Serial.BYTESIZES:
            self.byteSizeChoice.Append(str(byteSize))
            self.byteSizeChoices.append(byteSize)
        self.byteSizeChoice.SetSelection(self.byteSizeChoices.index(currentByteSize))

class serialMonitorGuiMainFrame( baseClasses.mainFrame ):

    #============================
    # CONSTRUCTOR
    #============================

    def __init__(self):
        """ Create the main frame, deriving from a baseline object which has all the panels, buttons, etc.
        already defined. """
        # initialise the underlying object
        baseClasses.mainFrame.__init__(self, None)

        # File logger name.
        self.fileLoggerName = None # Overwrite with a file name when user chooses to log to a file.

        # serial communication
        self.portOpen = False # indicates if the serial communication port is open
        self.currentPort = 'None' # currently chosen port
        self.currentSerialConnection = 0 # holds the serial connection object once it has been initialised
        self.serialOutputBuffer = '' # buffer for storing inbound data if it arrives in chunks

        # set default values
        self.readDelay = int(self.readDelayTxtCtrl.GetValue())
        self.BaudRate = int(self.baudRateTxtCtrl.GetValue())

        # No raw output so hexOutputCheckbox checkbox won't change anything.
        # Disable it not to confuse the users.
        self.hexOutputCheckbox.Enable(False)

        # Current serial connection details.
        self.currentStopBits = serial.STOPBITS_ONE
        self.currentParity = serial.PARITY_NONE
        self.currentByteSize = serial.EIGHTBITS

        # initialise the timing function for receiving the data from the serial port at a specific interval
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
            self.currentSerialConnection.close()
            logger.info('Disconnected from port before shutdown.')
        self.Destroy()

    def onSendInput(self, event):
        """ pass the message from the txtControl to the message parsing method that
        links with the comms protocol. """
        self.sendMessage( self.inputTextControl.GetLineText(0) )
        self.inputTextControl.Clear()

    def onChoseSerialPort(self, event):
        """ picks up the newly selected port and attempts to connect to a peripheral device via it """
        logger.debug('Choosing serial port.')
        # ignore the None option
        if self.portChoice.GetStringSelection() != 'None':
            try:
                # don't re-open a working stream
                if self.portChoice.GetStringSelection() != self.currentPort:
                    # close any open ports if present
                    if self.portOpen:
                        self.currentSerialConnection.close()

                    self.currentSerialConnection = serial.Serial(port=self.portChoice.GetStringSelection(),
                                                                 baudrate=self.BaudRate,
                                                                 timeout=2,
                                                                 stopbits=self.currentStopBits,
                                                                 parity=self.currentParity,
                                                                 bytesize=self.currentByteSize)

                    logger.debug('Checking {}'.format(self.currentSerialConnection))
                    if self.checkConnection(): # Try to connnect to the user-selected port.
                        self.portOpen = True
                        self.currentPort = self.portChoice.GetStringSelection()
                        logger.info('Connected to port {}'.format(self.currentPort))
                        # To verify the setting of the serial connection details.
                        logger.debug('baud={},stop bits={},parity={},byte size={}'.format(
                            self.currentSerialConnection.baudrate,
                            self.currentSerialConnection.stopbits,
                            self.currentSerialConnection.parity,
                            self.currentSerialConnection.bytesize,))
                    else: # Something's wrong, couldn't connect.
                        wx.MessageBox('Cannot connect to port {}.'.format(
                            self.portChoice.GetStringSelection()), 'Error',
                            wx.OK | wx.ICON_ERROR)
                        logger.error('Could not connect to port {}'.format(
                            self.portChoice.GetStringSelection()))
                        self.currentSerialConnection = 0
                        self.portOpen = False
                        self.updatePorts()
                        self.portChoice.SetSelection(0) # Go back to 'None' selection.

            except BaseException as unknonwError:
                wx.MessageBox('Unknown problem occurred while establishing connection using the chosen port!', 'Error',
                          wx.OK | wx.ICON_ERROR)
                self.currentSerialConnection = 0
                self.portOpen = False
                self.updatePorts()
                self.portChoice.SetSelection(0) # Go back to 'None' selection.
                logger.error('Failed to connect to a port due to {}.'.format(unknonwError))

        # if None is chosen then close the current port
        else:
            self.disconnect()

    def onUpdatePorts(self, event):
        """ call the update ports method - need a wrapper to be able to call it during initialisation """
        logger.debug('Attempting to update avaialble ports.')
        self.updatePorts()
        self.Layout() # makes sure the choice dropdown is big enough to fit all the choice options

    def onDisconnect(self, event):
        """ Call the disconnect method """
        self.disconnect()

    def onParseOutputs(self, event):
        """ Get information from the data received via the serial port, if there is anything available """
        self.parseOutputs()

    def onUpdateBaudRate(self, event):
        """ Update the Baud rate but do not restart the connection; the change will take effect
        when the next connection gets established """
        # attempt to retrieve the entire contenst of the txtCtrl. If they are
        # an int, use them. otherwise, revert back to the old value and let the
        # user figure out they're making a mistake
        logger.debug('Attempting to update baud rate.')
        try:
            newValue = int(self.baudRateTxtCtrl.GetValue())
            self.BaudRate = newValue
            self.notifyToReconnect() # Some people are confused about how this works.
        except ValueError:
            self.baudRateTxtCtrl.SetValue("{:d}".format(self.BaudRate))
            wx.MessageBox('Please specify integer baud rate','Incorrect baud rate',
                wx.OK | wx.ICON_WARNING)

    def onUpdateReadDelay(self, event):
        """ Update the rate at which outputs are being read from the serial port
        and restart the timer for the changes to take effect """
        logger.debug('Attempting to update read delay.')
        try:
            newValue = int(self.readDelayTxtCtrl.GetValue())
            self.readDelay = newValue
            self.parseOutputsTimer.Start(int(self.readDelay))
            logger.info('Changed read delay to {} ms.'.format(self.readDelay))
        except ValueError as ve:
            self.readDelayTxtCtrl.SetValue("{:d}".format(self.readDelay))
            logger.error('ValueError while updating read delay: {}'.format(ve))

    def onClearConsole(self, event):
        """ Clear the output/input console """
        logger.debug('Console cleared.')
        self.logFileTextControl.Clear()

    def onToggleLogFile(self, event):
        """ Open a log file if none is active, or close the existing one. """
        logger.debug('Attempting to open a log file.')

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
            dlg=wx.MessageDialog(self,"Stop logging?","Stop",wx.YES_NO|wx.ICON_QUESTION)
            if dlg.ShowModal()==wx.ID_YES: # Avoid accidental log termination.
                # Remove the file handler from the logger.
                for handler in logger.handlers:
                    if isinstance(handler,logging.FileHandler): # Only one file handler foreseen.
                        logger.removeHandler(handler)
                self.fileLoggerName=None # Reset.
            else: # The checkbox should still be checked if we don't stop logging.
                self.fileLogCheckbox.SetValue(True)

    def onRawOutputTicked(self, event):
        """ Raw output checkbox status defines whether hex output can also be
        enabled or not. Grey it out when it won't affect the program not to
        confuse the users. """
        logger.debug('Raw output ticked: {}. Current raw output state: {}.'.format(
            event.IsChecked(),self.hexOutputCheckbox.GetValue()))

        if event.IsChecked(): # Hex output can now be enabled.
            self.hexOutputCheckbox.Enable(True)
        else: # Now hex output won't change anything.
            self.hexOutputCheckbox.Enable(False) # Grey it out.
            # Upon re-enabling raw output start from the default state of the hex output, too.
            self.hexOutputCheckbox.SetValue(False)

    def onEditSerialPort( self, event ):
        """ Edit the more fine details of the serial connection, like the parity
        or the stopbits. """
        logger.debug('Attempting to edit serial connection details.')
        # Main frame is the parent of this.
        serialDialog = serialDetailsDialog(self, self.currentStopBits,
            self.currentParity, self.currentByteSize)
        result = serialDialog.ShowModal() # Need a user to click OK or cancel.
        if result == wx.ID_OK: # User selected new settings so change the current defaults.
            self.currentStopBits = serialDialog.stopBitsChoices[serialDialog.stopBitsChoice.GetSelection()]
            self.currentParity = serialDialog.parityChoices[serialDialog.parityChoice.GetSelection()]
            self.currentByteSize = serialDialog.byteSizeChoices[serialDialog.byteSizeChoice.GetSelection()]
            logger.debug('Changed serial settings to: stop bits={}, parity={}, byte size={}'.format(
                self.currentStopBits,self.currentParity,self.currentByteSize))
            # Tell the user to reconnect for changes to take effect.
            self.notifyToReconnect()
        else: # Nothing's changed.
            pass

    #============================
    # OTHER FUNCTIONS
    #============================

    def updatePorts(self, suppressWarn=False):
        """ Checks the list of open serial ports and updates the internal list
        and the options shown in the dropdown selection menu.

        Args
        -----
        suppressWarn (bool): whether to suppress showing a wx.MessageBox with
            a warning if no active ports are found.
        """

        # check what ports are currently open
        ports = commsInterface.getActivePorts()
        if len(ports) <= 0 and not suppressWarn:
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
        """ Drop the current connection with the serial port """
        if self.portOpen:
            self.currentSerialConnection.close()
        self.currentSerialConnection = 0
        self.portOpen = False
        self.portChoice.SetSelection(0)
        self.currentPort = 'None'
        logger.info('User disconnected from port.')

    def checkConnection(self):
        """ Checks if there is anything still connected to the port.

		Returns
		-------
		True if `self.currentSerialConnection` port is readable, False otherwise.
		"""

        if not commsInterface.checkConnection(self.currentSerialConnection):
            # handle all internal nuts and bolts related to the connection
            # by setting them back to defaults.
            self.currentSerialConnection = 0
            self.portOpen = False
            self.currentPort = 'None'
            # let the user know something's wrong
            logger.error('Lost port connection.')
            wx.MessageBox('Port isn\'t readable! Check the connection...', 'Error',
                wx.OK | wx.ICON_ERROR)
            # check what ports are open once the user has had a chance to react.
            self.updatePorts()
            return False
        else: # All is good.
            return True

    def writeToTextBox(self, msg, prepend="", colour=(0,0,0)):
        """ Log a message inside the main text display window.

        Refreshes the position inside the text box, writes the message, and sets
        the cursour at the end of the text box to avoid issues with the user
        accidentally clicking somewhere and disturbing the output process.

        Arguments
        ---------
            msg (string) - string representation of the message to be shown

        Optional
        ---------
            prepend (string, default empty) - how to prepend the message, useful
                for highlighting e.g. in/out directions, etc.
            colour (int tuple, len=3, default=(0,0,0)) - RGB colour of text
        """

        # Move the cursor to the end of the box
        self.logFileTextControl.MoveEnd()

        # Set colour if needed
        if colour != (0,0,0):
            self.logFileTextControl.BeginTextColour(colour)

		# Write the message, with a preamble if desired.
        if len(prepend) > 0:
            prepend = "{}".format(prepend) # Format the desired preamble nicely.
        self.logFileTextControl.WriteText(r'{}{}'.format(prepend, msg))

		# Scroll to the end of the box.
        self.logFileTextControl.ShowPosition(self.logFileTextControl.GetLastPosition())

        # Re-set colour to default but only if it's been changed to avoid WX
		# warning 'Debug: Too many EndStyle calls!"'.
        if colour != (0,0,0):
            self.logFileTextControl.EndTextColour()

    def sendMessage(self, msg):
        """ Sends a message to the port via the serial conneciton, but also takes
        care of any additional operations, such as logging the message.

        Arguments
        ---------
            msg (string) - representation of the message to be sent
        """

        # make sure the connection has not been broken
        if self.portOpen:
            if self.checkConnection():
                # Send the message; need to pass as a regular string to avoid compatibility
                # issues with new wxWidgets which use unicode string formatting
                # Convert msg to bytes, then pass to serial.
                self.currentSerialConnection.write(msg.encode('utf-8'))
                # Log in the main display box in new line and in blue to make sure it stands out.
                self.writeToTextBox(msg+'\n',prepend='\nOUT: ',colour=(0,0,255))
                # Log the sent command.
                logger.info(r'OUT: {}'.format(msg))

    def parseOutputs(self):
        """ Check the serial connection for any inbound information and read it if it's
        available. Pass it to the respective handlers accordingly. """
        if self.portOpen:
            if self.checkConnection():
                # # if incoming bytes are waiting to be read from the serial input buffer
                # if (self.currentSerialConnection.inWaiting() > 0):
                #     # Read the bytes.
                #     dataStr = self.currentSerialConnection.read(
                #         self.currentSerialConnection.inWaiting() )
                #
                #     # Pass to the buffer and convert from binary array to ASCII
                #     # and split the output on EOL characters, unless the user
                #     # desires to see the raw, undecoded output. In such case,
                #     # don't expect end of line characters and replace unkown bytes
                #     # with unicode replacement character. Also allow the user
                #     # to see the hex code of the received bytes, not unicode.
                #
                #     # Processed and (arguably) nicely formatted output.
                #     if not self.rawOutputCheckbox.GetValue():
                #         try:
                #             self.serialOutputBuffer += dataStr.decode('ascii')
                #
                #             # extract any full lines and log them - there can be more than
                #             # one, depending on the loop frequencies on either side of the
                #             # serial conneciton
                #             lines = self.serialOutputBuffer.rpartition("\n")
                #             if lines[0]:
                #                 for line in lines[0].split("\n"):
                #                     # Write the line to text ctrl and log it.
                #                     self.writeToTextBox(msg+"\n")
                #                     logger.info(line)
                #
                #                     # this is where one can pass the outputs to where they need to go
                #
                #                 # Keep the remaining output in buffer if there are no EOL characters
                #                 # in it. This is useful if only part of a message was received on last
                #                 # buffer update.
                #                 self.serialOutputBuffer = lines[2]
                #
                #         except UnicodeDecodeError as uderr:
                #             # Sometimes rubbish gets fed to the serial port.
                #             # Print the error in the console to let the user know something's not right.
                #             self.writeToTextBox("!!!   ERROR DECODING ASCII STRING   !!!\n", colour=(255,0,0))
                #             # Log the error and the line that caused it.
                #             logger.warning('UnicodeDecodeError :( with string:\n\t{}'.format(dataStr))
                #
                #     # Raw but not formatted output.
                #     elif not self.hexOutputCheckbox.GetValue():
                #         # Just print whatever came out of the serial port.
                #         # Writing unicode(dataStr) to logFileTextControl will sometimes
                #         # skip characters (e.g. for 0x00) and the remaining parts of the dataStr.
                #         # Write one character at the time and repalce invalid bytes manually.
                #         for c in dataStr:
                #             try:
                #                 self.writeToTextBox(chr(c))
                #
                #             # c was an unknown byte - replace it.
                #             except UnicodeDecodeError:
                #                 self.writeToTextBox(u'\uFFFD')
                #
                #         # Log the line that we received.
                #         logger.info(str(dataStr))
                #
                #     else: # Hex output.
                #         # Hex encoding of the datStr.
                #         hexDataStr = ":".join("{}".format(hex(c)) for c in dataStr)
                #         self.writeToTextBox(hexDataStr)
                #         logger.info(hexDataStr)

                # see in what format to request data
                if not self.rawOutputCheckbox.GetValue():
                    outputFormat = "formatted"
                elif not self.hexOutputCheckbox.GetValue():
                    outputFormat = "raw"
                else:
                    outputFormat = "hex"

                # grab the outputs
                output, self.serialOutputBuffer, warningSummary = commsInterface.grabPortOutput(
                    self.currentSerialConnection, self.serialOutputBuffer, outputFormat)

                # Log and print received data in the text box. output is a string,
				# which is Unicode in Python 3, so no need to cast.
				# Only print when there is some message to avoid spamming the logs
				# with empty lines.
                if len(output) > 0:
                    self.writeToTextBox(output)
                    logger.info(output)

                # Log and print (in red) warnings, if there are any.
                if len(warningSummary) > 0:
                    for w in warningSummary:
                        self.writeToTextBox("{}, check the log!\n".format(w), colour=(255,0,0))
                        logger.warning(warningSummary[w])

    def notifyToReconnect(self):
        """ Notify the user to reconnect to the serial port for the changes they've
        made to take effect by opening a dialog. It'll automatically disappear
        after two seconds. """
        reconnectInfoDialog = PleaseReconnectDialog(self)
        # Automatically close after some time.
        wx.CallLater(2000, reconnectInfoDialog.Destroy)
        reconnectInfoDialog.ShowModal()

# implements the GUI class to run a wxApp
class serialMonitorGuiApp(wx.App):
    def OnInit(self):
#TODO Maybe should call the parent wx.App.OnInit method here?
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
