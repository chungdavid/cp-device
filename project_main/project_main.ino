#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include "BluetoothSerial.h"

const int SDA_PIN_BNO = 21;
const int SCL_PIN_BNO = 22;
const int SDA_PIN_BNO2 = 32;
const int SCL_PIN_BNO2 = 33;
const int FSR1_IN = 37; //placed on the forefoot
const int FSR2_IN = 38; //placed on the heel

const int PRESSURE = 1000; //5kg of pressure on the sensor corresponds to an analog reading of 4095

BluetoothSerial SerialBT;
TwoWire i2cPort2 = TwoWire(1);

//pin 21 is blue wire (SDA), pin 22 is yellow wire (SCL)
//this sensor will be placed on the top of the foot
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28); 

//pin 32 is blue wire (SDA), pin 33 is yellow wire (SCL)
//this sensor will be placed on the top of the foot
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28, &i2cPort2);

double z1; //foot sensor
double z2; //shin sensor
double jointAngle;
unsigned int heel = 0;
unsigned int toe = 0;
unsigned long timeElapsed;

void setup(void) 
{
  // SerialBT.begin("ESP32 Bluetooth - Group 8"); Enable the ESP to connect via bluetooth
  Serial.print("Init program");
  Serial.begin(4800); //init the serial monitor
  i2cPort2.begin(SDA_PIN_BNO2, SCL_PIN_BNO2, 100000); //init the second I2C port
  
  /* Initialise the sensors */
  if(!bno.begin() || !bno2.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    // SerialBT.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    Serial.print("Ooops, one or more BNO055 sensors not detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  delay(1000);
    
  bno.setExtCrystalUse(true);
  bno2.setExtCrystalUse(true);

  //program starts once the foot has been lifted off the ground (i.e., the gait cycle has started!)
  while(analogRead(FSR1_IN) >= PRESSURE || analogRead(FSR1_IN) >= PRESSURE) { }

  //initialize variables
}

void loop(void) 
{
  //get the sensor events
  sensors_event_t event; 
  bno.getEvent(&event);
  sensors_event_t event2; 
  bno2.getEvent(&event2);

  toe = (analogRead(FSR1_IN)>=PRESSURE) ? 1 : 0;
  heel = (analogRead(FSR2_IN)>=PRESSURE) ? 1 : 0;
    
  //On the right foot, sensors should be placed horizontally  (along the Z axis)
  //and the wires should be coming out the right side for the sensor and into the board AND the axis symbol should be on the TOP-LEFT of the board
  z1=event.orientation.z; //foot sensor
  z2=event2.orientation.z; //shin sensor
  jointAngle = 180-(z2-z1);

  timeElapsed = millis();

  // Serial.print("t: ");
  // Serial.print(timeElapsed);
  // Serial.print("\t");
  Serial.print("T:");
  Serial.print(toe);
  // Serial.print("\t");
  Serial.print("H:");
  Serial.print(heel);
  // Serial.print("\t");
  Serial.print("A:");
  Serial.println(jointAngle);

  //data format is T:<toe>H:<heel>A:<angle>
  
  delay(250);

}

