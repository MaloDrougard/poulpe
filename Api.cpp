#include "Api.h"
#include "Log.h"
#include "Pompe.h"
#include "Stepper.h"

using namespace mylog;

void okResponse(EthernetClient& client)
{
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println("Access-Control-Allow-Origin: *");
    client.println();
    client.println("{\"status\":\"ok\"}");
}

void failResponse(EthernetClient& client, const char* message = "Bad Request")
{
    client.println("HTTP/1.1 400 Bad Request");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println("Access-Control-Allow-Origin: *");
    client.println();
    client.print("{\"status\":\"fail\",\"message\":\"");
    client.print(message);
    client.println("\"}");
}


void    handleRoot(EthernetClient& client) {
    if (client) {
        String request = client.readStringUntil('\r');
        info(request);
        if (request.indexOf("GET / ") >= 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/html");
            client.println("Connection: close");
            client.println();
            client.println("Hello there!)");
            //client.println(htmlPage);
        }
        else if (request.indexOf("GET /setpompe") >= 0) {
            int pIndex = request.indexOf("p=");
            int tIndex = request.indexOf("t=");
            if (pIndex >= 0 && tIndex >= 0) {
                int pValue = request.substring(pIndex + 2, request.indexOf('&', pIndex)).toInt();
                long tValue = request.substring(tIndex + 2, request.indexOf(' ', tIndex)).toInt();
                if (pValue >= 0 && pValue < pmSize) {
                    pm[pValue].setStateFor(HIGH, tValue);
                    okResponse(client);
                } else {
                    failResponse(client, "Invalid pump index");
                }
             } else {
                failResponse(client, "Error parsing parameters");
            }
        } else if (request.indexOf("GET /stepper") >= 0) {
            int rIndex = request.indexOf("r=");
            int resetIndex = request.indexOf("reset");
            if (rIndex >= 0) {
                double rValue = request.substring(rIndex + 2, request.indexOf(' ', rIndex)).toDouble();
                rotation(rValue);
                okResponse(client);
            }
            else if (resetIndex >= 0) {
                resetInitalPosition();
                okResponse(client);
            }
            else {
                failResponse(client, "Error parsing parameters");
            }
        }else {
           failResponse(client, "Unknown request");
        }
        client.stop();
    }
}
