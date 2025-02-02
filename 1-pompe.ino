// include in alphabetical order
#include <List.hpp>

class Pompe {

public:
  int pin = 0;

  String name = "undef";

  int state = 0;
  int defaultState = 0;

  unsigned long currentTime = 0;
  unsigned long startTime = 0;
  unsigned long endTime = 0;

  Pompe()
  {
  }

  Pompe(int newPin)
  {
    setup(newPin);
  }

  void setup(int newPin) {
    pin = newPin;
    pinMode(pin, OUTPUT);
  }

  void print() {
    Serial << "pompe: " << pin << ", state: " << state << '\n';
  }

  void setStateFor(int newState, unsigned long time) {
    state = newState;
    Serial << "pompe " << pin << ", set state to: " << state << '\n';
    startTime = millis();
    currentTime = millis();
    endTime = startTime + time;
    digitalWrite(pin, state);
    Serial << "pompe " << pin << ", set state to: " << state << " until :" << endTime << " current time: " << currentTime << '\n';
  }

  void checkTiming() {
   
    currentTime = millis();
    //Serial << "pompe" << pin << ", state: " << state << " until :" << endTime << " current time: " << currentTime << '\n';
    if (state != defaultState && currentTime >= endTime) {
      Serial << "pompe" << pin << ", timeout -> set state to: " << defaultState << '\n';
      digitalWrite(pin, defaultState);
      state = defaultState;
    }
  }
};

