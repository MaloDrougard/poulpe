#include "Pompe.h"

Pompe::Pompe() : pin(-1), state(LOW), duration(0), startTime(0) {}

void Pompe::mysetup(int pin) {
    this->pin = pin;
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
}

void Pompe::setStateFor(int state, unsigned long duration) {
    this->state = state;
    this->duration = duration;
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
