/*This edition comments out various print statements that might be useful for debugging, but are not necessary for actual implementation
 * 
 * 
 */

#include <AccelStepper.h>   //add libraries
#include <string.h>

#define xstep 54 // define pins and steppers
#define xdir 55
#define xen 38

#define ystep 60
#define ydir 61
#define yen 56

#define zstep 46
#define zdir 48
#define zen 62

#define estep 26
#define edir 28
#define een 24

#define qstep 36
#define qdir 34
#define qen 30



AccelStepper stepper1(1, xstep, xdir); //define steppers
AccelStepper stepper2(1, ystep, ydir);
AccelStepper stepper3(1, zstep, zdir);
AccelStepper stepper4(1, estep, edir);
AccelStepper stepper5(1, qstep, qdir);



String incomingstr = "";  // Data received from the serial port

int valC = 1;
int runFlag = 0;    //Run the stepper
int cleanFlag = 0;
long target = 0;
int startTime;    //for calc speed
int spd = 8192; //number of steps per revolution
char* dir;
long dist;

void setup() {
  pinMode(xen, OUTPUT); //enabling the motors
  digitalWrite(xen, LOW);
  pinMode(yen, OUTPUT);
  digitalWrite(yen, LOW);
  pinMode(zen, OUTPUT);
  digitalWrite(zen, LOW);
  pinMode(een, OUTPUT);
  digitalWrite(een, LOW);
  pinMode(qen, OUTPUT);
  digitalWrite(qen, LOW);
  
  
  Serial.begin(9600); // Start serial communication at 9600 bps
  Serial.setTimeout(5);   //reading the serial takes 3ms - if this isnt hear it will take 1000ms

  stepper1.setPinsInverted(true, false, false); //invert direction pins due to orientation
  stepper3.setPinsInverted(true, false, false);
  stepper5.setPinsInverted(true, false, false);
  
  stepper1.setMaxSpeed(8192*2); //setting MaxSpeed of motors
  stepper2.setMaxSpeed(8192*2);
  stepper3.setMaxSpeed(8192);
  stepper4.setMaxSpeed(8192);
  stepper5.setMaxSpeed(8192);

  stepper1.setAcceleration(1000);
  stepper2.setAcceleration(1000);
  stepper3.setAcceleration(1000);
  stepper4.setAcceleration(1000);
  stepper5.setAcceleration(1000);

  Serial.println("MOVEMENT");
}

