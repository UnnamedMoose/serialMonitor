#!/usr/bin/python3
""" This unit test evaluates the connection status checking routine in the comms
interface. This is done by opening a known connection to a system port and checking
how the vertification routine responds to it.

.. module:: SerialMonitor
   :platform: Unix, Windows
   :synopsis: Trial automated testing of serial port status verification.

.. moduleauthor:: Artur

"""

import unittest

# Set up path to the SM module for a raw git clone instead of install
import sys
sys.path.append("../")

# modules used at the global level in the test functions
import SerialMonitor as sm
from SerialMonitor import commsInterface as comms

# ===
# set up a dummy object with identical bollean interfaces to a serial port
class dummyPort(object):
	def __init__(self, inWaiting=True, readable=True, own=True):
		self.inWaiting_ = inWaiting
		self.readable_ = readable
		self.own_ = own

	def inWaiting(self):
		if self.inWaiting_:
			return self.inWaiting_
		else:
			# TODO AL: check exactly what kind of error serial returns
			raise ValueError

	def readable(self):
		return self.readable_

	# for Python <3
	def __nonzero__(self):
		return self.own_
	# for Python 3+
	def __bool__(self):
		return self.own_

	def close(self):
		pass # do nothing

# ===
# test case definition
class Tests(unittest.TestCase):

	def setUp(self):
		""" Prepare resources for testing. """
		# import the modules to be tested
		import SerialMonitor as sm
		from SerialMonitor import commsInterface as comms

		# test port instance
		self.fixture = dummyPort()

	def tearDown(self):
		""" Done testing, get rid of the test resources."""
		del self.fixture

	def testHandshake(self):
		""" Check that the routine picks up on the inWaiting status of the port;
		for an open connection, this should always return True. """
		# set the port to a bad status
		self.fixture.inWaiting_ = False
		self.assertEqual(comms.checkConnection(self.fixture), False,
		msg="Expected invalid inWaiting status to cause check failure")
		# set the port to a good status
		self.fixture.inWaiting_ = True
		self.assertEqual(comms.checkConnection(self.fixture), True,
		msg="Expected valid inWaiting to yield an valid check.")

	def testIsReadable(self):
		""" Make sure that the readable() check works. """
		self.fixture.readable_ = False
		self.assertEqual(comms.checkConnection(self.fixture), False,
			msg="Expected invalid readable status to cause check failure")

		self.fixture.readable_ = True
		self.assertEqual(comms.checkConnection(self.fixture), True,
			msg="Expected valid readable to yield an valid check.")

	def testIsNonzero(self):
		""" Make sure that the __bool__/__nonzero__() check works. """
		self.fixture.own_ = False
		self.assertEqual(comms.checkConnection(self.fixture), False,
			msg="Expected invalid __bool__/__nonzero__ status to cause check failure")

		self.fixture.own_ = True
		self.assertEqual(comms.checkConnection(self.fixture), True,
			msg="Expected valid __bool__/__nonzero__ to yield an valid check.")

# ===
# run the tests
if __name__ == '__main__':
	unittest.main()
