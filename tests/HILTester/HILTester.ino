/* This Arduino code is supposed to run together with a corresponding
 * SerialMonitor test script. The test script will send a command to the Arduino
 * to execute a given test case (send certain data through the serial port).
 * The test script will then compare the data that if received to the expected
 * results in order to determine whether the test has been successful or not.
 * */

void sendInvalidEOLValid(void)
 /* Send one invalid (128=0x80) and one valid (126=0x7E=~) ASCII bytes
 separated by EOL ('\n'). */
 {
 	Serial.write(0x80); // Invalid = 128.
 	Serial.print("\n"); // EOL = '\n' = 0x0A = 10.
	Serial.write(0x7E); // Valid ~ = 0x7E = 126.
 	Serial.flush(); // Wait for the outgoing buffer to be cleared.
 }

void sendValidEOLInvalid(void)
 /* Send one valid (127=0x7F) and one invalid (128=0x80) ASCII bytes
 separated by EOL ('\n'). */
 {
	Serial.write(0x7F); // Valid = 127.
	Serial.print("\n"); // EOL = '\n' = 0x0A = 10.
	Serial.write(0x80); // Invalid = 128.
 	Serial.flush(); // Wait for the outgoing buffer to be cleared.
 }

void sendValidInvalid(void)
 /* Send one valid (127=0x7F) and one invalid (128=0x80) ASCII bytes. */
 {
 	Serial.write(0x7F); // Valid = 127.
 	Serial.write(0x80); // Invalid = 128.
 	Serial.flush(); // Wait for the outgoing buffer to be cleared.
 }

void sendInvalidValid(void)
 /* Send one invalid (128=0x80) and one valid (126=0x7E=~) ASCII bytes.
 Use different valid byte than ValidInvalid test case to make sure we run both. */
 {
	Serial.write(0x80); // Invalid = 128.
	Serial.write(0x7E); // Valid = ~ = 0x7E = 126.
 	Serial.flush(); // Wait for the outgoing buffer to be cleared.
 }

void serialSendLong(long f)
/* Send a 16-bit long integer number via serial connection, one
byte at a time. The serial connection must be initialised with the desired baud
rate before calling this function. */
{
	byte* b = (byte *) &f; // Cast the long to a byte array (size 2 bytes = 16 bits).
	for(int i=0;i<2;i++)
	{
		Serial.write(b[i]); // Send each byte at a time.
	}
}

void sendOutOfRange(void)
/* Send three messgages, one of which (0x110000 = 0x10FFFF+1) exceeds Unicode
range in Python 3. */
{
	// We'll send the following 3-byte numbers: 0x10FFFE,0x10FFFF,0x110000.
	// Need to send bytes one by one, Serial.write doesn't support larger inputs.
	Serial.write(0x10);Serial.write(0xFF);Serial.write(0xFE); // Unicode range - 1
	Serial.write(0x10);Serial.write(0xFF);Serial.write(0xFF); // Unicode range
	Serial.write(0x11);Serial.write(0x00);Serial.write(0x00); // Unicode range + 1

	// Wait for the outgoing buffer to be cleared.
 	Serial.flush();
}

void sendSequences(void)
/* Send various sequences of bytes with 0x00 in different places. Send
each byte one at a time formatted in the raw binary representation. */
{
	// Test data from Python test-script. Various end cases.
	// goodHex=[b'\x80\x81\x82',b'\x80\x00\x82',b'\x80\x82\x00',b'\x00\x80\x82',
	// b'\x80\xA0\x00\x82\xA1',b'\x80\x82\xA1\x00',b'\x00\xA1\x80\x82',
	// b'\x00\xAF\x80\x82',b'\x00\xAF\x00\x00',b'\x00\x00\xAF\x00']

	// Send the data one byte at a time.
 	Serial.write(0x80);Serial.write(0x81);Serial.write(0x82);
 	Serial.write(0x80);Serial.write(0x00);Serial.write(0x82);
 	Serial.write(0x80);Serial.write(0x82);Serial.write(0x00);
	Serial.write(0x00);Serial.write(0x80);Serial.write(0x82);
	Serial.write(0x80);Serial.write(0xA0);Serial.write(0x00);Serial.write(0x82);Serial.write(0xA1);
	Serial.write(0x80);Serial.write(0x82);Serial.write(0xA1);Serial.write(0x00);
	Serial.write(0x00);Serial.write(0xA1);Serial.write(0x80);Serial.write(0x82);
	Serial.write(0x00);Serial.write(0xAF);Serial.write(0x80);Serial.write(0x82);
	Serial.write(0x00);Serial.write(0xAF);Serial.write(0x00);Serial.write(0x00);
	Serial.write(0x00);Serial.write(0x00);Serial.write(0xAF);Serial.write(0x00);

	// Wait for the outgoing buffer to be cleared.
 	Serial.flush();
}

