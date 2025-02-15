// include in alphabetical ordermd::warning

class Pompe {

public:
  int pin = 0;
  int state = 0;
  int defaultState = 0;

  unsigned long currentTime = 0;
  unsigned long startTime = 0;
  unsigned long endTime = 0;

  // having a string as member seems to be problematic ?!

  Pompe() {
    md::info("Create dummy pompe");
  }

  Pompe(int newPin) {
    mysetup(newPin);
  }

  void mysetup(int newPin) {
    if (newPin == 4 || newPin > 9) {
      md::warning("The pin assignment can enter in conflict with the ethernet shield!");
    }
    pin = newPin;
    pinMode(pin, OUTPUT);
  }

  void print() {
    char buffer[50];
    snprintf(buffer, sizeof(buffer), "pompe: pin %d, state: %d", pin, state);
    md::info(buffer);
  }

  void setStateFor(int newState, unsigned long time) {
    state = newState;
    startTime = millis();
    currentTime = millis();
    endTime = startTime + time;
    digitalWrite(pin, state);

    char buffer[100];
    snprintf(buffer, sizeof(buffer), "pompe %d, set state to: %d until: %lu current time: %lu", pin, state, endTime, currentTime);
    md::info(buffer);
  }

  void checkTiming() {
    currentTime = millis();
    if (state != defaultState && currentTime >= endTime) {
      digitalWrite(pin, defaultState);
      state = defaultState;

      char buffer[50];
      snprintf(buffer, sizeof(buffer), "pompe %d, state reset to default: %d", pin, defaultState);
      md::info(buffer);
    }
  }
};


