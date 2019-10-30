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
	connection. The grabbed output is formatted into a string which can then
	be examined or parsed as needed.

	Support different formatting types, which depend on the supplied `outputFormat`
	argument:
	* raw - convert bytes from the `port` into `str` (unicode) one byte at a time,
	* hex - convert all bytes from the `port` into `str` containing hex-codes of
	  the individual bytes, e.g. 0x00:0x01:0x0a,
	* formatted - expect the bytes in the `port` to contain end-of-line characters
	  ('\n'), which will be used to split the bytes into lines. If the last line
	  is incomplete, it will be returned in `outputBuffer`. For `hex` and `raw`
	  formatting types, `outputBuffer` is not used.

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

	Raises
	---------
		ValueError - when supplied `outputFormat` is not supported.
		TypeError - when `port` or `outputBuffer` are not of expected types
		(serial.SerialBase and str, respectively).
	"""

	# will hold any warnings encountered.
	warningSummary = {}
	# formatted output
	output = ""

	# Check requested formatting and other input types.
	if outputFormat not in ['formatted', 'raw', 'hex']:
		raise ValueError("Requested output format {} not supported.".format(outputFormat))

	if not isinstance(port,serial.SerialBase):
		raise TypeError('Expected port of type serial.serialposix.Serial,\
		 got {} instead.'.format(type(port)))

	if not isinstance(outputBuffer,str):
		raise TypeError('Expected outputBuffer of type str, got {}\
		 instead.'.format(type(outputBuffer)))

	# if incoming bytes are waiting to be read from the serial input buffer
	if (port.inWaiting() > 0):
		# Read the bytes (dataStr is <class 'bytes'>).
		dataStr = port.read(port.inWaiting())

		# Pass to the buffer and convert from binary array to \n-separated ASCII,
		# unless the user desires to see the raw, undecoded output. In such case,
		# don't expect end of line characters. Also allow the user to see the
		# hex codes of the received bytes, not the corresponding unicode characters.

		# Processed and (arguably) nicely formatted output.
		if outputFormat == "formatted":
			# Trying to decode the entire dataStr to ASCII will discard all the
			# bytes contained therein even if only one of them is invalid. Thus,
			# go through each byte in dataStr one by one.
			for i in range(len(dataStr)): # Need the index of the bye to cast an error, if need be.
				try:
					if dataStr[i] < 128: # Valid ASCII character.
						outputBuffer += chr(dataStr[i])
					else: # Not in ASCII range. chr() will cope with this becuase
						# it convers to Unicode, which has a larger range but here
						# we specifically want ASCII.
						raise UnicodeDecodeError('SM',dataStr,i,i+1,'Outside of ASCII range, i.e. >=128.')
				except UnicodeDecodeError as uderr:
					# Sometimes rubbish gets fed to the serial port.
					# Log the error and the line that caused it. Include index
					# of every error to keep track of all the encountered errors.
					warningSummary['UnicodeDecodeError{}'.format(len(warningSummary))] = \
					'UnicodeDecodeError :( with character:\n\t{}'.format(dataStr[i])

			# Extract any full lines and log them - there can be more than
			# one, depending on the loop frequencies on either side of the
			# serial conneciton
			lines = outputBuffer.rpartition("\n")
			if lines[0]: # lines[0] = complete lines terminated with '\n'.
				for line in lines[0].split("\n"):
					output += "{}\n".format(line)

				# Keep the remaining output in buffer if there are no EOL characters
				# in it. This is useful if only part of a message was received on last
				# buffer update.
				outputBuffer = lines[2] # lines[2] = Remainder after the
					# last '\n' and not terminated with '\n'.
					# lines[1] = '\n'

		# Raw but not formatted output.
		elif outputFormat == "raw":
			# Just print whatever came out of the serial port as a string.
			# Converting dataStr to unicode used to sometimes skip characters
			# (e.g. for 0x00) and the remaining parts of the dataStr.
			# It would also cause UnicodeDecodeErrors, which were caught here and
			# the wrong bytes were replaced with u'\uFFFD'. In Python 3, this is
			# no longer necessary - all strings are unicode and the maximum range
			# of unicode codes (0x10FFFF) can't be exceeded with a single byte.
			for c in dataStr: # For every byte (dataStr is <class 'bytes'>)
				output += chr(c) # Convert one byte at a time.

		# Hex output.
		else:
			# Take one byte at a time from dataStr (<class 'bytes'>) and format
			# it as a hex-code, e.g. 0x12 or 0x03. Iterating over dataStr will
			# produce single integers (<class 'int'>). Separate consecutive bytes
			# with ':'.
			# NOTE 1 - there's a leading '0' for integers smaller than 0x0F+1=16.
			#          Need it to understand transmissions involving many bytes.
			# NOTE 2 - because we process one byte at a time, endian doesn't matter;
			#          big or small will yield the same *single* byte.
			# NOTE 3 - there will be no leading or trailing colon (':').
			output = ':'.join('0x'+c.to_bytes(1,'big',signed=False).hex() for c in dataStr)
#TODO for raw and hex output, outputBuffer makes no sense.
	return output, outputBuffer, warningSummary
