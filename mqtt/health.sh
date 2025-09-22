#!/bin/sh
# Simple HTTP health check on port 80
while true; do
    echo -e "HTTP/1.1 200 OK\r\n\r\nMQTT OK" | nc -l -p 80 -q 1
done