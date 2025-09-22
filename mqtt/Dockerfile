FROM eclipse-mosquitto:2.0

RUN apk add --no-cache netcat-openbsd

COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY health.sh /health.sh

RUN mkdir -p /mosquitto/data /mosquitto/log
RUN chown -R mosquitto:mosquitto /mosquitto
RUN chmod +x /health.sh

EXPOSE 80 1883

CMD sh -c '/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf -v & /health.sh'