void sendUnique(void)
/* Send the same bytes as in sendSequences but just one unique byte at a time.
Only used in white/black box testsing, not automated test suite. */
{
	Serial.write(0x80);
	Serial.write(0x81);
	Serial.write(0x82);
	Serial.write(0xA0);
	Serial.write(0xA1);
	Serial.write(0xAF);
	Serial.write(0x00);
	// Wait for the outgoing buffer to be cleared.
 	Serial.flush();
}

void sendLongs(void)
/* Send two-byte integers from 256 to 65535 inclusive (0x0100 to 0xFFFF). Do it
in steps of 500 to speed up the test w/o loss of generality and end cases. Send
each long one at a time formatted in the raw binary representation. */
{
	long thisByte = 256; // 0x0100, smallest two-byte int.

	while(thisByte<65535) // Go through all ints until 0xFFFF.
	{
		// Print thisByte unaltered, i.e. the raw binary version of the byte.
		// Do it one byte at a time.
		serialSendLong(thisByte);
		Serial.flush(); // Wait for the outgoing buffer to be cleared.

		// Go on to the next long but in large steps to speed things up.
		thisByte+=500;
	}
	// Send the end case, 0xFFFF = 65535. Now will finish with 65256.
	serialSendLong(65535); // 0xFFFF
	Serial.flush();
}

