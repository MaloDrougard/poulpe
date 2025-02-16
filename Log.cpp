#ifndef LOG_H
#define LOG_H

#include <Arduino.h>

namespace mylog
{
    
    void debug(const String& msg) {
        // Serial << "debug: " << msg << '\n';
    }

    void trace(const String& func, const String& msg) {
        // Serial << "trace: " << func << ": " << msg << '\n';
        Serial.print("trace: " + func);
        Serial.println(msg);
    }

    void info(const String& msg) {
        // Serial << "info: " << msg << '\n';
        Serial.print("info: ");
        Serial.println(msg);
    }

    void warning(const String& msg) {
        // Serial << "warning: " << msg << '\n';
        Serial.print("warning: ");
        Serial.println(msg);
    }

    void error(const String& msg) {
        // Serial << "error: " << msg << '\n';
        Serial.print("error: ");
        Serial.println(msg);
    }
} // namespace mylog


#endif // LOG_H
