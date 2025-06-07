#include "Pompe.h"
#include "Log.h"

using namespace mylog;

const int pmSize = 5;
Pompe pm[pmSize];


Pompe::Pompe() : pin(-1), state(LOW), duration(0), startTime(0) {}

void Pompe::mysetup(int pin) {
    this->pin = pin;
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
}

void Pompe::setStateFor(int state, float duration) {
    this->state = state;
    this->duration = duration * 1000.0; // convert form second (float) to millis (long)
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
    String message = "{ \"pin\": " + String(pin) \
                      + ", \"state\":" + (state == HIGH ? "ON" : "OFF") \
                      + ", \"duration\":" +  String(duration/1000) \
                      +  ", \"remaining\": " + (state == HIGH ? String((duration - (millis() - startTime))/1000) : "0") + "}" ;
    mylog::print(message);
}



void setupPompes() {
   info("Setup pompes ...");
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
  
  
  int pmInfo() {
    for (int i = 0; i < pmSize; i++) {
      pm[i].print();
    }
    return 0;
  }
  