void loop() {
  if (Serial.available()) { //this whooole chunk is for dealing with serial input
//    startTime = millis();
    
    incomingstr = Serial.readString(); //reading string and then converting it to char array to use token
    char incoming[incomingstr.length()];
    incomingstr.toCharArray(incoming, incomingstr.length());

    dir = strtok(incoming, " "); //extracting the first and second parameters
    char* distString = strtok(NULL, " ");

    //data processing by converting dist to int and string to upper
    sscanf(distString, "%d", &dist);
    strupr(dir); //converts string to uppercase

    
    if (strcmp(dir, "FRONT") == 0) {      //front dir
      int distused = (dist==-1)?-1000:dist;
      stepper1.move(distused);
      stepper2.move(distused);
      stepper3.move(distused);
      stepper4.move(distused);

      stepper1.setSpeed(spd);
      stepper2.setSpeed(spd);
      stepper3.setSpeed(spd);
      stepper4.setSpeed(spd);
      
      if(dist == -1){
        target = distused;
        valC = 11; //continuous
      }
      else{
        target = stepper2.distanceToGo();
//        Serial.println("FRONT config loaded");
        valC = 1; //all move at spd
      }
    }
    
    else if (strcmp(dir, "BACK") == 0) {      //back dir
      int distused = (dist==-1)?1000:-dist;
      stepper1.move(distused);
      stepper2.move(distused);
      stepper3.move(distused);
      stepper4.move(distused);

      stepper1.setSpeed(-spd);
      stepper2.setSpeed(-spd);
      stepper3.setSpeed(-spd);
      stepper4.setSpeed(-spd);
      
      if(dist == -1){
        target = distused;
        valC = 11; //continuous
      }
      else{
        target = stepper2.distanceToGo();
//        Serial.println("BACK config loaded");
        valC = 1; //all move at spd
      }
    }

    
    else if (strcmp(dir, "E") == 0) {      //turn clockwise
      
        stepper1.move(dist);
        stepper2.move(-dist);
        stepper3.move(dist);
        stepper4.move(-dist);
        
        stepper1.setSpeed(spd);
        stepper2.setSpeed(-spd);
        stepper3.setSpeed(spd);
        stepper4.setSpeed(-spd);
      
      
        target = stepper2.distanceToGo();
//        Serial.println("ROTATE CW config loaded");
        valC = 1; //all move at spd
 
    }

    else if (strcmp(dir, "Q") == 0) {      //turn dir
     
     
        stepper1.move(-dist);
        stepper2.move(dist);
        stepper3.move(-dist);
        stepper4.move(dist);
        
        stepper1.setSpeed(-spd);
        stepper2.setSpeed(spd);
        stepper3.setSpeed(-spd);
        stepper4.setSpeed(spd);
      
        target = stepper2.distanceToGo();
//        Serial.println("ROTATE CCW config loaded");
        valC = 1; //all move at spd
 
    }

    else if (strcmp(dir, "LEFT") == 0) {      //turn dir
        stepper1.move(-dist);
        stepper2.move(dist);
        stepper3.move(dist);
        stepper4.move(-dist);
        
        stepper1.setSpeed(-spd);
        stepper2.setSpeed(spd);
        stepper3.setSpeed(spd);
        stepper4.setSpeed(-spd);
      
        target = stepper2.distanceToGo();
//        Serial.println("LEFT config loaded");
        valC = 1; //all move at spd
    }

    else if (strcmp(dir, "RIGHT") == 0) {      //turn dir
        stepper1.move(dist);
        stepper2.move(-dist);
        stepper3.move(-dist);
        stepper4.move(dist);
        
        stepper1.setSpeed(spd);
        stepper2.setSpeed(-spd);
        stepper3.setSpeed(-spd);
        stepper4.setSpeed(spd);
      
        target = stepper1.distanceToGo();
//        Serial.println("RIGHT config loaded");
        valC = 1; //all move at spd
    }

    else if (strcmp(dir, "CORNER") == 0) {      //back dir
      if (dist>=0){ //clockwise
        stepper1.move(dist);
        stepper2.move(0);
        stepper3.move(dist);
        stepper4.move(0);
        
        stepper1.setSpeed(spd);
        stepper2.setSpeed(0);
        stepper3.setSpeed(spd);
        stepper4.setSpeed(0);
        valC = 1; //run to target, stepper 1 as reference
      }
      else{  //anti-clockwise
        stepper1.move(0);
        stepper2.move(-dist);
        stepper3.move(0);
        stepper4.move(-dist);

        stepper1.setSpeed(0);
        stepper2.setSpeed(spd);
        stepper3.setSpeed(0);
        stepper4.setSpeed(spd);
        valC = 2; //run to target, stepper 2 as reference
      }
      
        target = dist;
//        Serial.println("CORNER config loaded");
      
    }

    
    
    
    else if (strcmp(dir, "R") == 0) {   //if recieved R then run
      runFlag = 1;
      dist = 0;
    }
    
    else if (strcmp(dir, "S") == 0) {   //if recieved S then stop
      runFlag = 0;
      Serial.println("STOPPED");
    }
    
    else if (strcmp(dir, "I") == 0) {   //if recieved I then show current positions
      Serial.print("Stepper 1 position = ");
      Serial.println(stepper1.currentPosition());
      Serial.print("Stepper 2 position = ");
      Serial.println(stepper2.currentPosition());
      Serial.print("Stepper 3 position = ");
      Serial.println(stepper3.currentPosition());
      Serial.print("Stepper 4 position = ");
      Serial.println(stepper4.currentPosition());

      Serial.print("Stepper 1 dist left = ");
      Serial.println(stepper1.distanceToGo());
      Serial.print("Stepper 2 dist left = ");
      Serial.println(stepper2.distanceToGo());
      Serial.print("Stepper 3 dist left = ");
      Serial.println(stepper3.distanceToGo());
      Serial.print("Stepper 4 dist left = ");
      Serial.println(stepper4.distanceToGo());
    }
    
    else if (dir == "X") {   //reset the board
      Serial.println("RESET");
      delay(500);                         //delay so that the print can finish
      void software_Reset();      {
        asm volatile ("  jmp 0");
      }
    }

    else if (strcmp(dir, "CLEAN") == 0) {      //turn dir
        cleanFlag = dist;
        stepper5.setSpeed(dist);
//        Serial.println("cleanFlag: ");Serial.println(cleanFlag);

    }
    
    else if (strcmp(dir, "OFF") == 0) {      //turn off everything
        digitalWrite(xen, HIGH);
        digitalWrite(yen, HIGH);
        digitalWrite(zen, HIGH);
        digitalWrite(een, HIGH);
        digitalWrite(qen, HIGH);
       
    }

    else if (strcmp(dir, "ON") == 0) {      //turn on everything
        digitalWrite(xen, LOW);
        digitalWrite(yen, LOW);
        digitalWrite(zen, LOW);
        digitalWrite(een, LOW);
        digitalWrite(qen, LOW);
 
    }
    
    else {
      Serial.println("Incorrect Code!");    //if its not one of the recognised letters
      Serial.print("Incorrect input--");Serial.print("Dir: "); Serial.print(dir); Serial.print(" Dist: "); Serial.println(dist);
    }
//    Serial.print("Dir: "); Serial.print(dir); Serial.print(" --Dist: "); Serial.print(dist); Serial.print(" --Target: "); Serial.print(target); Serial.print(" --Config: ");Serial.println(valC);
//    Serial.print(" --runFlag: "); Serial.println(runFlag);
  }


  if (cleanFlag > 0){
    stepper5.runSpeed();
  }

  if (runFlag == 1) {   //if run command was sent
    switch(valC){
      case 1: //for front
        
        stepper1.runSpeed();
        stepper2.runSpeed();
        stepper3.runSpeed();
        stepper4.runSpeed();
        target = stepper1.distanceToGo();
        break;
        
      case 11: //front continuous there's some issue here that makes it run slow; nah no issue alr it's a hardware limitation thing
        stepper1.runSpeed();
        stepper2.runSpeed();
        stepper3.runSpeed();
        stepper4.runSpeed();
        target = 1000;
        break;
        
      case 2: //for back       
        stepper1.runSpeed();
        stepper2.runSpeed();
        stepper3.runSpeed();
        stepper4.runSpeed();
        target = stepper2.distanceToGo();
        break;
        
      case 3:
        stepper1.setSpeed(spd);
        stepper2.setSpeed(spd);
        stepper3.setSpeed(spd);
        stepper4.setSpeed(spd);
        stepper1.setAcceleration(1000);
        stepper2.setAcceleration(1000);
        stepper3.setAcceleration(1000);
        stepper4.setAcceleration(1000);
  
        stepper1.run();
        stepper2.run();
        stepper3.run();
        stepper4.run();

        target = stepper2.distanceToGo();
        break;
      case 999:
        stepper1.setAcceleration(1000);
        stepper2.setAcceleration(1000);
        stepper3.setAcceleration(1000);
        stepper4.setAcceleration(1000);
        stepper1.runToPosition();
        stepper2.runToPosition();
        stepper3.runToPosition();
        stepper4.runToPosition();
        runFlag = 0;
//        Serial.println("case 999 ended");
        break;
    }

    if (target == 0) {   //if the stepper has reached destination
      runFlag = 0;                              //turn off run flag
      Serial.println("Move complete");
      }
  }
}


  
