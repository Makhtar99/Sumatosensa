#!/bin/sh
# Start Mosquitto in background
/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf -v &

# Wait for Mosquitto to start
sleep 5

# Start simple HTTP health check server on port 80
while true; do
    echo -e "HTTP/1.1 200 OK\r\n\r\nMQTT Service Running - Ports 1883 & 9001 active" | nc -l -p 80 -q 1
done