// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// ---------------------------------------------------------------- //

//Echo Sensor

#define echoPin1 2 //pins for sensors 1-4
#define trigPin1 3
#define echoPin2 4 
#define trigPin2 5 
#define echoPin3 6 
#define trigPin3 7 
#define echoPin4 8 
#define trigPin4 9

#define echoPin5 54 //pins for sensors 5-8
#define trigPin5 55
#define echoPin6 56
#define trigPin6 57 
#define echoPin7 58 
#define trigPin7 59 
#define echoPin8 60 
#define trigPin8 61   


long duration1; // variable for the duration of sound wave travel
int distance1; // variable for the distance measurement
long duration2; 
int distance2; 
long duration3; 
int distance3; 
long duration4; 
int distance4; 

long duration5; 
int distance5;
long duration6; 
int distance6;
long duration7; 
int distance7;
long duration8; 
int distance8;

//------------------------------------------------------------------//

//Accelerometer

#include "Wire.h"
#include <MPU6050_light.h>
MPU6050 mpu(Wire);
long timer = 0;
long AngleX, AngleY, AngleZ;

//------------------------------------------------------------------//

//Buttons

#define buttonPin1 62
int buttonState1 = 0;
int lastButtonState1 = 1;


#define buttonPin2 63
int buttonState2 = 0;
int lastButtonState2 = 1;

//------------------------------------------------------------------//

//Limit Switches

#define limitPin1 68
int limitState1 = 0;
int lastLimitState1 = 0;


#define limitPin2 69
int limitState2 = 0;
int lastLimitState2 = 0;

//------------------------------------------------------------------//

//Optical Sensor

/*  CS = 22
 *  MISO = 50
 *  MOSI = 51
 *  SCK = 52 
 */
#include "Bitcraze_PMW3901.h"
Bitcraze_PMW3901 flow(22); //defining pin 22 for CS

int16_t deltaX,deltaY; //values for the X and Y deltas
long coordX, coordY;

//------------------------------------------------------------------//

void setup() {
  
  // ECHO setup 
  pinMode(trigPin1, OUTPUT); 
  pinMode(echoPin1, INPUT); 
  
  pinMode(trigPin2, OUTPUT); 
  pinMode(echoPin2, INPUT); 
  
  pinMode(trigPin3, OUTPUT); 
  pinMode(echoPin3, INPUT); 
  
  pinMode(trigPin4, OUTPUT); 
  pinMode(echoPin4, INPUT); 

  pinMode(trigPin5, OUTPUT); 
  pinMode(echoPin5, INPUT); 
  
  pinMode(trigPin6, OUTPUT); 
  pinMode(echoPin6, INPUT); 
  
  pinMode(trigPin7, OUTPUT); 
  pinMode(echoPin7, INPUT); 
  
  pinMode(trigPin8, OUTPUT); 
  pinMode(echoPin8, INPUT); 
  
  //------------------------------------------------------------------//

  //MPU setup
  Wire.begin();
  byte status = mpu.begin();
  while(status!=0){ } // stop everything if could not connect to MPU6050
  mpu.calcOffsets(true,true); // gyro and accelero

  //------------------------------------------------------------------//

  //Button setup
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  
  //------------------------------------------------------------------//

  //Limit switches setup
  pinMode(limitPin1, INPUT);
  pinMode(limitPin2, INPUT);
  
  //------------------------------------------------------------------//

  //Optical Sensor setup

  if (!flow.begin()) { //stop everything if cannot connect to PMW 3901
    while(1) { }
  }

  //------------------------------------------------------------------//

  //Serial setup
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  Serial.println("SENSOR");
  delay(10);
  
}
void loop() {
  echoreading();
  limitdetect();
  accelreading();
  buttondetect();
  opticalreading();



//  delay(100);
//  Serial.print(lastButtonState); Serial.print(" ");
//  Serial.println(buttonState);
//  for(int i = 0; i < 5; i++){
//    accelwarning();
//    
//  }
//  Serial.println("5 times alr");

  




}



