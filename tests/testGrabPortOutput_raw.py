#!/usr/bin/python3
""" Test the SerialMonitor.grabPortOutput without using actual hardware.
Focus on the raw outputFormat.

.. module:: SerialMonitor
   :platform: Unix, Windows
   :synopsis: Trial automated testing of the message passing through a serial port.

.. moduleauthor:: Alek, Artur

"""
import unittest, time
import SerialMonitor as sm

TEST_PORT = 'loop://' # Type of the test port. This one is a simple RX <-> TX
	# type to be used for unit testing.
	# https://pyserial.readthedocs.io/en/latest/url_handlers.html#loop

class Tests(unittest.TestCase):

	def setUp(self):
		""" Prepare resources for testing. """
		import SerialMonitor as sm
		import time

		# Test port settings. Default and representative of what the SM does.
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

	def testRawEmptyMessage(self):
		""" Send an empty message with hex outputFormat. """
		notNeeded=self.fixture.read(1) # Empty the port.
		self.assertEqual(self.fixture.read(1),b'',
						msg='Need an empty bufferbefore running this test case.')
		# port.inWaiting will be 0, so grabPortOutput will just proceed to return
		# the input outputBuffer and the default (empty) output.
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		self.assertEqual(hexOutput[0],'',msg='Expected empty string as output.')
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0x00(self): #TODO
		""" Send a valid hex message. """
		self.fixture.write(b'\x00')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
		# Should just get whatever we've put in, but in a string representation of hex.
		self.assertEqual(hexOutput[0],hex(0x00),msg='Expected 0x00.')
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0x01(self): #TODO
		""" Send a valid hex message. """
		self.fixture.write(b'\x01')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
		# Should just get whatever we've put in, but in a string representation of hex.
		self.assertEqual(hexOutput[0],hex(0x01),msg='Expected 0x01.')
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0x41(self): #TODO
		""" Send a valid hex message, ASCII 'A'. """
		self.fixture.write(b'\x41')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
		# Should just get whatever we've put in, but in a string representation of hex.
		self.assertEqual(hexOutput[0],hex(0x41),msg="Expected 0x41 ('A').")
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0x41(self):
		""" Send a valid raw message, ASCII 'A'. """
		self.fixture.write(b'\x41')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should just get whatever we've put in, but in a string representation of hex.
		self.assertEqual(rawOutput[0],'A',msg="Expected 'A'.")
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	#TODO add some checks on other inputs
	#TODO test is port.inWaiting==0, should return the input outputBuffer - (empty dataStr) DONE
	#TODO test raw output with:
		# 1) valid and invalid ASCII characters,
		# 2) valid and invalid unicode characters,
		# 3) valid and invalid numbers,
		# 4) empty dataStr, - (port.inWaiting==0) DONE
		# 5) sequences of many bytes, incl. long integers.
	#TODO test formatted output with:
		# 1) valid and invalid ASCII characters,
		# 2) valid and invalid unicode characters,
		# 3) valid and invalid numbers,
		# 4) empty dataStr,
		# 5) valid and invalid formatitng of the dataStr,
		# 5) sequences of many bytes.
	#TODO should try sending various representations of the same bytes to make sure they're all understood.
if __name__ == '__main__':
	unittest.main()
