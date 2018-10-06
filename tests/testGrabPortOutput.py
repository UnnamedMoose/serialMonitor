#!/usr/bin/python3
""" Test the SerialMonitor.grabPortOutput without using actual hardware.

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

	def testRaiseVE_InalidOutputFormat(self):
		""" Should raise VE for invalid outputFormat. """
		self.assertRaises(ValueError,sm.commsInterface.grabPortOutput,
			self.fixture,"DummyBuff","invalidFormat")

	def testDefaultRetType(self):
		""" Should return string, string, dict when there's no message. """
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,"DummyBuff",
														 "formatted")
		self.assertIs(type(formattedOutput),tuple,
			msg='Output not a tuple.')
		self.assertIs(type(formattedOutput[0]),str,
			msg='output not a string.')
		self.assertIs(type(formattedOutput[1]),str,
			msg='outputBuffer not a string.')
		self.assertIs(type(formattedOutput[2]),dict,
			msg='warningSummary not a dict.')

	def testFormattedRetType(self):
		""" Should return string, string, dict for formatted output. """
		self.fixture.write(b'HelloWorld') # The message cna be whatever, not testing it.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,"DummyBuff",
														 "formatted")
		self.assertIs(type(formattedOutput),tuple,
			msg='Output not a tuple.')
		self.assertIs(type(formattedOutput[0]),str,
			msg='output not a string.')
		self.assertIs(type(formattedOutput[1]),str,
			msg='outputBuffer not a string.')
		self.assertIs(type(formattedOutput[2]),dict,
			msg='warningSummary not a dict.')


	def testRawRetType(self):
		""" Should return string, string, dict for raw output. """
		self.fixture.write(b'HelloWorld') # The message cna be whatever, not testing it.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,"DummyBuff",
														 "raw")
		self.assertIs(type(formattedOutput),tuple,
			msg='Output not a tuple.')
		self.assertIs(type(formattedOutput[0]),str,
			msg='output not a string.')
		self.assertIs(type(formattedOutput[1]),str,
			msg='outputBuffer not a string.')
		self.assertIs(type(formattedOutput[2]),dict,
			msg='warningSummary not a dict.')

	def testHexRetType(self):
		""" Should return string, string, dict for hex output. """
		self.fixture.write(b'HelloWorld') # The message cna be whatever, not testing it.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,"DummyBuff",
														 "hex")
		self.assertIs(type(formattedOutput),tuple,
			msg='Output not a tuple.')
		self.assertIs(type(formattedOutput[0]),str,
			msg='output not a string.')
		self.assertIs(type(formattedOutput[1]),str,
			msg='outputBuffer not a string.')
		self.assertIs(type(formattedOutput[2]),dict,
			msg='warningSummary not a dict.')
	
	#TODO assert raises if outputFormat not in ['formatted', 'raw', 'hex']
	#TODO add some checks on other inputs
	#TODO test is port .inWaiting==0, should return the input outputBuffer
	#TODO test hex encoding with:
		# 1) valid and invalid ASCII characters,
		# 2) valid and invalid unicode characters,
		# 3) valid and invalid numbers,
		# 4) empty dataStr.
	#TODO test raw output with:
		# 1) valid and invalid ASCII characters,
		# 2) valid and invalid unicode characters,
		# 3) valid and invalid numbers,
		# 4) empty dataStr.
	#TODO test formatted output with:
		# 1) valid and invalid ASCII characters,
		# 2) valid and invalid unicode characters,
		# 3) valid and invalid numbers,
		# 4) empty dataStr,
		# 5) valid and invalid formatitng of the dataStr.
if __name__ == '__main__':
	unittest.main()
