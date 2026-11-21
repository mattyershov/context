#include <SoftwareSerial.h>

// USER-DEFINED CONSTANTS
//-----------------------
const int address = 0;
const int num_relays = 8;
//-----------------------

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

    Serial.print("Received:");
    Serial.print(inData);
    Serial.print("| Length: ");
    Serial.println(inData.length());

    if (inData.length() == 5) {
      int addr = inData.substring(0, 2).toInt();
      Serial.println(addr);
      int subaddr = inData.substring(2, 4).toInt();
      char value = inData[4];

      if (addr == address && subaddr >= 0 && subaddr < num_relays) {
        int targetPin = subaddr + 1;
        Serial.print("Pin ");
        Serial.print(targetPin);

        if (targetPin >= 1) {

          if (value == '0') {
            digitalWrite(targetPin, HIGH);
            Serial.println("Set HIGH");

          } else if (value == '1') {
            digitalWrite(targetPin, LOW);
            Serial.println(" Set LOW");

          } else if (value == '2') {
            digitalWrite(targetPin, LOW);
            Serial.println(" Set XLOW");
            for (int i = 2; i < num_relays; i++) {
              if (i != targetPin) {
                digitalWrite(i, HIGH);
              }
            }
          }
        }
        
      } else {
        Serial.println("Error: Port number out of bounds.");
      }
    } else {
      Serial.println("Error: Command ignored because length != 5");
    }
  }
}