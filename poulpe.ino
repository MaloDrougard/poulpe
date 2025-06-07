// Libraries
#include <SPI.h>
#include <Ethernet.h>
#include <avr/wdt.h>
#include "Pompe.h"
#include "Log.h"
#include "Stepper.h"
#include "Api.h"

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
  10 : free
  11 : free
  12 : free
  13 : free

**/

unsigned long int serialBaud = 115200;
String command = "";

void setup(void)
{

  // Start Serial
  Serial.begin(serialBaud);
  info("Setup ...");

  setupStepper();
  setupPompes();

  // Start watchdog
  wdt_enable(WDTO_8S);
  info("Setup done");
}

// Read command from serial and store it in the argument
// return true if a command was readed, false otherwise
bool readSerial(String& command)
{
  bool bRet = false; 
  command = "";
  if (Serial.available())
  {
    command = Serial.readStringUntil('\n');
    command.trim();
    debug("Serial string recieved: " + command);
    bRet = true;
  }
  return bRet;
}




void loop()
{

  if(readSerial(command))
  {
    handleCommand(command); 
  }
  
  // check if some timeout has been reached
  pmChecking();

  // perform one step of the stepper motor if needed
  performOneStep();

  // watchdog reset
  wdt_reset();
}
