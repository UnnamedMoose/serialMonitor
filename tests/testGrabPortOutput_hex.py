#!/usr/bin/python3
""" Test the SerialMonitor.grabPortOutput without using actual hardware.
Focus on the hex outputFormat.

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

	def testHexEmptyMessage(self):
		""" Send an empty message with hex outputFormat. """
		notNeeded=self.fixture.read(1) # Empty the port.
		self.assertEqual(self.fixture.read(1),b'',
						msg='Need an empty bufferbefore running this test case.')
		# port.inWaiting will be 0, so grabPortOutput will just proceed to return
		# the input outputBuffer and the default (empty) output.
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
		self.assertEqual(hexOutput[0],'',msg='Expected empty string as output.')
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testHexGoodByte_0x00(self):
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

	def testHexGoodByte_0x01(self):
		""" Send a valid hex message. """
		self.fixture.write(b'\x01')
		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
		# Should just get whatever we've put in, but in a string representation of hex.
		#TODO this was tested against hex(0x01), which returns '0x1'. This would cause
		# problems down the line because of the missing leading zero.
		self.assertEqual(hexOutput[0],'0x01',msg='Expected 0x01.')
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testHexGoodByte_0x41(self):
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

	def testHexGoodByte_fullASCIITable(self):
		""" Send a valid hex message, one valid ASCII byte at a time. """
		for i in range(0,128): # From 0x00 to 0x7F.
			# Avoid implicit casting in the serial module - need to send bytes.
			# Easiest to convert int i to ASCII and then to bytes.
			self.fixture.write(bytes(chr(i),'ASCII'))
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
			#print(hexOutput[0],i) # To eyeball the results.
			# Should just get whatever we've put in, but in a string representation of hex.
			self.assertEqual(hexOutput[0],hex(i),msg='Expected {}.'.format(hex(i)))
			# 'hex' option should leave outputBuffer unchanged.
			self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
			# Should have no warnings.
			self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testHexGoodByte_nonASCIIInts(self):
		""" Valid hex message - one integer above the ASCII range at a time.
		Also covers extended ASCII range and unicode Latin script codes. """
		# Below are hex bytes, expected results of the monitor and their decimal
		# representations up to 255 - getting them programmatically is a bit of
		# a pain, so use https://www.rapidtables.com/convert/number/ascii-hex-bin-dec-converter.html
		# All hex-code letters will be lower case - they're the same numbers as capitals, though.
		goodHex=[b'\x80',b'\x81',b'\x82',b'\x8A',b'\x8B',b'\x8F',b'\x9F',b'\xA0',
			b'\xA1',b'\xC8',b'\xF0',b'\xFE',b'\xFF']
		goodAns=['0x80','0x81','0x82','0x8a','0x8b','0x8f','0x9f','0xa0','0xa1',
			'0xc8','0xf0','0xfe','0xff']
		goodDec=[128,129,130,138,139,143,159,160,161,200,240,254,255]
		for i in range(len(goodDec)): # 0x80 to 0xFF, i.e. no longer ASCII but still one byte.
			self.fixture.write(goodHex[i])
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
			# print(hexOutput[0],goodAns[i],goodDec[i]) # To eyeball the results.
			# Should just get whatever we've put in, but in a string representation of hex.
			self.assertEqual(hexOutput[0],goodAns[i],msg='Expected {}.'.format(goodAns[i]))
			# 'hex' option should leave outputBuffer unchanged.
			self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
			# Should have no warnings.
			self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testHex_ByteSequence(self):
		""" Valid hex message - various sequences of bytes with 0x00 in various
		places. """
		# Below are hex bytes sequences and the corresponding expected results of the
		# monitor - getting them programmatically is a bit of a pain, so use
		# https://www.rapidtables.com/convert/number/decimal-to-hex.html
		# All hex-code letters will be lower case - they're the same numbers as
		# capitals, though.
		# Individual bytes will be separated by a colon (':') in the output.
		# 0x00 will be output as 0x0.
		goodHex=[b'\x80\x81\x82',b'\x80\x00\x82',b'\x80\x82\x00',b'\x00\x80\x82',
				b'\x80\xA0\x00\x82\xA1',b'\x80\x82\xA1\x00',b'\x00\xA1\x80\x82',
				b'\x00\xAF\x80\x82']
		goodAns=['0x80:0x81:0x82','0x80:0x0:0x82','0x80:0x82:0x0','0x0:0x80:0x82',
				'0x80:0xa0:0x0:0x82:0xa1','0x80:0x82:0xa1:0x0','0x0:0xa1:0x80:0x82',
				'0x0:0xaf:0x80:0x82']

		for i in range(len(goodHex)):
			# Avoid implicit casting in the serial module - need to send bytes.
			self.fixture.write(goodHex[i])
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
			# print(hexOutput[0],goodAns[i]) # To eyeball the results.
			# Should just get whatever we've put in, but in a string representation of hex.
			self.assertEqual(hexOutput[0],goodAns[i],msg='Expected {}.'.format(goodAns[i]))
			# 'hex' option should leave outputBuffer unchanged.
			self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
			# Should have no warnings.
			self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

	def testHexByteSequence_fullASCIITable(self):
		""" Send the entire ASCII table in one go. """
		previousMaxDiff=self.maxDiff # Only temporarily change the test settings.
		self.maxDiff=None # Otherwise, the comparison will be truncated.
		goodHex=[] # All the sent bytes.
		goodAns='0x0:' # The expected answer.

		# Send the entire sequence, with 0x00 in the beginning, ~middle, and the end.
		self.fixture.write(b'\x00')
		for i in range(0,128): # From 0x00 to 0x7F.
			# Avoid implicit casting in the serial module - need to send bytes.
			# Easiest to convert int i to ASCII and then to bytes.
			self.fixture.write(bytes(chr(i),'ASCII'))
			goodHex.append(bytes(chr(i),'ASCII'))
			goodAns+=(hex(i)+':')
			if i==63: # Put some 0x00 in the middle, to mix thing up a bit.
				self.fixture.write(b'\x00\x00\x00')
				goodAns+='0x0:0x0:0x0:'
		self.fixture.write(b'\x00')
		goodAns+='0x0'

		time.sleep(0.1) # In case there's a delay (to be expected on Windows).
		hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
		#print(hexOutput[0],i) # To eyeball the results.
		# Should just get whatever we've put in, but in a string representation of hex.
		self.assertEqual(hexOutput[0],goodAns,msg='Expected {}.'.format(goodAns))
		# 'hex' option should leave outputBuffer unchanged.
		self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
		# Should have no warnings.
		self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
		# The port should be empty now.
		self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

		self.maxDiff=previousMaxDiff # Back to what it was.

	def testHexGoodBytes_twoByteInt(self):
		""" Valid hex message - one two-byte integer at a time. """
		# Below are hex bytes, expected results of the monitor and their decimal
		# representations - getting them programmatically is a bit of a pain, so
		#  use https://www.rapidtables.com/convert/number/decimal-to-hex.html
		# All hex-code letters will be lower case - they're the same numbers as capitals, though.
		goodHex=[b'\x01\x03'] #TODO using int.to_bytes here might help to send the right bytes.
		goodAns=['0x01:0x03'] #TODO verify if this is correct: AssertionError: '0x1:0x3' != '0x01:0x03'
		#TODO according to the hex-to-decimal converter, the leading zeros in front of 1 and 3 are needed
		# so the AssertionError is correct. So there might be a problem in the hex option.
		# Also, it's impossible to create a bute array from 0x1 0x3, whereas 0x01 0x03 works:
		# >>> bbb=bytearray(b'\x1\x3')
		# File "<stdin>", line 1
		# SyntaxError: (value error) invalid \x escape at position 0
		# bbb=bytearray(b'\x01\x03') # Works.
		goodDec=[259]

		for i in range(len(goodDec)): # 0x103 to 0xFFFF, two byte integers.
			# Avoid implicit casting in the serial module - need to send bytes.
			self.fixture.write(goodHex[i])
			time.sleep(0.1) # In case there's a delay (to be expected on Windows).
			hexOutput=sm.commsInterface.grabPortOutput(self.fixture,'DummyBuff','hex')
			print(hexOutput[0],goodAns[i],goodDec[i]) # To eyeball the results.
			# Should just get whatever we've put in, but in a string representation of hex.
			self.assertEqual(hexOutput[0],goodAns[i],msg='Expected {}.'.format(goodAns[i]))
			# 'hex' option should leave outputBuffer unchanged.
			self.assertEqual(hexOutput[1],'DummyBuff',msg='Expected unchanged DummyBuff.')
			# Should have no warnings.
			self.assertEqual(hexOutput[2],{},msg='Expected empty warning dict.')
			# The port should be empty now.
			self.assertEqual(self.fixture.read(1),b'',msg='Expected empty buffer after the test.')

			#TODO there is a bug with long integers.
			# For 259=0x103='ă', get '0x10:0x33' from the SerialMonitor.
			#>>> hex(259)
			#'0x103'
			#>>> chr(259)
			#'ă'
			#>>> bytes(chr(259),'utf-8')
			#b'\xc4\x83'
			#>>> sm.commsInterface.grabPortOutput(fixture,'DummyBuff','hex')
			#('', 'DummyBuff', {})
			#>>> fixture.write(b'\x103')
			#2
			#>>> sm.commsInterface.grabPortOutput(fixture,'DummyBuff','hex')
			#('0x10:0x33', 'DummyBuff', {})

	#     port.inWaiting==0, should return the input outputBuffer - (empty dataStr) DONE
	#     test hex encoding with:
		# 1) invalid ASCII characters, - ints larger than 127 -                     DONE
		# 2) valid and invalid unicode characters, - one byte (up to 255) -         DONE
		# 3) valid and invalid numbers, - one byte (up to 255) -                    DONE
		# 4) empty dataStr, - (port.inWaiting==0)                                   DONE
		# 5) sequences of many bytes with \0x00 in various places.                  DONE
		#TODO 6) long integers -                                                    FAIL
	#TODO should try sending various representations of the same bytes to make      _
	    # sure they're all understood.

if __name__ == '__main__':
	unittest.main()