void sendControlLongs(void)
/* Send all C0 and C1 control characters from WikiPedia:
 https://en.wikipedia.org/wiki/C0_and_C1_control_codes#DCS) interweaved with
  'normal' ones to make sure the replacement works.
  Send two bytes at a time as a long integer. */
{
	serialSendLong(0x0001);Serial.flush();
	serialSendLong(0x0203);Serial.flush();
	serialSendLong(0x0405);Serial.flush();
	serialSendLong(0x0607);Serial.flush();
	serialSendLong(0x0809);Serial.flush();
	serialSendLong(0x0A0B);Serial.flush();
	serialSendLong(0x0C0D);Serial.flush();
	serialSendLong(0x0E0F);Serial.flush();
	serialSendLong(0x1011);Serial.flush();
	serialSendLong(0x1213);Serial.flush();
	serialSendLong(0x1415);Serial.flush();
	serialSendLong(0x1617);Serial.flush();
	serialSendLong(0x1819);Serial.flush();
	serialSendLong(0x1A1B);Serial.flush();
	serialSendLong(0x1C1D);Serial.flush();
	serialSendLong(0x1E1F);Serial.flush();
	serialSendLong(0x207F);Serial.flush();
	serialSendLong(0x0B0C);Serial.flush();
	serialSendLong(0x0D0E);Serial.flush();
	serialSendLong(0x0F11);Serial.flush();
	serialSendLong(0x1213);Serial.flush();
	serialSendLong(0x1819);Serial.flush();
	serialSendLong(0x1C1D);Serial.flush();
	serialSendLong(0x1E1F);Serial.flush();
	serialSendLong(0x8081);Serial.flush();
	serialSendLong(0x8283);Serial.flush();
	serialSendLong(0x8485);Serial.flush();
	serialSendLong(0x8687);Serial.flush();
	serialSendLong(0x8889);Serial.flush();
	serialSendLong(0x8A8B);Serial.flush();
	serialSendLong(0x8C8D);Serial.flush();
	serialSendLong(0x8E8F);Serial.flush();
	serialSendLong(0x9091);Serial.flush();
	serialSendLong(0x9293);Serial.flush();
	serialSendLong(0x9495);Serial.flush();
	serialSendLong(0x9697);Serial.flush();
	serialSendLong(0x9899);Serial.flush();
	serialSendLong(0x9A9B);Serial.flush();
	serialSendLong(0x9D);Serial.flush(); // 0x9C is the terminating byte that unblocks the terminal. Skip it.
	serialSendLong(0x9E9F);Serial.flush();
	serialSendLong(0x8788);Serial.flush();
	serialSendLong(0x898A);Serial.flush();
	serialSendLong(0x8B8C);Serial.flush();
	serialSendLong(0x8D8E);Serial.flush();
	serialSendLong(0x8F90);Serial.flush();
	serialSendLong(0x9192);Serial.flush();
	serialSendLong(0x9394);Serial.flush();
	serialSendLong(0x9596);Serial.flush();
	serialSendLong(0x9798);Serial.flush();
	serialSendLong(0x999A);Serial.flush();
	serialSendLong(0x9B);Serial.flush(); // 0x9C is the terminating byte that unblocks the terminal. Skip it.
	serialSendLong(0x9D9E);Serial.flush();
	Serial.write(0x9F);
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendControl(void)
/* Send all C0 and C1 control characters from WikiPedia:
 https://en.wikipedia.org/wiki/C0_and_C1_control_codes#DCS) interweaved with
  'normal' ones and 'A's to make sure the replacement works.
  Send each byte at a time. */
{
	Serial.write(0x0);Serial.write(0x41);Serial.write(0x1);Serial.write(0x41);
	Serial.write(0x2);Serial.write(0x41);Serial.write(0x3);Serial.write(0x41);
	Serial.write(0x4);Serial.write(0x41);Serial.write(0x5);Serial.write(0x41);
	Serial.write(0x6);Serial.write(0x41);Serial.write(0x7);Serial.write(0x41);
	Serial.write(0x8);Serial.write(0x41);Serial.write(0x9);Serial.write(0x41);
	Serial.write(0x0A);Serial.write(0x41);Serial.write(0x0B);Serial.write(0x41);
	Serial.write(0x0C);Serial.write(0x41);Serial.write(0x0D);Serial.write(0x41);
	Serial.write(0x0E);Serial.write(0x41);Serial.write(0x0F);Serial.write(0x41);
	Serial.write(0x10);Serial.write(0x41);Serial.write(0x11);Serial.write(0x41);
	Serial.write(0x12);Serial.write(0x41);Serial.write(0x13);Serial.write(0x41);
	Serial.write(0x14);Serial.write(0x41);Serial.write(0x15);Serial.write(0x41);
	Serial.write(0x16);Serial.write(0x41);Serial.write(0x17);Serial.write(0x41);
	Serial.write(0x18);Serial.write(0x41);Serial.write(0x19);Serial.write(0x41);
	Serial.write(0x1A);Serial.write(0x41);Serial.write(0x1B);Serial.write(0x41);
	Serial.write(0x1C);Serial.write(0x41);Serial.write(0x1D);Serial.write(0x41);
	Serial.write(0x1E);Serial.write(0x41);Serial.write(0x1F);Serial.write(0x41);
	Serial.write(0x20);Serial.write(0x41);Serial.write(0x7F);Serial.write(0x41);
	Serial.write(0x0B);Serial.write(0x41);Serial.write(0x0C);Serial.write(0x41);
	Serial.write(0x0D);Serial.write(0x41);Serial.write(0x0E);Serial.write(0x41);
	Serial.write(0x0F);Serial.write(0x41);Serial.write(0x11);Serial.write(0x41);
	Serial.write(0x12);Serial.write(0x41);Serial.write(0x13);Serial.write(0x41);
	Serial.write(0x18);Serial.write(0x41);Serial.write(0x19);Serial.write(0x41);
	Serial.write(0x1C);Serial.write(0x41);Serial.write(0x1D);Serial.write(0x41);
	Serial.write(0x1E);Serial.write(0x41);Serial.write(0x1F);Serial.write(0x41);
	Serial.write(0x80);Serial.write(0x41);Serial.write(0x81);Serial.write(0x41);
	Serial.write(0x82);Serial.write(0x41);Serial.write(0x83);Serial.write(0x41);
	Serial.write(0x84);Serial.write(0x41);Serial.write(0x85);Serial.write(0x41);
	Serial.write(0x86);Serial.write(0x41);Serial.write(0x87);Serial.write(0x41);
	Serial.write(0x88);Serial.write(0x41);Serial.write(0x89);Serial.write(0x41);
	Serial.write(0x8A);Serial.write(0x41);Serial.write(0x8B);Serial.write(0x41);
	Serial.write(0x8C);Serial.write(0x41);Serial.write(0x8D);Serial.write(0x41);
	Serial.write(0x8E);Serial.write(0x41);Serial.write(0x8F);Serial.write(0x41);
	Serial.write(0x90);Serial.write(0x41);Serial.write(0x91);Serial.write(0x41);
	Serial.write(0x92);Serial.write(0x41);Serial.write(0x93);Serial.write(0x41);
	Serial.write(0x94);Serial.write(0x41);Serial.write(0x95);Serial.write(0x41);
	Serial.write(0x96);Serial.write(0x41);Serial.write(0x97);Serial.write(0x41);
	Serial.write(0x98);Serial.write(0x41);Serial.write(0x99);Serial.write(0x41);
	Serial.write(0x9A);Serial.write(0x41);Serial.write(0x9B);Serial.write(0x41);
	Serial.write(0x41);Serial.write(0x9D);Serial.write(0x41); // 0x9C is the terminating byte that unblocks the terminal. Skip it.
	Serial.write(0x9E);Serial.write(0x41);Serial.write(0x9F);Serial.write(0x41);
	Serial.write(0x87);Serial.write(0x41);Serial.write(0x88);Serial.write(0x41);
	Serial.write(0x89);Serial.write(0x41);Serial.write(0x8A);Serial.write(0x41);
	Serial.write(0x8B);Serial.write(0x41);Serial.write(0x8C);Serial.write(0x41);
	Serial.write(0x8D);Serial.write(0x41);Serial.write(0x8E);Serial.write(0x41);
	Serial.write(0x8F);Serial.write(0x41);Serial.write(0x90);Serial.write(0x41);
	Serial.write(0x91);Serial.write(0x41);Serial.write(0x92);Serial.write(0x41);
	Serial.write(0x93);Serial.write(0x41);Serial.write(0x94);Serial.write(0x41);
	Serial.write(0x95);Serial.write(0x41);Serial.write(0x96);Serial.write(0x41);
	Serial.write(0x97);Serial.write(0x41);Serial.write(0x98);Serial.write(0x41);
	Serial.write(0x99);Serial.write(0x41);Serial.write(0x9A);Serial.write(0x41);
	Serial.write(0x9B);Serial.write(0x41);Serial.write(0x41); // 0x9C is the terminating byte that unblocks the terminal. Skip it.
	Serial.write(0x9D);Serial.write(0x41);Serial.write(0x9E);Serial.write(0x41);
	Serial.write(0x9F);Serial.write(0x41);
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendAsAndControl(void)
/* Send 10 'A' characters, problematic 0x90 control byte, and 10 more 'A's. */
{
	for(int i=0; i<10; i++)
	{
		Serial.write(0x41); // ASCII for 'A'.
	}
	Serial.write(0x90); // 58256 = 'ã'.
	for(int i=0; i<10; i++)
	{
		Serial.write(0x41); // ASCII for 'A'.
	}
	Serial.flush();
}

void sendTerminatingByte(void)
/* Send 0x9C, which terminates the control byte sequences and unblock the terminal. */
{
	Serial.write(0x9C);
	Serial.flush();
}

void sendNonASCII(void)
/* Send several non-ASCII bytes (128+, 0x80 to 0xFF, i.e. no longer ASCII but
still one byte.). This also covers extended ASCII range and unicode Latin script
codes. Send each byte one at a time formatted in the raw binary representation. */
{
	// Sequence of bytes to be sent during this test case.
	int bytesToSend[] = {128,129,130,138,139,143,159,160,161,200,240,254,255};

	for(int i=0;i<13;i++)
	{
	  // Send this byte unaltered, i.e. the raw binary version of the byte.
	  Serial.write(bytesToSend[i]);
	  Serial.flush(); // Wait for the outgoing buffer to be cleared.
	}
}

void sendASCIITable(void)
/* Send all ASCII characters from 33 to 126 ('!' to '~'), inclusive. Send each
byte one at a time formatted in the raw binary representation. */
{
	// First visible ASCIIcharacter '!' is number 33 but start from 0.
	int thisByte = 0;

	while(thisByte<128) // Go through all characters until 0x7f=128.
						 // Last readable character is '~'=126.
	{
	  // Print thisByte unaltered, i.e. the raw binary version of the byte.
	  Serial.write(thisByte);
	  Serial.flush(); // Wait for the outgoing buffer to be cleared.

	  // Go on to the next character.
	  thisByte++;
	}
}

void sendASCIITableInOneGo(void)
/* Send all ASCII characters from 33 to 126 ('!' to '~'), inclusive in packs of
ten separated by EOL ('\n'). Send 'outputBuffer' at the end. */
{
	// First visible ASCIIcharacter '!' is number 33 but start from 0.
	int ctr = 10;

	// Go through all characters until 0x7f=128.
	// Last readable character is '~'=126.
	for(int thisByte=0; thisByte<128; thisByte++)
	{
	  // Print thisByte unaltered, i.e. the raw binary version of the byte.
	  Serial.write(thisByte);
	  Serial.flush(); // Wait for the outgoing buffer to be cleared.

	  ctr-=1;
	  if(ctr==0)
	  {
	    ctr=10;
	    Serial.write('\n'); // Separate groups of 10 bytes.
	  }
	}

	// Last bytes to be sent. 'OutputBuffer' will go to the outputBuffer, '\n' to output.
	Serial.write("\nOutputBuffer"); // No EOL after 'OutputBuffer'
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendOne(void)
/* Send '1' ASCII character, followed by a 0x00 and 0 integers. */
{
	Serial.print("1"); // Send ASCII character.
	Serial.write(0x01); // Hex number.
	Serial.write(1); // Decimal number.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendZero(void)
/* Send '0' ASCII character, followed by a 0x00 and 0 integers. */
{
	Serial.print("0"); // Send ASCII character.
	Serial.write(0x00); // Hex number.
	Serial.write(0); // Decimal number.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendA(void)
/* Send 'A' character, followed by a 0x41 and 65 (corresponding ASCII code in hex and decimal). */
{
	Serial.print("A"); // Send ASCII.
	Serial.write(0x41); // Send binary data.
	Serial.write(65); // ASCII code.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendOneEOL(void)
/* Send '1' ASCII character, followed by a 0x00 and 0 integers. Add \n at the end. */
{
	Serial.print("1"); // Send ASCII character.
	Serial.write(0x01); // Hex number.
	Serial.write(1); // Decimal number.
	Serial.print("\n"); // Send EOL character.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendZeroEOL(void)
/* Send '0' ASCII character, followed by a 0x00 and 0 integers. Add \n at the end.  */
{
	Serial.print("0"); // Send ASCII character.
	Serial.write(0x00); // Hex number.
	Serial.write(0); // Decimal number.
	Serial.print("\n"); // Send EOL character.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void sendAEOL(void)
/* Send 'A' character, followed by a 0x41 and 65 (corresponding ASCII code in hex
 * and decimal). Add \n at the end.  */
{
	Serial.print("A"); // Send ASCII.
	Serial.write(0x41); // Send binary data.
	Serial.write(65); // ASCII code.
	Serial.print("\n"); // Send EOL character.
	Serial.flush(); // Wait for the outgoing buffer to be cleared.
}

void setup()
/* Setup the Arduino - just open the serial port. */
{
	// Open the serial port @ 9600 baud rate.
	Serial.begin(9600);
}

void loop()
/* Main loop - wait, receive commands to execute a particular test, and delegate
* the said test to a particular function. */
{
	char cmdChar = '0'; // Which test case to execute. 0 - do nothing.
	// Wait until there's something in the serial port to read.
	if (Serial.available() > 0)
	{
		// Read the incoming serial data.
		cmdChar = Serial.read();
		// Execute the chosen test case.
		switch(cmdChar)
		{
			case '0': // Default - do nothing special, use this to make sure that the Arduino is working.
				Serial.print("Arduino reachable."); // Send ASCII characters.
				Serial.flush(); // Wait for the outgoing buffer to be cleared.
				break;
			case 'A': // Simplest test.
				sendA();
				break;
			case 'Z': // Another simple test.
				sendZero();
				break;
			case 'O': // Another simple test.
				sendOne();
				break;
			case 'S': // Send an entire ASCII table.
				sendASCIITable();
				break;
			case 'N': // Send several non-ASCII bytes.
				sendNonASCII();
				break;
			case 'L': // Send two-byte integers.
				sendLongs();
				break;
			case 'Q': // Send sequences of bytes.
				sendSequences();
				break;
			case 'R': // Send one message that exceeds Unicode range (and two others).
				sendOutOfRange();
				break;
			case 'a': // Simplest test, including \n at the end.
				sendAEOL();
				break;
			case 'z': // Another simple test, including \n at the end.
				sendZeroEOL();
				break;
			case 'o': // Another simple test, including \n at the end.
				sendOneEOL();
				break;
			case 's': // Groups of ten bytes incl. full ASCII table.
				sendASCIITableInOneGo();
				break;
			case 'V': // Valid and invalid ASCII.
				sendValidInvalid();
				break;
			case 'v': // Invalid and valid ASCII.
				sendInvalidValid();
				break;
			case 'E': // Valid and invalid ASCII with '\n' in between.
				sendValidEOLInvalid();
				break;
			case 'e': // Invalid and valid ASCII with '\n' in between.
				sendInvalidEOLValid();
				break;

			/*******************************************************************
			 * The following tests aren't used in any automated test sequences.
			 * They are only used in black-box testing of the entire application,
			 * including the GUI.
			 *******************************************************************/
			case 'u': // Unique bytes from sendSequences test.
				sendUnique();
				break;
			case 'l': // Two end cases of the long, 2-byte integers.
				serialSendLong(256); // 0x0100, smallest two-byte int.
				serialSendLong(65535); // 0xFFFF
				Serial.flush(); // Wait for the outgoing buffer to be cleared.
				break;
			case 'm': // Many bytes sent in one go.
				for(int i=0;i<131;i++) // Larger than the ASCII table.
				{
			  		Serial.write(0x41); // 'A'
			  		Serial.flush();
				}
				break;
			case 'x': // One of the two bytes that make the log stall. It's one
				// of the control bytes that is also sent in C0 and C1 test cases.
				Serial.write(0x90); // 58256 = 'ã'.
				Serial.flush();
				break;
			case 'X': // Similar to 'x' but sends 10 'A' before and after 0x90
				// in order to clearly show where the log stalls.
				sendAsAndControl();
				break;
			case 'y': // One of the two problematic control bytes, which has
			 	// turned out not to make the log stall.
				Serial.write(0x84); // 58756 = 'å'.
				Serial.flush();
				break;
			case 'c': // Send all the possible control characters interweaved with
				// 'A' to make sure the replacement works. Do not send the
				// terminating byte 0x9C, however, to stall the log.
				sendControl();
				Serial.flush();
				break;
			case 'C': // Send all the possible control characters, two at a time
				// to make sure the replacement works.Do not send the
				// terminating byte 0x9C, however, to stall the log.
				sendControlLongs();
				break;
			case 't': // Send command terminating byte 0x9C to unblock the log
				// after test cases c, C, x, X, and L.
				sendTerminatingByte();
				break;
		}
	}
}
