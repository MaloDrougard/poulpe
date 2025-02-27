#include "Stepper.h"
#include "Log.h"

using namespace mylog;


void setupStepper() {
    info("Stepper setup");
    // Set the two pins as Outputs
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    // Set the spinning direction clockwise:
    digitalWrite(dirPin, HIGH);
    stepToPerform = 0;
  }


void rotation(double rotation) {
    // Calculate the number of steps for the stepper motor
    stepToPerform = (int) (stepsPerRevolution * rotation);
    info("Rotation: " + String(rotation) + ", new steps: " + String(stepToPerform));
}

void performOneStep() {
    if (stepToPerform > 0) {
        onestepClockwise();
        stepToPerform--;
    } else if (stepToPerform < 0) {
        onestepAntiClockwise();
        stepToPerform++;
    }
}

void onestepClockwise() {

    // Set the spinning direction clockwise:
    digitalWrite(dirPin, HIGH);
    
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepSpeed);
    delayMicroseconds(delayAfterSetp); // to slow down the rotation    
}

void onestepAntiClockwise() {

    // Set the spinning direction counterclockwise:
    digitalWrite(dirPin, LOW);
  
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepSpeed);
    delayMicroseconds(delayAfterSetp); // to slow down the rotation    
}
