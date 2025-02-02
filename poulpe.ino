// dummy file 
// This file is just there for the arduino precompiler 
// He file concatenate all this ino files togheter using this one as the first, because it is the same name as the folder

template <typename T>
Print& operator<<(Print& printer, T value)
{
    printer.print(value);
    return printer;
}

void debug(String msg)
{
  //Serial << "debug: " <<  msg << '\n';
}

void trace(String func, String msg)
{
  Serial << "trace: "<< func << ": " << msg << '\n';
}

void info(String msg)
{
  Serial << "info: " <<  msg << '\n';
}

void error(String msg)
{
  Serial << "error: " << msg << '\n';
}