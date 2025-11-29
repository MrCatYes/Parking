

#include <Stepper.h>

const int stepsPerRevolution = 2048;  // changed ordering from default in sketch

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); 

// pushbutton pin
const int buttonPin = 4;
const int greenledPin =7;
const int redledPin = 5;
bool buttonState; 
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
byte lastButtonState = LOW;
byte currentButtonState = LOW;
unsigned long lastButtonDebounceTime = 0;
unsigned long buttonDebounceDelay = 20;

// defines variables
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(12); //16 doesn't always stick; 
  pinMode(buttonPin, INPUT);
  pinMode(greenledPin, OUTPUT);
  pinMode(greenledPin, OUTPUT);
  digitalWrite(redledPin, HIGH);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  // initialize the serial port:
  Serial.begin(9600);
}

void loop()
{
  byte readValue = digitalRead(buttonPin);

  if (readValue != lastButtonState) {
    lastButtonDebounceTime = millis();
  }

  if (millis() - lastButtonDebounceTime > buttonDebounceDelay) {
    if (readValue != currentButtonState) {
      currentButtonState = readValue;
      if (currentButtonState == HIGH) {
        Serial.write(18);
      }
    }
  }

  lastButtonState = readValue;

  if (Serial.available() > 0) {
    int stationnement = Serial.read() - '0';
        // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor


    if (stationnement == 1) {
  // step one revolution  in one direction:
  digitalWrite(greenledPin, HIGH);
  digitalWrite(redledPin, LOW);
  myStepper.step(stepsPerRevolution/4);

 
  while (distance<15){
      digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor

  }
  delay(5000);
  // step one revolution in the other direction:
   digitalWrite(greenledPin,LOW );
  digitalWrite(redledPin, HIGH);
  myStepper.step(-stepsPerRevolution/4);
  delay(500);
  
  
    }
  }
}
