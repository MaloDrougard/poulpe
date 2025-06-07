#include "Api.h"
#include "Log.h"
#include "Pompe.h"
#include "Stepper.h"

using namespace mylog;

void okResponse()
{
    print("{\"status\":\"ok\"}");
}

void failResponse(const String &errorMessage = "Undefined")
{
    print("{\"status\":\"fail\",\"message\":\"");
    print(errorMessage);
    print("\"}");
}

void handleCommand(const String &command)
{

    if (command == "")
    {
        failResponse("Command is null");
        return;
    }
    if (command.indexOf("/setpompe") >= 0)
    {
        int pIndex = command.indexOf("p=");
        int tIndex = command.indexOf("t=");
        if (pIndex >= 0 && tIndex >= 0)
        {
            int pValue = command.substring(pIndex + 2, command.indexOf('&', pIndex)).toInt();
            float tValue = command.substring(tIndex + 2, command.indexOf(' ', tIndex)).toFloat();
            if (pValue >= 0 && pValue < pmSize)
            {
                pm[pValue].setStateFor(HIGH, tValue);
                okResponse();
            }
            else
            {
                failResponse("Invalid pump index");
            }
        }
        else
        {
            failResponse("Error parsing parameters");
        }
    }
    else if (command.indexOf("/stepper") >= 0)
    {
        int rIndex = command.indexOf("r=");
        int resetIndex = command.indexOf("reset");
        if (rIndex >= 0)
        {
            double rValue = command.substring(rIndex + 2, command.indexOf(' ', rIndex)).toDouble();
            rotation(rValue);
            okResponse();
        }
        else if (resetIndex >= 0)
        {
            resetInitalPosition();
            okResponse();
        }
        else
        {
            failResponse("Error parsing parameters");
        }
    }
    else if (command.indexOf("/info") >= 0)
    {
        pmInfo();
        okResponse();
    }   
    else
    {
        failResponse("Unknown command");
    }
}
