// dummy file 
// This file is just there for the arduino precompiler 
// He file concatenate all this ino files togheter using this one as the first, because it is the same name as the folder

/**
template <typename T>
Print& operator<<(Print& printer, T value)
{
    printer.print(value);
    return printer;
}
**/

namespace md
{
void debug(const String&  msg)
{
  //Serial << "debug: " <<  msg << '\n';
}

void trace(const String&  func, String msg)
{
  //Serial << "trace: "<< func << ": " << msg << '\n';
  Serial.print("trace: " + func);
  Serial.println(msg);
}

void info(const String&  msg)
{
  //Serial << "info: " <<  msg << '\n';
  Serial.print("info: ");
  Serial.println(msg);
}

void warning(const String& msg)
{
  //Serial << "warning: " << msg << '\n';
  Serial.print("warning: ");
  Serial.println(msg);
}

void error(const String&  msg)
{
  //Serial << "error: " << msg << '\n';
  Serial.print("error: ");
  Serial.println(msg);
}
}

