// Libraries
#include <SPI.h>
#include <Ethernet.h>
#include <avr/wdt.h>
#include "Pompe.h"
#include "Log.h"
#include "Api.h"

using namespace mylog; 


/**
  PIN ASSIGNMENT:

DIGITAL:
  00 : none
  01 : none
  02 : none
  03 : none
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

const int pmSize = 5; // the array can have contains all the diigtal pins 
Pompe pm[pmSize];


void pmChecking() {
  for (int i = 0; i < pmSize; i++) {
    pm[i].checkTiming();
  }
}


int pmPrint(String dummy) {
  for (int i = 0; i < pmSize; i++) {
    pm[i].print();
  }
  return 0;
}


int setPompe(String command) {
  trace(__func__, command.c_str());

  char buffer[100];
  snprintf(buffer, sizeof(buffer), "Set pompe with arg: %s", command.c_str());
  info(buffer);

  int splitPos = command.indexOf("-");
  if (splitPos < 0) {
    snprintf(buffer, sizeof(buffer), "invalid parameter: %s", command.c_str());
    error(buffer);
    return -1;
  }

  String strPompeIdx = command.substring(0, splitPos);
  int pompeIdx = strPompeIdx.toInt();
  String strTime = command.substring(splitPos + 1, command.length());
  unsigned long time = strTime.toInt();  // command is time in millisec, important not to use int because of the buffer overflow

  if (pompeIdx >= pmSize) {
    snprintf(buffer, sizeof(buffer), "out of bound index: %d", pompeIdx);
    error(buffer);
    return -2;
  }

  snprintf(buffer, sizeof(buffer), "set pompe: %d", pompeIdx);
  info(buffer);

  pm[pompeIdx].setStateFor(HIGH, time);

  return 0;
}


void setupEthernet() {
  // Start the Ethernet connection and the server
  if (Ethernet.begin(mac) == 0) {
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


void setupPompes() {
  pm[0].mysetup(5);
  pm[1].mysetup(6);
  pm[2].mysetup(7);
  pm[3].mysetup(8);
  pm[4].mysetup(9);
}



void setup(void) {
  
  // Start Serial
  Serial.begin(serialBaud);
  info("Setup ...");  

  setupPompes();
  setupEthernet(); 

  // Start watchdog
  wdt_enable(WDTO_4S);
  info("Setup done");
}


void loop() {
  EthernetClient client = server.available();
  handleRoot(client);  
  // check if some timeout has been reached
  pmChecking();

  // watchdog reset
  wdt_reset();
}