void echoreading(){

  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  duration1 = pulseIn(echoPin1, HIGH);
  distance1 = duration1 * 0.034 / 2; 
  delay(10);

  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  duration2 = pulseIn(echoPin2, HIGH);
  distance2 = duration2 * 0.034 / 2; 
  delay(10);

  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);
  duration3 = pulseIn(echoPin3, HIGH);
  distance3 = duration3 * 0.034 / 2; 
  delay(10);

  digitalWrite(trigPin4, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin4, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin4, LOW);
  duration4 = pulseIn(echoPin4, HIGH);
  distance4 = duration4 * 0.034 / 2; 
  delay(10);
  

  digitalWrite(trigPin5, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin5, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin5, LOW);
  duration5 = pulseIn(echoPin5, HIGH);
  distance5 = duration5 * 0.034 / 2;
  delay(10);  

  digitalWrite(trigPin6, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin6, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin6, LOW);
  duration6 = pulseIn(echoPin6, HIGH);
  distance6 = duration6 * 0.034 / 2;
  delay(10);  


  digitalWrite(trigPin7, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin7, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin7, LOW);
  duration7 = pulseIn(echoPin7, HIGH);
  distance7 = duration7 * 0.034 / 2;
  delay(10);  


  digitalWrite(trigPin8, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin8, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin8, LOW);
  duration8 = pulseIn(echoPin8, HIGH);
  distance8 = duration8 * 0.034 / 2;
  delay(10);  

  
  Serial.print("ECHO ");Serial.print(distance1);Serial.print(" ");Serial.print(distance2);Serial.print(" ");Serial.print(distance3);Serial.print(" ");Serial.print(distance4);
  Serial.print(" ");Serial.print(distance5);Serial.print(" ");Serial.print(distance6);Serial.print(" ");Serial.print(distance7);Serial.print(" ");Serial.println(distance8);



}



void accelreading(){

  mpu.update();
  Serial.print("ACCEL ");
  //rotation around the axis in angles
  Serial.print(mpu.getAngleX()); Serial.print(" ");
  Serial.print(mpu.getAngleY()); Serial.print(" ");
  Serial.println(mpu.getAngleZ()); //use this to detect if turning is executed correctly


}

void buttondetect(){

//Button 1
  buttonState1 = digitalRead(buttonPin1);
  if(buttonState1 != lastButtonState1){
    if(lastButtonState1 == LOW){ //if this is a transition from LOW to HIGH aka pressing button
      Serial.println("B1");
    }
  }
  lastButtonState1 = buttonState1;
//  delay(50);

//Button 2
  buttonState2 = digitalRead(buttonPin2);
  if(buttonState2 != lastButtonState2){
    if(lastButtonState2 == LOW){ //if this is a transition from LOW to HIGH aka pressing button
      Serial.println("B2");
    }
  }
  lastButtonState2 = buttonState2;
//  delay(50);
}

void limitdetect(){
  limitState1 = digitalRead(limitPin1);
  if(limitState1 != lastLimitState1){
    if(lastLimitState1 == LOW){ //if this is a transition from LOW to HIGH aka pressing button
      Serial.println("CLEAR");
    }
    else{
      Serial.println("BUMP");
    }
  }
  lastLimitState1 = limitState1;
//  delay(50);

  limitState2 = digitalRead(limitPin2);
    if(limitState2 != lastLimitState2){
      if(lastLimitState2 == LOW){ //if this is a transition from LOW to HIGH aka pressing button
        Serial.println("CLEAR");
      }
      else{
        Serial.println("BUMP");
      }
    }
    lastLimitState2 = limitState2;
}

void opticalreading(){
  //X and Y axis are pointing towards the right and back originally
  // Get motion count since last call
  flow.readMotionCount(&deltaX, &deltaY);

//  coordX += deltaX;
//  coordY += deltaY;
  
//  Serial.print("OPTICAL "); Serial.print(coordY); Serial.print(" "); Serial.println(coordX);
//  Serial.print("XCoord: "); Serial.print(coordX); Serial.print(" YCoord: "); Serial.println(coordY);
  
  Serial.print("OPTICAL ");
  Serial.print(-deltaY);
  Serial.print(" ");
  Serial.println(deltaX);

//  delay(100);
}
