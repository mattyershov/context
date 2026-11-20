#include <SoftwareSerial.h>

const int rxPin = 10;
const int txPin = 11;
SoftwareSerial rs485Serial(rxPin, txPin);

void setup() {
  // 1. Start Hardware Serial for USB debugging
  Serial.begin(9600);
  Serial.println("Arduino Ready. Waiting for RS485 data...");

  rs485Serial.begin(9600);

  // Relay board
  for (int i = 2; i <= 9; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH); // Active-Low: HIGH is OFF
  }
}

void loop() {
  if (rs485Serial.available()) {
    String inData = rs485Serial.readStringUntil('\n');
    inData.trim();

    // 2. Print exactly what was received to your computer screen
    Serial.print("Received:");
    Serial.print(inData);
    Serial.print("| Length: ");
    Serial.println(inData.length());

    if (inData.length() == 2) {
      int port = inData[0] - '0';
      char value = inData[1];

      if (port >= 0 && port <= 7) {
        int targetPin = port + 2;
        Serial.print("Pin ");
        Serial.print(targetPin);

        if (value == '0') {
          digitalWrite(targetPin, HIGH);
          Serial.println("Set HIGH");
        } else if (value == '1') {
          digitalWrite(targetPin, LOW);
          Serial.println(" Set LOW");
        }
      } else {
        Serial.println("Error: Port number out of bounds.");
      }
    } else {
      Serial.println("Error: Command ignored because length != 2");
    }
  }
}