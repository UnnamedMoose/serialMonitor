/* This Arduino code is supposed to run together with a corresponding
 * SerialMonitor test script. The test script will send a command to the Arduino
 * to execute a given test case (send certain data through the serial port).
 * The test script will then compare the data that if received to the expected
 * results in order to determine whether the test has been successful or not.
 * */

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

	  // Go on to the next character.
	  thisByte++;
	}
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
			case 'S': // Send an entire ASICC table.
				sendASCIITable();
				break;
			case 'N': // Send several non-ASICC bytes.
				sendNonASCII();
				break;
		}
	}
}
