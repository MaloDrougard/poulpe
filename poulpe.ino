// Libraries
#include <SPI.h>
#include <Ethernet.h>
#include <avr/wdt.h>
#include "Pompe.h"
#include "Log.h"
#include "Api.h"
#include "Stepper.h"

using namespace mylog; 


/**
  PIN ASSIGNMENT:

DIGITAL:
  00 : none
  01 : none
  02 : step motor direction
  03 : step motor step
  04 : sd
  05 : p1
  06 : p2
  07 : p3
  08 : p4
  09 : grand-p5
  10 : eth
  11 : eth
  12 : eth
  13 : eth
  
**/

unsigned long int serialBaud = 115200;





void setup(void) {
  
  // Start Serial
  Serial.begin(serialBaud);
  info("Setup ...");

  setupStepper();
  setupPompes();

  // Start watchdog
  wdt_enable(WDTO_8S);
  info("Setup done");
}

void readSerial() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    info("Serial command recieved: " + command);
    if (command.startsWith("rotation")) 
    {
      rotation(10.0);
    }
  }
}


void loop() {

  // read serial command
  readSerial();

  // check if some timeout has been reached
  //pmChecking();

  // perform one step of the stepper motor if needed
  performOneStep();

  // watchdog reset
  wdt_reset();
}
