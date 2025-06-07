#ifndef POMPE_H
#define POMPE_H

#include <Arduino.h>

class Pompe {
public:
    Pompe();
    void mysetup(int pin);
    // duration in second
    void setStateFor(int state, float duration);
    void checkTiming();
    void print();

private:
    int pin;
    int state;
    unsigned long duration;
    unsigned long startTime;
};

// global variables and functions
extern const int pmSize;
extern Pompe pm[];

void setupPompes();
void pmChecking();
int pmPrint(String dummy);

#endif // POMPE_H
