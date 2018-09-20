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
