// Libraries
#include <SPI.h>
#include <Ethernet.h>
#include <aREST.h>
#include <avr/wdt.h>




// Enter a MAC address for your controller below.
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0E, 0xFE, 0x40 };

// IP address in case DHCP fails
IPAddress ip(192, 168, 2, 2);

// Ethernet server
EthernetServer server(80);

// Create aREST instance
aREST rest = aREST();





// Variables to be exposed to the API
unsigned long  counter;
const int pmSize = 8;
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
  trace(__func__, command);

  int splitPos = command.indexOf("-");
  if (splitPos < 0) {
    error("invalid parameter: " + command);
    return -1;
  }

  String strPompeIdx = command.substring(0, splitPos);
  int pompeIdx = strPompeIdx.toInt();
  String strTime = command.substring(splitPos + 1, command.length());
  unsigned long time = strTime.toInt();  // command is time in millisec, important not tu use int because of the buffer overflow

  if (pompeIdx >= pmSize) {
    error("out of bound index: " + pompeIdx);
    return -2;
  }

  info("set pompe: " + pompeIdx);
  pm[pompeIdx].setStateFor(HIGH, time);
  return 0;
}




void setup(void) {

  // Start Serial
  Serial.begin(115200);
  Serial.println("Setup ...");

  // setup rest api
  rest.set_id("001");
  rest.set_name("poulpette");

  for (int i = 0; i < pmSize; i++) {
    pm[i] = Pompe(i);
  }

  // Init variables and expose them to REST API
  counter = 0;
  rest.variable("counter", &counter);
  // Function to be exposed
  rest.function("pompes", pmPrint);
  rest.function("setpompe", setPompe);

  // Give name & ID to the device (ID should be 6 characters long)

  Ethernet.begin(mac, ip);

  // Start the Ethernet connection and the server
  //if (Ethernet.begin(mac) == 0) {
  //Serial.println("Failed to configure Ethernet using DHCP");
  // no point in carrying on, so do nothing forevermore:
  // try to congifure using IP address instead of DHCP:
  //Ethernet.begin(mac, ip);
  // }

  server.begin();
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());

  // Start watchdog
  wdt_enable(WDTO_4S);
}




void loop() {

  // using ethernet
  EthernetClient client = server.available();
  rest.handle(client);

  // or using serial interface
  rest.handle(Serial);

  // check is some timeout has been riched
  pmChecking();

  counter = counter + 1;
  wdt_reset();
}
