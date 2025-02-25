#include "Pompe.h"
#include "Log.h"

using namespace mylog;

const int pmSize = 4;
Pompe pm[pmSize];


Pompe::Pompe() : pin(-1), state(LOW), duration(0), startTime(0) {}

void Pompe::mysetup(int pin) {
    this->pin = pin;
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
}

void Pompe::setStateFor(int state, unsigned long duration) {
    this->state = state;
    this->duration = duration * 1000;
    info("Setting pump " + String(pin) + " HIGH for duration " + String(duration) + "s");
    this->startTime = millis();
    digitalWrite(pin, state);
}

void Pompe::checkTiming() {
    if (state == HIGH && (millis() - startTime >= duration)) {
        digitalWrite(pin, LOW);
        state = LOW;
    }
}

void Pompe::print() {
    Serial.print("Pompe on pin ");
    Serial.print(pin);
    Serial.print(" is ");
    Serial.println(state == HIGH ? "ON" : "OFF");
}



void setupPompes() {
    pm[0].mysetup(5);
    pm[1].mysetup(6);
    pm[2].mysetup(7);
    pm[3].mysetup(8);
    pm[4].mysetup(9);
  }

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
    unsigned long time = (unsigned long)strTime.toInt();  // Convert String to unsigned int
  
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
