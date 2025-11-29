

#include <Stepper.h>

const int stepsPerRevolution = 2048;  // changed ordering from default in sketch

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); 


const int greenledPin =7;
const int redledPin = 5;
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04


// defines variables
bool ok= true;
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(12); //16 doesn't always stick; 

  pinMode(greenledPin, OUTPUT);
  pinMode(greenledPin, OUTPUT);
  digitalWrite(redledPin, HIGH);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  // initialize the serial port:
  Serial.begin(9600);
}
int distanceCalcul(){ // calcul the distance of the object
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
  return distance;
}

void loop()
{
  distance = distanceCalcul();
     if (distance<15 && ok == true) {
      // send 18 (random value) to Python
        Serial.write(18);
        // set false to avoid a loop
        ok = false;
     }
  if (Serial.available() > 0) {
      int stationnement = Serial.read() - '0'; // ASCII values that are being used in the subtraction
      ok =true;
      distance = distanceCalcul();  

      
      if (stationnement == 1) {
          // step one revolution  in one direction:
          digitalWrite(greenledPin, HIGH);
          digitalWrite(redledPin, LOW);
          
          myStepper.step(stepsPerRevolution/4); // 90 degree
  

          while (distance<15){ //while distance < 15cm stay up
              digitalWrite(trigPin, LOW);
              delayMicroseconds(2);
              distance = distanceCalcul();         
              }
          delay(5000); //5sec before go down
          digitalWrite(greenledPin,LOW );
          digitalWrite(redledPin, HIGH);
          // step one revolution in the other direction:
          myStepper.step(-stepsPerRevolution/4);
          delay(500);
          
      }
   }
}
