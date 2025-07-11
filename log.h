#ifndef LOG_H
#define LOG_H

#include <Arduino.h>

namespace mylog
{
    
    void debug(const String& msg);
    void trace(const String& func, const String& msg);
    void info(const String& msg);
    void warning(const String& msg);
    void error(const String& msg);

    // always print, no log level filtering, usefull for message to user
    void print(const String& msg);
} // namespace mylog


#endif // LOG_H
