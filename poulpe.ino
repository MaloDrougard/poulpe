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

// Enter a MAC address for your controller below.
byte mac[] = { 0x90, 0xA1, 0xDA, 0x0E, 0xFE, 0x40 };
// IP address in case DHCP fails
IPAddress ip(192, 168, 1, 13);
// Ethernet server
EthernetServer server(80);



void setupEthernet() {
  info("Setting up Ethernet ...");
  // Start the Ethernet connection and the server
  if (Ethernet.begin(mac, 1000, 1000) == 0) {
    info("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    // try to configure using IP address instead of DHCP:
    char ipStr[16];
    snprintf(ipStr, sizeof(ipStr), "%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
    info(ipStr);
    Ethernet.begin(mac, ip);
  }

  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    info("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1); // do nothing, no point running without Ethernet hardware
    }
  }
  if (Ethernet.linkStatus() == LinkOFF) {
    info("Ethernet cable is not connected.");
  }

  delay(1000); 
  server.begin();
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
}




void setup(void) {
  
  // Start Serial
  Serial.begin(serialBaud);
  info("Setup ...");  

  setupStepper();
  setupPompes();
  setupEthernet(); 

  // Start watchdog
  wdt_enable(WDTO_8S);
  info("Setup done");
}


void loop() {
  EthernetClient client = server.available();
  handleRoot(client);  
  // check if some timeout has been reached
  pmChecking();

  // perform one step of the stepper motor if needed
  performOneStep();

  // watchdog reset
  wdt_reset();
}
