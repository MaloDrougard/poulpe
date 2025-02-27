
#ifndef STEPPER_H
#define STEPPER_H


// Define stepper motor connections and steps per revolution:
#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 200.0
#define stepSpeed 1000 // in microseconds
#define delayAfterSetp 10000 // in milliseconds


void setupStepper();
void rotation(double rotation); // 1 rotation = 360 degrees = 200 steps, -1 rotation = -360 degrees = -200 steps
void performOneStep();

void onestepClockwise();
void onestepAntiClockwise();


static int stepToPerform; // number of steps to perform, if = 0 then no rotation

#endif // STEPPER_H