#!/usr/bin/python3
""" Test the SerialMonitor.grabPortOutput without using actual hardware.
Focus on the formatted outputFormat.

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

	def testFormattedEmptyMessage(self):
		""" Send an empty message with formatted outputFormat. """
		notNeeded=self.fixture.read(1) # Empty the port.
		self.assertEqual(self.fixture.read(1),b'',
						msg='Need an empty buffer before running this test case.')
		# port.inWaiting will be 0, so grabPortOutput will just proceed to return
		# the input outputBuffer and the default (empty) output.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		self.assertEqual(formattedOutput[0],'',msg='Expected empty string as output.')
		self.assertEqual(formattedOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_0(self):
		""" Send a single formatted byte with two different representations of '0'. """
		self.fixture.write(b'\x00')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff\x00',msg='Expected DummyBuff\\x00.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'0')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff0',msg='Expected DummyBuff0.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_1(self):
		""" Send a single formatted byte with two different representations of '1'. """
		self.fixture.write(b'\x01')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff\x01',msg='Expected DummyBuff\\x01.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'1')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff1',msg='Expected DummyBuff1.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_0x41(self):
		""" Send a single formatted byte with two different representations of
		ASCII 'A' = 0x41. """
		self.fixture.write(b'\x41')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff\x41',msg='Expected DummyBuff\\x41.')
		self.assertEqual(formattedOutput[1],'DummyBuffA',msg='Expected DummyBuffA.') # Both representations work.
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'A')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuffA',msg='Expected DummyBuffA.')
		self.assertEqual(formattedOutput[1],'DummyBuff\x41',msg='Expected DummyBuff\\x41.') # Both representations work.
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_fullASCIITable(self):
		""" Send a valid formatted message, one valid ASCII byte at a time. Some will
		be sent and read as hex codes of bytes, others as ASCII characters. """
		for i in range(0,128): # From 0x00 (0) to 0x7F (127).
			# Avoid implicit casting in the serial module - need to send bytes.
			# Easiest to convert int i to ASCII and then to bytes.
			self.fixture.write(bytes(chr(i),'ASCII'))
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
			# print(i,formattedOutput[0],bytes(chr(i),'ASCII'),chr(i)) # To eyeball the results.
			if i != 10:
				# output will be empty if there is no EOL termination of the message.
				self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
				# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
				self.assertEqual(formattedOutput[1],'DummyBuff'+chr(i),
					msg='Expected DummyBuff{}.'.format(chr(i)))
			else: # We terminated the message because 0x41='\n'
				# Will move input outputBuffer to output and append nothing to it -
				# only one complete line has been sent.
				self.assertEqual(formattedOutput[0],'DummyBuff\n',msg='Expected DummyBuff\\n in output.')
				self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer')
			# Should have no warnings.
			self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	# port.inWaiting==0, should return the input outputBuffer - (empty dataStr)     DONE
	#TODO test formatted output with:
		# 1) valid ASCII characters,                                                DONE
		# 2) invalid ASCII characters,                                              _
		# 3) valid numbers,                                                         DONE
		# 4) empty dataStr,                                                         DONE
		# 5) valid and invalid formatitng of the dataStr,                           _
		# 5) sequences of many bytes.                                               _
	#TODO should try sending various representations of the same bytes to make      _
	    # sure they're all understood.
	#TODO send single bytes in various representations w/ EOL termination.

if __name__ == '__main__':
	unittest.main()
