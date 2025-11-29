#include <MusicBuzzer.h>


#include<SoftwareSerial.h>

int sensorPin = A0; // select the input pin for the LDR

int sensorValue = 0; // variable to store the value coming from the sensor


int buzzer = 12; // Output pin for Buzzer

void setup() {

// declare the ledPin and buzzer as an OUTPUT:


pinMode(buzzer,OUTPUT);
music.init(buzzer);

Serial.begin(9600);

}

void loop()

{



sensorValue = analogRead(sensorPin);

Serial.println(sensorValue);

if (sensorValue >0)

{

Serial.println("Fire Detected");
music.imperialmarch();


digitalWrite(buzzer,HIGH);

delay(1000);

}


digitalWrite(buzzer,LOW);

delay(sensorValue);

}
