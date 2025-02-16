#ifndef API_H
#define API_H

#include <Arduino.h>
#include <Ethernet.h>

void handleRoot(EthernetClient& client);

void okResponse(EthernetClient& client);
void failResponse(EthernetClient& client);

#endif // API_H
