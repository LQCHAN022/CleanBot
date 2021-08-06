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

//Button

#define buttonPin1 62
int buttonState1 = 0;
int lastButtonState1 = 0;

//Not implemented yet
//int buttonPin2 = 63;
//int buttonState2 = 0;
//int lastButtonState2 = 0;

//------------------------------------------------------------------//

//Limit Switches

#define limitPin1 68
int limitState1 = 0;
int lastLimitState1 = 0;

//Not implemented yet
#define limitPin2 69
int limitState2 = 0;
int lastLimitState2 = 0;

//------------------------------------------------------------------//


void setup() {
  pinMode(trigPin1, OUTPUT); 
  pinMode(echoPin1, INPUT); 
  
  pinMode(trigPin2, OUTPUT); 
  pinMode(echoPin2, INPUT); 
  
  pinMode(trigPin3, OUTPUT); 
  pinMode(echoPin3, INPUT); 
  
  pinMode(trigPin4, OUTPUT); 
  pinMode(echoPin4, INPUT); 
  
  //------------------------------------------------------------------//
  
  Wire.begin();
  byte status = mpu.begin();
  while(status!=0){ } // stop everything if could not connect to MPU6050
  mpu.calcOffsets(true,true); // gyro and accelero

  //------------------------------------------------------------------//

  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  
  //------------------------------------------------------------------//

  pinMode(limitPin1, INPUT);
  
  //------------------------------------------------------------------//
  
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  Serial.println("SENSOR");
  
}
void loop() {
  echoreading();
  limitdetect();
  accelreading();
  buttondetect();
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
  Serial.print("ECHO ");Serial.print(distance1);Serial.print(" ");Serial.print(distance2);Serial.print(" ");Serial.print(distance3);Serial.print(" ");Serial.println(distance4);
  delay(10);


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
  
  buttonState1 = digitalRead(buttonPin1);
//  Serial.println(buttonState1);
  if(buttonState1 != lastButtonState1){
    if(lastButtonState1 == LOW){ //if this is a transition from LOW to HIGH aka pressing button
//      buttonTog1 = buttonTog1?0:1;
//      digitalWrite(LED_BUILTIN, buttonTog1);
//      Serial.print("ButtonTog1: "); Serial.println(buttonTog1);
      Serial.println("B1");
    }
  }
  lastButtonState1 = buttonState1;
  delay(50);
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
  delay(50);
}
