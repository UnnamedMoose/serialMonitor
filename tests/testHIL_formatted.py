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

	def testEmptyMessage(self):
		""" Send an empty message. """
		notNeeded=self.fixture.read(1) # Empty the port.
		self.assertEqual(self.fixture.read(1),b'',
						msg='Need an empty buffer before running this test case.')
		# port.inWaiting will be 0, so grabPortOutput will just proceed to return
		# the input outputBuffer and the default (empty) output.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		self.assertEqual(formattedOutput[0],'',msg='Expected empty string as output.')
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes.')
		self.assertEqual(formattedOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),9,msg='Expected nine bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_0(self):
		""" Single formatted byte with three different representations of '0'. """
		self.fixture.write(b'Z') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response ('0' ASCII and two 0x00 integers).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff0\x00\x00',msg='Expected DummyBuff0\\x00\\x00.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),12,msg='Expected 12 bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_1(self):
		""" Single formatted byte with three different representations of '1'. """
		self.fixture.write(b'O') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response is '1'11 (ASCII and two 1 integers) = 0x31 0x01 0x01
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff1\x01\x01',msg='Expected DummyBuff1\\x01\\x01.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),12,msg='Expected 12 bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_0x41(self):
		""" Single formatted byte with three different representations of
		ASCII 'A' = 0x41 = 65. """
		self.fixture.write(b'A') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response is 'A'0x41 65 (ASCII and two integers).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		# Both 'A' and '\x41' representations work.
		self.assertEqual(formattedOutput[1],'DummyBuffA\x41\x41',msg='Expected DummyBuffA\\x41\\x41.')
		self.assertEqual(formattedOutput[1],'DummyBuffAAA',msg='Expected DummyBuffAAA.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),12,msg='Expected 12 bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_0andEOL(self):
		""" Single formatted byte with three different representations of '0'.
		There will be an EOL ('\n') at the end. """
		self.fixture.write(b'z') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response ('0' ASCII and two 0x00 integers).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent bytes + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff0\x00\x00\n',msg='Expected DummyBuff0\\x00\\x00\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected epty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),13,msg='Expected 13 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_1ndEOL(self):
		""" Single formatted byte with three different representations of '1'.
		There will be an EOL ('\n') at the end. """
		self.fixture.write(b'o') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response is '1'11 (ASCII and two 1 integers) = 0x31 0x01 0x01
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent bytes + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff1\x01\x01\n',msg='DummyBuff1\\x01\\x01\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected epty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),13,msg='Expected 13 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_0x41ndEOL(self):
		""" Single formatted byte with three different representations of
		ASCII 'A' = 0x41 = 65. There will be an EOL ('\n') at the end. """
		self.fixture.write(b'a') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response is 'A'0x41 65 (ASCII and two integers).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent bytes + EOL.
		# Both 'A' and '\x41' representations work.
		self.assertEqual(formattedOutput[0],'DummyBuffA\x41\x41\n',msg='Expected DummyBuffA\\x41\\x41\n.')
		self.assertEqual(formattedOutput[0],'DummyBuffAAA\n',msg='Expected DummyBuffAAA\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected epty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),13,msg='Expected 13 bytes')
		self.assertEqual(len(formattedOutput[1]),0	,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_invalidASCII(self):
		""" Send several non-ASCII bytes (128+, 0x80 to 0xFF, i.e. no longer ASCII but
		still one byte.) """
		self.fixture.write(b'N') # Send the command byte to execute this test case.
		timeoutCounter=0

		while self.fixture.inWaiting() <= 0: # Wait for data to appear.
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response - received no valid ASCII bytes.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# Will not change the outputBuffer if there are invalid bytes sent.
		self.assertEqual(formattedOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected 0 characters.')
		self.assertEqual(len(formattedOutput[1]),9,msg='Expected 9 characters.')
		# Should have 13 warnings.
		self.assertEqual(len(formattedOutput[2]),13,msg='Expected 13 warnings in the dict.')
		# Check that the error dict has the expected keys. N.B. dicts are unordered
		# so don't know which key will be at what index.
		for i in range(13):
			self.assertIn('UnicodeDecodeError{}'.format(i),list(formattedOutput[2].keys()),
				msg='Expected UnicodeDecodeError{} in the dict keys.'.format(i))
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

	def testFormattedGoodByte_fullASCIITable(self):
		""" Send a valid formatted message, one valid ASCII byte at a time. Some will
		be sent and read as hex codes of bytes, others as ASCII characters. """
		self.fixture.write(b'S') # Send the command byte to execute this test case.
		time.sleep(1) # Wait for the transmission of all the ASCII bytes.

		# Prepare the expected output. Some bytes (before EOL) as well as the input
		# buffer will be moved to output. The following will be in the outputBuffer.
		# N.B. 0x0a=10='\n'
		expectedOutput='DummyBuff'
		expectedBuffer=''
		for i in range(0,10): # Before EOL - will be moved to output.
			expectedOutput+=chr(i)
		expectedOutput+='\n' # EOL at the end of output.

		for i in range(11,128): # After EOL - will be stored in the buffer.
			expectedBuffer+=chr(i)

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response - some bytes in output, others in the buffer.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		self.assertEqual(formattedOutput[0],expectedOutput,msg='Expected output={}'.format(expectedOutput))
		self.assertEqual(formattedOutput[1],expectedBuffer,msg='Expected buffer={}'.format(expectedBuffer))
		self.assertEqual(len(formattedOutput[0]),20,msg='Expected 20 characters.')
		self.assertEqual(len(formattedOutput[1]),117,msg='Expected 117 characters.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_fullASCIITableInOneGo(self):
		""" Send the full ASCII table in many lines separated by EOLs. Some bytes
		will be sent and read as hex codes of bytes, others as ASCII characters. """
		previousDiffLen = self.maxDiff
		self.maxDiff = None # To be able to see the entire message in case of test failure.

		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer before the test.')

		self.fixture.write(b's') # Send the command byte to execute this test case.
		time.sleep(2) # Wait for the transmission of all the ASCII bytes.

		# Prepare the expected output.
		sentBytes=b'' # What we've actually sent.
		ctr=10 # Sent EOL when this reaches 0.
		for i in range(0,128): # From 0x00 (0) to 0x7F (127).
			sentBytes += i.to_bytes(1,byteorder='big',signed=False)
			ctr-=1
			if ctr==0: # Send EOL every so often to split all characters into lines.
				ctr=10
				sentBytes += b'\n'
		sentBytes += b'\n' # A known outputBuffer after the message.

		timeoutCounter=0 # Wait for data to appear.
		while self.fixture.inWaiting() <= 0:
			time.sleep(0.1)
			timeoutCounter += 1
			if timeoutCounter == TIMEOUT:
				self.fixture.close()
				raise BaseException('Getting test data from the Arduino on port {} timed out.'.format(self.fixture.port))

		# Verify the response - some bytes in output, others in the buffer.
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# Will move input outputBuffer ('DummyBuff') to output and append the
		# sent message to it. 'OutputBuffer' will now be in the outputBuffer.
		self.assertEqual(formattedOutput[0],'DummyBuff'+''.join(chr(x) for x in sentBytes),
			msg='Expected {} in output.'.format('DummyBuff'+''.join(chr(x) for x in sentBytes)))
		self.assertEqual(formattedOutput[1],'OutputBuffer',msg="Expected 'OutputBuffer' in outputBuffer")
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),len('DummyBuff')+len(sentBytes),
			msg='Expected {} bytes'.format(len('DummyBuff')+len(sentBytes)))
		self.assertEqual(len(formattedOutput[1]),12,msg='Expected 12 bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

		self.maxDiff = previousDiffLen # Revert temporay change.

		#TODO translate formatted tests into hardware in the loop.
		#TODO testFormattedGoodByte_validInvalidASCII
		#TODO testFormattedGoodByte_invalidValidASCII
		#TODO testFormattedGoodByte_validELOInvalidASCII

if __name__ == '__main__':
	unittest.main()
