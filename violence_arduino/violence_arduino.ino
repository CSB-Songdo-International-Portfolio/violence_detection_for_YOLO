int ledPin = 13;  // Assuming the LED is connected to digital pin 13

void setup() {
  // Start the serial communication at 9600 baud
  Serial.begin(9600);
  
  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming byte:
    int violenceCount = Serial.parseInt();

    // If the violence count is greater than or equal to 1, turn the LED on
    if (violenceCount >= 1) {
      digitalWrite(ledPin, HIGH);  // Turn the LED on
    } else {
      digitalWrite(ledPin, LOW);   // Turn the LED off
    }
  }
}