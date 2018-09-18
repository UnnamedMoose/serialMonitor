#!/usr/bin/python3.5
"""This is a first test that attempts to send messages from a remote terminal
to the SerialMonitor without using actual hardware.

.. module:: SerialMonitor
   :platform: Unix, Windows
   :synopsis: Trial automated testing of the message passing through a serial port.

.. moduleauthor:: Alek

"""
import unittest, serial, time
import SerialMonitor as sm

TEST_PORT = 'loop://' # Type of the test port. This one is a simple RX <-> TX
	# type to be used for unit testing.
	# https://pyserial.readthedocs.io/en/latest/url_handlers.html#loop

class Tests(unittest.TestCase):

	def setUp(self):
		"""Prepare resources for testing. """
		import SerialMonitor as sm
		import time

		# Test port settings. Very default and representative of what the SM does.
		self.BaudRate = 9600
		self.currentStopBits = sm.serial.STOPBITS_ONE
		self.currentParity = sm.serial.PARITY_EVEN
		self.currentByteSize = sm.serial.EIGHTBITS

		# Create a port that we'll write test messages into and see if the sm
		# responds correctly.
		self.fixture = sm.serial.serial_for_url(url=TEST_PORT,
												 baudrate=self.BaudRate,
												 timeout=2,
												 stopbits=self.currentStopBits,
												 parity=self.currentParity,
												 bytesize=self.currentByteSize
											 	)

	def tearDown(self):
		""" Done testing, get rid of the test resources."""
		del self.fixture

	def testEmptyPort(self):
		""" Port should be empty by default. """
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer.')

	def testSimpleMsg(self):
		""" Try to write and read a simple message. """
		self.fixture.write(b'HelloWorld')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		# Read more characters than have been sent, trigger timeout.
		self.assertEqual(self.fixture.read(10),b'HelloWorld',msg='Expected HelloWorld.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer.')

if __name__ == '__main__':
	unittest.main()
