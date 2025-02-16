#include "Api.h"
#include "Log.h"

using namespace mylog;

void handleRoot(EthernetClient& client) {
    if (client) {
        String request = client.readStringUntil('\r');
        info(request);
        if (request.indexOf("GET / ") >= 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/html");
            client.println("Connection: close");
            client.println();
            client.println("hello there!)");
            //client.println(htmlPage);
        } else if (request.indexOf("GET /status") >= 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: application/json");
            client.println("Connection: close");
            client.println();
            client.println("{\"status\":\"ok\"}");
        } else if (request.indexOf("GET /setpompe") >= 0) {
            int pIndex = request.indexOf("p=");
            int tIndex = request.indexOf("t=");
            if (pIndex >= 0 && tIndex >= 0) {
                int pValue = request.substring(pIndex + 2, request.indexOf('&', pIndex)).toInt();
                int tValue = request.substring(tIndex + 2, request.indexOf(' ', tIndex)).toInt();
                // Handle the setpompe logic here with pValue and tValue
                client.println("HTTP/1.1 200 OK");
                client.println("Content-Type: application/json");
                client.println("Connection: close");
                client.println("Access-Control-Allow-Origin: *");
                client.println();
                client.println("{\"status\":\"ok\",\"p\":" + String(pValue) + ",\"t\":" + String(tValue) + "}");
            } else {
                client.println("HTTP/1.1 400 Bad Request");
                client.println("Content-Type: text/plain");
                client.println("Connection: close");
                client.println();
                client.println("400 Bad Request");
            }
        } else {
            client.println("HTTP/1.1 404 Not Found");
            client.println("Content-Type: text/plain");
            client.println("Connection: close");
            client.println();
            client.println("404 Not Found");
        }
        client.stop();
    }
}
