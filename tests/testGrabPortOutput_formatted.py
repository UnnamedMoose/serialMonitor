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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),9,msg='Expected nine bytes')
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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
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
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
		self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_0andEOL(self):
		""" Send a single formatted byte with two different representations
		of '0' and an EOL termination. """
		self.fixture.write(b'\x00\n')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent byte + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff\x00\n',msg='Expected DummyBuff\\x00\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'0\n')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent byte + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff0\n',msg='Expected DummyBuff0\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_1andEOL(self):
		""" Send a single formatted byte with two different representations of
		'1' and an EOL termination. """
		self.fixture.write(b'\x01\n')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent byte + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff\x01\n',msg='Expected DummyBuff\\x01\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'1\n')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent byte + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff1\n',msg='Expected DummyBuff1\n.')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_0x41andEOL(self):
		""" Send a single formatted byte with two different representations of
		ASCII 'A' = 0x41 and an EOL termination. """
		self.fixture.write(b'\x41\n')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent byte + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuff\x41\n',msg='Expected DummyBuff\\x41\n.')
		self.assertEqual(formattedOutput[0],'DummyBuffA\n',msg='Expected DummyBuffA\n.') # Both representations work.
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after reading.')

		self.fixture.write(b'A\n')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have the input outputBuffer + sent byte + EOL.
		self.assertEqual(formattedOutput[0],'DummyBuffA\n',msg='Expected DummyBuffA\n.')
		self.assertEqual(formattedOutput[0],'DummyBuff\x41\n',msg='Expected DummyBuff\\x41\n.') # Both representations work.
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 bytes')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
		# No output buffer, we've sent one complete line.
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
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
				# Check message length.
				self.assertEqual(len(formattedOutput[0]),0,msg='Expected zero bytes')
				self.assertEqual(len(formattedOutput[1]),10,msg='Expected ten bytes')
			else: # We terminated the message because 0x0a='\n'
				# Will move input outputBuffer to output and append nothing to it -
				# only one complete line has been sent.
				self.assertEqual(formattedOutput[0],'DummyBuff\n',msg='Expected DummyBuff\\n in output.')
				self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer')
				# Check message length.
				self.assertEqual(len(formattedOutput[0]),10,msg='Expected ten bytes')
				self.assertEqual(len(formattedOutput[1]),0,msg='Expected zero bytes')
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

		sentBytes=b'' # What we've actually sent.
		ctr=10 # Sent EOL when this reaches 0.
		for i in range(0,128): # From 0x00 (0) to 0x7F (127).
			# Avoid implicit casting in the serial module - need to send bytes.
			self.fixture.write(i.to_bytes(1,byteorder='big',signed=False))
			sentBytes += i.to_bytes(1,byteorder='big',signed=False)
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			ctr-=1
			if ctr==0: # Send EOL every so often to split all characters into lines.
				ctr=10
				self.fixture.write(b'\n')
				sentBytes += b'\n'
		# Make sure there is a known outputBuffer after the message.
		self.fixture.write(b'\nOutputBuffer') # No EOL after 'OutputBuffer'
		sentBytes += b'\n' # 'OutputBuffer' will go to the outputBuffer, '\n' to output.

		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# Will move input outputBuffer ('DummyBuff') to output and append the
		# sent message to it. 'OutputBuffer' will now be in the outputBuffer.
		self.assertEqual(formattedOutput[0],'DummyBuff'+''.join(chr(x) for x in sentBytes),
			msg='Expected {} in output.'.format('DummyBuff'+''.join(chr(x) for x in sentBytes)))
		self.assertEqual(formattedOutput[1],'OutputBuffer',msg="Expected\
		 							'OutputBuffer' in outputBuffer")
		# Check message length.
		self.assertEqual(len(formattedOutput[0]),len('DummyBuff')+len(sentBytes),
			msg='Expected {} bytes'.format(len('DummyBuff')+len(sentBytes)))
		# print(''.join(chr(x) for x in sentBytes), # To eyeball the results.
		# 	formattedOutput[0],formattedOutput[1])
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

		self.maxDiff = previousDiffLen # Revert temporay change.

	def testFormattedGoodByte_invalidASCII(self):
		""" Send a formatted message with an invalid ASCII byte. """
		# First send the largest valid ASCII byte.
		self.fixture.write(b'\x7F') # 127 = 0x7F, largest valid ASCII.
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# 'formatted' outputFormat will append to the outputBuffer if there's no EOL termination.
		self.assertEqual(formattedOutput[1],'DummyBuff\x7F',msg='Expected DummyBuff\\x7F.')
		# Should have no warnings.
		self.assertEqual(formattedOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

		# Send one invalid byte.
		self.fixture.write(b'\x80') # 128 = 0x80, invalid ASCII.
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# Will not change the outputBuffer if there's an invalid byte sent.
		self.assertEqual(formattedOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have a warning.
		self.assertEqual(len(formattedOutput[2]),1,msg='Expected one warning in the dict.')
		# print(formattedOutput[2]) # To eyeball the results.
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

		self.fixture.write(b'\x80\x81') # 128=0x80, 129=0x81, both invalid ASCII.
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# Will not change the outputBuffer if there's an invalid byte sent.
		self.assertEqual(formattedOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		self.assertEqual(len(formattedOutput[0]),0,msg='Expected 0 characters.')
		self.assertEqual(len(formattedOutput[1]),len('DummyBuff'),msg='Expected {} characters.'.format(len('DummyBuff')))
		self.assertEqual(len(formattedOutput[2]),2,msg='Expected two warnings in the dict.')
		# Check that the error dict has the expected keys. N.B. dicts are unordered
		# so don't know which key will be at what index.
		self.assertIn('UnicodeDecodeError0',list(formattedOutput[2].keys()),msg='Expected UnicodeDecodeError0 in the dict keys.')
		self.assertIn('UnicodeDecodeError1',list(formattedOutput[2].keys()),msg='Expected UnicodeDecodeError1 in the dict keys.')
		# print(formattedOutput[2]) # To eyeball the results.
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_validInvalidASCII(self):
		""" Send a formatted message with valid and invalid ASCII bytes. """
		# Send one valid and one invalid byte.
		self.fixture.write(b'\x7F\x80') # 128=0x80, invalid ASCII. 127=0x7F is valid.
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# Should append the valid byte to outputBuffer (no EOL termination), and discard the invalid byte.
		self.assertEqual(formattedOutput[1],'DummyBuff\x7F',msg='Expected DummyBuff\\x7F.')
		self.assertEqual(len(formattedOutput[1]),len('DummyBuff')+1,msg='Expected {} characters.'.format(len('DummyBuff')+1))
		# Should have one warning.
		self.assertEqual(len(formattedOutput[2]),1,msg='Expected one warning in the dict.')
		self.assertIn('UnicodeDecodeError0',list(formattedOutput[2].keys()),msg='Expected UnicodeDecodeError0 in the dict keys.')
		# print(formattedOutput[2]) # To eyeball the results.
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_invalidValidASCII(self):
		""" Send a formatted message with invalid and valid ASCII bytes. """
		# Send one invalid and one valid byte.
		self.fixture.write(b'\x80\x7F') # 128=0x80, invalid ASCII. 127=0x7F is valid.
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will be empty if there is no EOL termination of the message.
		self.assertEqual(formattedOutput[0],'',msg='Expected empty output.')
		# Should append the valid byte to outputBuffer (no EOL termination), and discard the invalid byte.
		self.assertEqual(formattedOutput[1],'DummyBuff\x7F',msg='Expected DummyBuff\\x7F.')
		self.assertEqual(len(formattedOutput[1]),len('DummyBuff')+1,msg='Expected {} characters.'.format(len('DummyBuff')+1))
		# Should have one warning.
		self.assertEqual(len(formattedOutput[2]),1,msg='Expected one warning in the dict.')
		self.assertIn('UnicodeDecodeError0',list(formattedOutput[2].keys()),msg='Expected UnicodeDecodeError0 in the dict keys.')
		# print(formattedOutput[2]) # To eyeball the results.
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testFormattedGoodByte_validELOInvalidASCII(self):
		""" Send a formatted message with valid and invalid ASCII bytes separated by EOL. """
		# Send one valid and one invalid byte with 0x0a=10='\n' in the middle.
		self.fixture.write(b'\x7F\x0A\x80') # 128=0x80, invalid ASCII. 127=0x7F is valid.
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		formattedOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','formatted')
		# output will have one byte sent before the EOL, which will be appended to DummyBuff.
		self.assertEqual(formattedOutput[0],'DummyBuff\x7F\n',msg='Expected DummyBuff\\x7F\\n in output.')
		self.assertEqual(len(formattedOutput[0]),11,msg='Expected 11 characters.')
		# Should have nothing to the outputBuffer (no valid byte after EOL termination, DummyBuff moved to output).
		self.assertEqual(formattedOutput[1],'',msg='Expected empty outputBuffer.')
		self.assertEqual(len(formattedOutput[1]),0,msg='Expected 0 characters.')
		# Should have one warning.
		self.assertEqual(len(formattedOutput[2]),1,msg='Expected one warning in the dict.')
		self.assertIn('UnicodeDecodeError0',list(formattedOutput[2].keys()),msg='Expected UnicodeDecodeError0 in the dict keys.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	# port.inWaiting==0, should return the input outputBuffer - (empty dataStr)     DONE
	# test formatted output with:
		# 1) valid ASCII characters,                                                DONE
		# 2) invalid ASCII characters,                                              DONE
		# 3) valid numbers,                                                         DONE
		# 4) empty dataStr,                                                         DONE
		# 5) valid and invalid formatitng of the dataStr (bytes with and            DONE
		# without EOL termination),
		# 5) sequences of many bytes interrupted with \n.                           DONE
	# Should try sending various representations of the same bytes to make          DONE
	# sure they're all understood.
	# Should check the length of the returned bytes.                                DONE

if __name__ == '__main__':
	unittest.main()
