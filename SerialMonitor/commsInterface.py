#!/bin/env/python3

import serial
import sys
import glob

def getActivePorts():
	""" Find the open serial ports and return as a list.

	Main part of the code from:
	http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

	Returns
    -------
    	(list) a list of strings denoting names of open ports.
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

def checkConnection(port):
	""" Check the serial port connection.

	Arguments
	---------
		port (serial.Serial) - instance of a port interface.

	Returns
	---------
		(bool) - status of the port (True means good connection)
	"""

	# first try a handshake
	testMsgGood = True
	try:
		port.inWaiting()
	except:
		testMsgGood = False

	# then try serial.Serial methods to establish if port's okay
	if (not port) or (not port.readable()) or (not testMsgGood):
		# close the connection if something went wrong
		port.close()

		# reutrn status
		return False
	else:
		return True

def grabPortOutput(port, outputBuffer, outputFormat):
	""" See if there is anything to read in the port and grab the outputs.

	The calling part of the code is responsible for checking the status of the
	connection. The grabed output is formatted into a string which can then
	be examined or parsed as needed.

	Arguments
	---------
		port (serial.Serial) - instance of a port interface.
		outputBuffer (string) - leftover contents of an incomplete message
			received during previous retrieval of output.
		outputFormat (string) - chosen formatting type, must be one of
			['formatted', 'raw', 'hex']

	Returns
	---------
		(string) - formatted output from the serial port.
		(string) - leftover buffer contents from a possible incomplete message
			received. Needs to be passed to the next call to avoid data loss.
		(dict) - summary of warnings and errors raised. These should be taken
			care of externally - this function tries its best not to fall over.
	"""

	# will hold any warnings encountered.
	warningSummary = {}
	# formatted output
	output = ""

	# check requested formatting
	if outputFormat not in ['formatted', 'raw', 'hex']:
		raise ValueError("Requested output format {} not supported.".format(outputFormat))

	# if incoming bytes are waiting to be read from the serial input buffer
	if (port.inWaiting() > 0):
		# Read the bytes.
		dataStr = port.read(port.inWaiting())

		# Pass to the buffer and convert from binary array to \n-separated ASCII,
		# unless the user desires to see the raw, undecoded output. In such case,
		# don't expect end of line characters and replace unkown bytes
		# with a unicode replacement character. Also allow the user
		# to see the hex code of the received bytes, not unicode.

		# Processed and (arguably) nicely formatted output.
		if outputFormat == "formatted":
			try:
				outputBuffer += dataStr.decode('ascii')

				# extract any full lines and log them - there can be more than
				# one, depending on the loop frequencies on either side of the
				# serial conneciton
				lines = outputBuffer.rpartition("\n")
				if lines[0]:
					for line in lines[0].split("\n"):
						output += "{}\n".format(line)

					# Keep the remaining output in buffer if there are no EOL characters
					# in it. This is useful if only part of a message was received on last
					# buffer update.
					outputBuffer = lines[2]

			except UnicodeDecodeError as uderr:
				# Sometimes rubbish gets fed to the serial port.
				# Log the error and the line that caused it.
				warningSummary["UnicodeDecodeError"] = \
					"UnicodeDecodeError :( with string:\n\t{}".format(dataStr)

		# Raw but not formatted output.
		elif outputFormat == "raw":
			# Just print whatever came out of the serial port as a string.
			# Converting dataStr to unicode used to sometimes skip characters
			# (e.g. for 0x00) and the remaining parts of the dataStr.
			# It would also cause UnicodeDecodeErrors, which were caught here and
			# the wrong bytes were replaced with u'\uFFFD'. In Python 3 this is
			# no longer necessary - all strings are unicode and the maximum range
			# of unicode codes (0x10FFFF) can't be exceeded with a single byte.
			for c in dataStr: # For every byte (dataStr is <class 'bytes'>)
				output += chr(c)

		# Hex output.
		else:
			# Take one byte at a time from dataStr (<class 'bytes'>) and format
			# it as a hex-code, e.g. 0x12 or 0x03. N.B. the leading '0' for
			# integers smaller than 0x0F+1=16. Need it to understand transactions
			# involving many bytes.
			output = ':'.join('0x'+c.to_bytes(1,'big',signed=False).hex() for c in dataStr)
#TODO for raw and hex output, outputBuffer makes no sense.
	return output, outputBuffer, warningSummary

#TODO Update the docs regarding the number of expected returned bytes.
