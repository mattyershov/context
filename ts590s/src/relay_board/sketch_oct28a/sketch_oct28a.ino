#include <SoftwareSerial.h>

const int rxPin = 10;
const int txPin = 11;
SoftwareSerial rs485Serial(rxPin, txPin);


void setup() {
  // put your setup code here, to run once:

  rs485Serial.begin(9600);

  // Relay board
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
  digitalWrite(8, HIGH);
  digitalWrite(9, HIGH);
}

  int[][] rs485Receive() {
    String inData = rs485Serial.readStringUntil("\n");
    inData.trim();
    

    for (char n : inData) {
      if (char == "[")
    }
  }


void loop() {

  if (rs485Serial.available()) {
    String inData = rs485Serial.readStringUntil("\n");
    inData.trim(); 








    // Data sent as an array of arrays, e.g., [[0, 1], [1, 1], [2, 0]], where each array contains a port ([0,8]) and a value (0 or 1)

    for (int i = 0; i < inData.length(); i++) {
      if (inData[i][1] == 0) {
        digitalWrite(inData[i][0] + 2, LOW);
      } else if (inData[i][1] == 1) {
        digitalWrite(inData[i][0] + 2, HIGH);
      }
        rs485Serial.println(inData);
    }

  }
}
 
