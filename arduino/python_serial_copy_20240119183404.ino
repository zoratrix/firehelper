#include "Parser.h"
#include "AsyncStream.h"

#include <Servo.h>

Servo myservo;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5);
  myservo.attach(3);  // подключаем на пин 3
  myservo.write(90);
}



void loop() {

  if (Serial.available()>0) {

   String str = Serial.readString();

    if (str.toInt() == 0){
      myservo.write(90);
    }
    int degree = map(str.toInt(),0,90,45,135);
    myservo.write(180-degree);
    delay(15);
  } 
  
 
}