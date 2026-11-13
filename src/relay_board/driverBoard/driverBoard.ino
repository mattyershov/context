#include <SoftwareSerial.h>

const int rxPin = 10;
const int txPin = 11;
SoftwareSerial rs485Serial(rxPin, txPin);


void setup() {
  rs485Serial.begin(9600);

  // Relay board
  for (int i = 2; i <= 9; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }
}



void loop() {

  if (rs485Serial.available()) {
    String inData = rs485Serial.readStringUntil('\n');
    inData.trim(); 

    // Data sent as an array of arrays, e.g., [[0, 1], [1, 1], [2, 0]], where each array contains a port ([0,7]) and a value (0 or 1)
    // Currently, data can only be sent as a 1D array, for testing purposes. TODO: Add tags to differentiate between exclusive vs. additive antenna selections.

    if (inData.length() == 2) {
      int port = inData[0] - '0';
      char value = inData[1];

      if (port >= 0 && port <= 7) {
        int targetPin = port + 2;


        if (value == '0') {
          digitalWrite(targetPin, LOW);
        } else if (value == '1') {
          digitalWrite(targetPin, HIGH);
        }
      }
    }
    rs485Serial.println(inData);
  }
}