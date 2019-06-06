/* This Arduino code is supposed to run together with a corresponding
 * SerialMonitor test script. The test script will send a command to the Arduino
 * to execute a given test case (send certain data through the serial port).
 * The test script will then compare the data that if received to the expected
 * results in order to determine whether the test has been successful or not.
 * */

void sendA(void)
/* Send 'A' character, followed by a 0x41 (corresponding ASCII code). */
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
		}
	}
}
