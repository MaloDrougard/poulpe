#ifndef POMPE_H
#define POMPE_H

#include <Arduino.h>

class Pompe {
public:
    Pompe();
    void mysetup(int pin);
    void setStateFor(int state, unsigned long duration);
    void checkTiming();
    void print();

private:
    int pin;
    int state;
    unsigned long duration;
    unsigned long startTime;
};

#endif // POMPE_H
