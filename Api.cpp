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
