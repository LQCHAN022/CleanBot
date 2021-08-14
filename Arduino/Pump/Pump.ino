#include <string.h>

#define PWM_pin 6

String incomingstr = "";
char* state;
long PWM_val;

void setup() {
  // put your setup code here, to run once:
  pinMode(6, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(5);
  Serial.println("PUMP");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) { //this whooole chunk is for dealing with serial input
    
  
    incomingstr = Serial.readString(); //reading string and then converting it to char array to use token
    char incoming[incomingstr.length()];
    incomingstr.toCharArray(incoming, incomingstr.length());

    state = strtok(incoming, " "); //extracting the first and second parameters
    char* PWM_val_str = strtok(NULL, " ");

    //data processing by converting dist to int and string to upper
    sscanf(PWM_val_str, "%d", &PWM_val);
    strupr(state); //converts string to uppercase

    
    if (strcmp(state, "ON") == 0) {      //front dir
      analogWrite(PWM_pin, PWM_val);
      digitalWrite(LED_BUILTIN, HIGH);
//      Serial.print("ON: ");Serial.println(PWM_val);
      }
    else if (strcmp(state, "OFF") == 0){
      digitalWrite(PWM_pin, LOW);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("OFF");
      }
    }
}
