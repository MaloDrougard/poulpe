#ifndef API_H
#define API_H

#include <Arduino.h>

void handleCommand(const String& command);

void okResponse();
void failResponse();

#endif // API_H
