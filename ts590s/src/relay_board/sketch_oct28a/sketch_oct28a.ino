#include <SoftwareSerial.h>

const int rxPin = 0;
const int txPin = 1;
SoftwareSerial rs485Serial(rxPin, txPin);


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  rs485Serial.begin(9600);
  Serial.println("SH-U12 (MAX13487) RS485 Serial initialized.");

  // Relay board
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  

}
