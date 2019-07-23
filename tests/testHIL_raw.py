#!/usr/bin/python3
""" Test the SerialMonitor.grabPortOutput by talking to an Arduino that is
programmed to reply with known data to specific commands. This test verifies
that the data are correctly received and interpreted.

.. module:: SerialMonitor
   :platform: Unix, Windows
   :synopsis: Automated testing of the SerialMonitor with an Arduino.

.. moduleauthor:: Alek, Artur

"""
import unittest, time
import SerialMonitor as sm

TEST_PORT = 'loop://' # Type of the test port. This one is a simple RX <-> TX
	# type to be used for unit testing.
	# https://pyserial.readthedocs.io/en/latest/url_handlers.html#loop

TIMEOUT = 20 # Will wait for data to come from the Arduino TIMEOUT*100 ms.

class Tests(unittest.TestCase):

	def setUp(self):
		""" Prepare resources for testing. """
		import SerialMonitor as sm
		import time

		# Test port settings. Default and representative of what the SM does.
		self.BaudRate = 9600
		self.currentStopBits = sm.serial.STOPBITS_ONE
		self.currentParity = sm.serial.PARITY_NONE
		self.currentByteSize = sm.serial.EIGHTBITS

		# See what ports we've got active.
		ports = sm.commsInterface.getActivePorts()
		if len(ports)<1:
			raise BaseException('No active ports, connect the Arduino!')

		# Open a port that we'll use to communicate with the Arduino. Assume it's
		# the only currently connected device, hence use ports[0].
		self.fixture = sm.serial.Serial(port=ports[0],
										baudrate=self.BaudRate,
										timeout=2,
										stopbits=self.currentStopBits,
										parity=self.currentParity,
										bytesize=self.currentByteSize)

		# Check that the port is readable.
		time.sleep(2) # Need to let the things settle a bit. 1 second won't work.
		if not sm.commsInterface.checkConnection(self.fixture):
			self.fixture.close()
			raise BaseException('Port {} is unreadable.'.format(self.fixture.port))

		# Check that the Arduino replies with the expected message.
		self.fixture.write(b'0') # Send the command byte.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		self.assertEqual(self.fixture.read(20),b'Arduino reachable.',
						msg="Arduino hasn't replied with the expected string to the test command.")

	def tearDown(self):
		""" Done testing, get rid of the test resources."""
		self.fixture.close()
		del self.fixture

	def testRawEmptyMessage(self):
		""" Send an empty message with raw outputFormat. """
		notNeeded=self.fixture.read(1) # Empty the port.
		self.assertEqual(self.fixture.read(1),b'',
						msg='Need an empty buffer before running this test case.')
		# port.inWaiting will be 0, so grabPortOutput will just proceed to return
		# the input outputBuffer and the default (empty) output.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		self.assertEqual(rawOutput[0],'',msg='Expected empty string as output.')
		self.assertEqual(len(rawOutput[0]),0,msg='Expected zero bytes.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Check message length.
		self.assertEqual(len(rawOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(rawOutput[1]),9,msg='Expected nine bytes')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testRawGoodByte_0(self):
		""" Send a three bytes with three different representations of '0'. """
		self.fixture.write(b'Z') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get '0'00 (ASCII and two integers) in a raw string representation.
		self.assertEqual(rawOutput[0],'0\x00\x00',msg="Expected '0'\\x00\\x00 ('0'00).")
		self.assertEqual(len(rawOutput[0]),3,msg='Expected three bytes.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		# Verify casting of the received bytes to integers.
		for i in range(len(rawOutput[0])): # Already asserted it's three bytes. Use it.
			self.assertTrue(type(rawOutput[0][i])==str,'rawOutput[0][{}] is not string.'.format(i))
		tempInt=int(rawOutput[0][0]) # Cast the unicode string to integer.
		self.assertEqual(tempInt,0,msg='tempInt != 0.')
		tempInt=int.from_bytes(bytes(rawOutput[0][1],'ASCII'), # Cast str to bytes, and bytes to int.
				byteorder='little',signed=False)
		self.assertEqual(tempInt,0,msg='tempInt != 0.')
		tempInt=int.from_bytes(bytes(rawOutput[0][2],'ASCII'), # Cast str to bytes, and bytes to int.
				byteorder='little',signed=False)
		self.assertEqual(tempInt,0,msg='tempInt != 0.')

	def testRawGoodByte_1(self):
		""" Send a three bytes with three different representations of '1'. """
		self.fixture.write(b'O') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get '1'11 (ASCII and two integers) in a raw string representation.
		self.assertEqual(rawOutput[0],'1\x01\x01',msg="Expected '1'\\x01\\x01 ('1'11).")
		self.assertEqual(len(rawOutput[0]),3,msg='Expected three bytes.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		# Verify casting of the received bytes to integers.
		for i in range(len(rawOutput[0])): # Already asserted it's three bytes. Use it.
			self.assertTrue(type(rawOutput[0][i])==str,'rawOutput[0][{}] is not string.'.format(i))
		tempInt=int(rawOutput[0][0]) # Cast the unicode string to integer.
		self.assertEqual(tempInt,1,msg='tempInt != 1.')
		tempInt=int.from_bytes(bytes(rawOutput[0][1],'ASCII'), # Cast str to bytes, and bytes to int.
				byteorder='little',signed=False)
		self.assertEqual(tempInt,1,msg='tempInt != 1.')
		tempInt=int.from_bytes(bytes(rawOutput[0][2],'ASCII'), # Cast str to bytes, and bytes to int.
				byteorder='little',signed=False)
		self.assertEqual(tempInt,1,msg='tempInt != 1.')

	def testRawGoodByte_0x41(self):
		""" Send three raw bytes with three different representations of
		ASCII 'A' = 0x41 = 65. """
		self.fixture.write(b'A') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should just get 'AAA' in a raw string representation.
		self.assertEqual(rawOutput[0],'\x41\x41\x41',msg="Expected \\x41\\x41\\x41 ('AAA').")
		self.assertEqual(rawOutput[0],'AAA',msg="Expected 'AAA' (\x41\x41\x41)).") # Both will work.
		self.assertEqual(len(rawOutput[0]),3,msg='Expected three bytes.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testRawGoodByte_fullASCIITable(self):
		""" Read the entire ASCII table, i.e. integers from 0 to 127 inclusive,
		all in one go. """
		self.fixture.write(b'S') # Send the command byte to execute this test case.
		time.sleep(1) # Wait for the transmission of all the ASCII bytes.

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Prepare the expected results - the entire ASCII table in byte format.
		allASCIIBytes=b''
		for i in range(0,128): # From 0x00 to 0x7F.
			allASCIIBytes += i.to_bytes(1,byteorder='little',signed=False)

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get allASCIIBytes in a raw string representation. Explicitly
		# cast rawOutput[0] to bytes to be able to compare to allASCIIBytes.
		self.assertEqual(bytes(rawOutput[0],'ASCII'),allASCIIBytes,msg="Expected {}.".format(allASCIIBytes))
		self.assertEqual(len(rawOutput[0]),128,msg='Expected 128 bytes.')
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testRawGoodByte_nonASCIIInts(self):
		""" Send several integers above the ASCII range at the same time. This
		test also covers extended ASCII range and unicode Latin script codes. """

		# Below expected results of the monitor and their decimal
		# representations up to 255 - getting them programmatically is a bit of
		# a pain, so use https://www.rapidtables.com/convert/number/hex-to-ascii.html
		# They are in range 0x80 to 0xFF, i.e. no longer ASCII but still one byte.
		expectedAns='\x80\x81\x82\x8a\x8b\x8f\x9f\xa0\xa1\xc8\xf0\xfe\xff'
		expectedDec=[128,129,130,138,139,143,159,160,161,200,240,254,255] # Unused here, only in the Arduino.

		self.fixture.write(b'N') # Send the command byte to execute this test case.
		time.sleep(1) # Wait for the transmission of all the bytes.

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get expectedAns in a raw string representation.
		# expectedAns is also a string, so can compare w/o casting.
		self.assertEqual(rawOutput[0],expectedAns,msg="Expected {}.".format(expectedAns))
		self.assertEqual(len(rawOutput[0]),len(expectedAns),msg='Expected {} bytes.'.format(len(expectedAns)))
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testRawGoodBytes_longInts(self):
		""" Two-byte integers. Expect string representation of both bytes.  """
		self.fixture.write(b'L') # Send the command byte to execute this test case.
		time.sleep(1) # Wait for the transmission of all the bytes.

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Prepare the expected results - all the individual bytes.
		# NOTE - Arduino uses little endian, so be careful with byteorder.
		expectedAns=''
		for i in range(256,65535,500): # 0x0100 to 0xFFFF.
			expectedAns += ''.join(chr(x) for x in i.to_bytes(2, byteorder='little', signed=False))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get expectedAns in a raw string representation.
		# expectedAns is also a string, so can compare w/o casting.ng.
		self.assertEqual(rawOutput[0],expectedAns,msg="Expected {}.".format(expectedAns))
		self.assertEqual(len(rawOutput[0]),len(expectedAns),msg='Expected {} bytes.'.format(len(expectedAns)))
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testRaw_ByteSequence(self):
		""" Various sequences of bytes with 0x00 in different places.  """
		# Below are hex bytes sequences and the corresponding expected results of
		# the monitor - getting them programmatically is a bit of a pain, so use
		# https://www.rapidtables.com/convert/number/hex-to-ascii.html
		expectedAnsParts=['\x80\x81\x82\x80\x00\x82\x80\x82\x00\x00\x80\x82',
						# '¡'=0xA1=0xa1, both hex (with a and A) and str will work.
						'\x80\xa0\x00\x82¡\x80\x82\xa1\x00\x00\xA1\x80\x82',
						# '¯'=0xaf=0xAF, all thee representations will work.
						'\x00¯\x80\x82\x00\xaf\x00\x00\x00\x00\xaf\x00']
		expectedAns=expectedAnsParts[0]+expectedAnsParts[1]+expectedAnsParts[2]

		self.fixture.write(b'Q') # Send the command byte to execute this test case.
		time.sleep(1) # Wait for the transmission of all the bytes.

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get expectedAns in a raw string representation.
		# expectedAns is also a string, so can compare w/o casting.ng.
		self.assertEqual(rawOutput[0],expectedAns,msg="Expected {}.".format(expectedAns))
		self.assertEqual(len(rawOutput[0]),len(expectedAns),msg='Expected {} bytes.'.format(len(expectedAns)))
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testRaw_OutOfUnicodeRange(self):
		""" Send a few valid messgages on the border of unicode range,
		and one that exceeds the valid range (up to 1 114 111=0x10FFFF). """
		# Below are integers and the corresponding expected results of
		# the monitor - getting them programmatically is a bit of a pain, so use
		# https://www.rapidtables.com/convert/number/hex-to-ascii.html
		# 0x110000 = 0x10FFFF+1, exceeds unicode range in Python 3:
		# https://docs.python.org/3/library/functions.html#chr
		# However, SerialMonitor will convert bytes one at a time so cannot exceed
		# the valid unicode range even if we send a larger integer.
		expectedAnsParts=['\x10\xFF\xFE','\x10\xFF\xFF','\x11\x00\x00']
		expectedAns=expectedAnsParts[0]+expectedAnsParts[1]+expectedAnsParts[2]
		goodDec=[0x10FFFE,0x10FFFF,0x110000] # Unused here, only in the Arduino.

		self.fixture.write(b'R') # Send the command byte to execute this test case.
		time.sleep(1) # Wait for the transmission of all the bytes.

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the reply to the command byte if no exception has been raised.
		rawOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','raw')
		# Should get a string output.
		self.assertTrue(type(rawOutput[0])==str,'rawOutput[0] is not string.')
		# Should get expectedAns in a raw string representation.
		# expectedAns is also a string, so can compare w/o casting.ng.
		self.assertEqual(rawOutput[0],expectedAns,msg="Expected {}.".format(expectedAns))
		self.assertEqual(len(rawOutput[0]),len(expectedAns),msg='Expected {} bytes.'.format(len(expectedAns)))
		# 'raw' option should leave outputBuffer unchanged.
		self.assertEqual(rawOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(rawOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

if __name__ == '__main__':
	unittest.main()
