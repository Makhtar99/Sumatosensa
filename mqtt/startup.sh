#!/bin/sh
# Start Mosquitto
/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf -v &

# Wait for Mosquitto to start
sleep 3

# Start nginx for health checks and WebSocket proxy
nginx -g 'daemon off;' &

# Keep container running
wait