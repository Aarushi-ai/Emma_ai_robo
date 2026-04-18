#include <Servo.h>     //Standard Arduino servo library (controls PWM servo motors)
#include <cvzone.h>    //cvzone library for serial communication with Python

//Declaration of servo objects
Servo LServo; // left servo
Servo RServo; // right servo
Servo HServo; // head servo

//Define the servo control pins
const int LS_pin = 8;
const int RS_pin = 9;
const int HS_pin = 10;

//Initialize serial data to receive 3 values from three servo motors and
//each servo motor will have angles of rotation from 0 degree to 180 degrees
//so three digits of values received  so we pass the parameter (3,3) in the
//constructor of the SerialData class whose parameters are (int numOfValRec, int digitsOfVal)
SerialData serialData(3,3); //python code sends angles
int valsRec[3];             //Array to store the received values of angles for each servo motor


void setup() {

  // put your setup code here, to run once:
  serialData.begin(9600);   //Initializes Serial Data Communication at 9600 baud rate

  //Attach Servo motors to their respective pins
  LServo.attach(LS_pin);
  RServo.attach(RS_pin);
  HServo.attach(HS_pin);

  //Move servos to safe home positions on startup
  LServo.write(180);  //left arm up
  RServo.write(0);    //right arm down
  HServo.write(90);   //head centered
}

void loop() {
  // put your main code here, to run repeatedly:
  serialData.Get(valsRec);      //Angles received from Python

  LServo.write(valsRec[0]);     //Set the left servo to the received position
  RServo.write(valsRec[1]);     //Set the right servo to the received position
  HServo.write(valsRec[2]);     //Set the head servo to the received position
}