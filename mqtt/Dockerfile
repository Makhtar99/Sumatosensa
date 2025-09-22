FROM eclipse-mosquitto:2.0

RUN apk add --no-cache netcat-openbsd

COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY health_check.sh /health_check.sh

RUN mkdir -p /mosquitto/data /mosquitto/log
RUN chown -R mosquitto:mosquitto /mosquitto
RUN chmod +x /health_check.sh

EXPOSE 80 1883 9001

CMD ["/health_check.sh"]