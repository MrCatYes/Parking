

#include <Stepper.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

const int stepsPerRevolution = 2048;  // changed ordering from default in sketch

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); 
// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int greenledPin =7;
const int redledPin = 5;
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
const int brightness = 255;

// defines variables
bool ok= true;
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
int offset = 0;
String lastname;
String firstname;

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(12); //16 doesn't always stick; 
  lcd.init();
  lcd.backlight();
  
 //  set the brightness of the red led to max
  analogWrite(redledPin, brightness);
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
int centerText(String text){
  offset = (16 - text.length())/2;
  return offset;
  }



void loop()
{
  distance = distanceCalcul();
     if (distance < 8 && ok == true) {
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
              lcd.setCursor(5,0);
              lcd.print("Acces");
              lcd.setCursor(4,1);
              lcd.print("Autorise");
              delay(3000);
              lcd.clear();

        // Display name
          while (Serial.available() > 0) {
            // Split Name and Firstname to display on 2 lines
              firstname = Serial.readStringUntil(' ');
              lastname = Serial.readString();
              lcd.setCursor(centerText(firstname), 0);
              lcd.print(firstname);
              lcd.setCursor(centerText(lastname), 1);
              lcd.print(lastname);              
                lcd.setCursor(16, 1);

          
          }
          // step one revolution  in one direction:
          digitalWrite(greenledPin, HIGH);
          digitalWrite(redledPin, LOW);
          
          myStepper.step(stepsPerRevolution/4); // 90 degree

          while (distance < 8){ //while distance < 8cm stay up
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
          lcd.clear();
          
      }
    
      if (stationnement == 0) {
              lcd.setCursor(5,0);
              lcd.print("Acces");
              lcd.setCursor(5,1);
              lcd.print("Refuse");
              delay(3000);
              lcd.clear();}
   }
   
}
