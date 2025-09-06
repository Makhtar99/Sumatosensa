import asyncio
import json
import logging
from datetime import datetime
from typing import Optional
import paho.mqtt.client as mqtt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models import Sensor, Measurement
import os

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        self.broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
        self.broker_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))
        
        self.hetic_broker_host = os.getenv("HETIC_MQTT_HOST", "admin-hetic.arcplex.tech")
        self.hetic_broker_port = int(os.getenv("HETIC_MQTT_PORT", "8818"))  # Groupe 1
        
        self.connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info(f"Connected to MQTT broker: {self.broker_host}:{self.broker_port}")
            
            topics = [
                # Topics RuuviTag existants
                "sensors/ruuvitag/+/temperature",
                "sensors/ruuvitag/+/humidity", 
                "sensors/ruuvitag/+/pressure",
                "sensors/ruuvitag/+/battery",
                "sensors/ruuvitag/+/acceleration",
                "sensors/ruuvitag/+/data",
                
                # Topics Hetic existants
                "gw-req/get_configs/res",
                "gw-event/received_data",
                "sensor/+/data",
                
                # Topics PWS-Packet - Format corrigé selon MQTT Explorer
                "pws-packet/+/+/+",  # pws-packet/timestamp/sink_id/sensor_id
                
                # Topics Wirepas (gardé pour compatibilité)
                "wirepas-json-event/packet/+/+/+"
            ]
            
            for topic in topics:
                client.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
            self.connected = False

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.warning(f"Disconnected from MQTT broker. Return code: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            # LOG DÉTAILLÉ pour débugger
            logger.info(f"=== MQTT MESSAGE RECEIVED ===")
            logger.info(f"Topic: {topic}")
            logger.info(f"Payload length: {len(payload)}")
            logger.info(f"Payload: '{payload}'")
            logger.info(f"Payload (repr): {repr(payload)}")
            
            import threading
            def run_async():
                asyncio.run(self.process_message(topic, payload))
            
            thread = threading.Thread(target=run_async)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    async def process_message(self, topic: str, payload: str):
        try:
            topic_parts = topic.split('/')
            
            # Traitement RuuviTag existant
            if len(topic_parts) >= 3 and topic_parts[0] == "sensors":
                sensor_type = topic_parts[1]  # ruuvitag
                sensor_id = topic_parts[2]    # MAC address or sensor ID
                measurement_type = topic_parts[3] if len(topic_parts) > 3 else "data"
                
                await self.handle_ruuvitag_data(sensor_id, measurement_type, payload)
                
            # Traitement Hetic existant
            elif topic.startswith("gw-event/received_data"):
                await self.handle_hetic_gateway_data(payload)
                
            elif topic.startswith("sensor/"):
                sensor_id = topic_parts[1]
                await self.handle_sensor_data(sensor_id, payload)
                
            # NOUVEAU: Traitement PWS-PACKET
            elif topic.startswith("pws-packet/"):
                if len(topic_parts) >= 4:
                    timestamp = topic_parts[1]      # 20241587021839
                    sink_id = topic_parts[2]        # 1154767363
                    sensor_id = topic_parts[3]      # 192, 116, etc.
                    await self.handle_pws_packet_data(timestamp, sink_id, sensor_id, payload)
                
            # Traitement Wirepas existant
            elif topic.startswith("wirepas-json-event/packet/"):
                if len(topic_parts) >= 5:
                    network_id = topic_parts[2]
                    source_address = topic_parts[3]
                    destination_endpoint = topic_parts[4]
                    await self.handle_wirepas_data(network_id, source_address, destination_endpoint, payload)
                
        except Exception as e:
            logger.error(f"Error processing message from topic {topic}: {e}")

    async def handle_ruuvitag_data(self, sensor_id: str, measurement_type: str, payload: str):
        try:
            async with AsyncSessionLocal() as session:
                sensor = await self.get_or_create_sensor(session, sensor_id)
                
                if measurement_type == "data":
                    data = json.loads(payload)
                    await self.store_measurement(
                        session, 
                        sensor.id, 
                        data.get("temperature"),
                        data.get("humidity"),
                        data.get("pressure"),
                        data.get("acceleration_x"),
                        data.get("acceleration_y"), 
                        data.get("acceleration_z"),
                        data.get("rssi"),
                        data.get("battery_voltage"),
                        data.get("movement_counter")
                    )
                else:
                    value = float(payload)
                    await self.store_partial_measurement(session, sensor.id, measurement_type, value)
                    
        except Exception as e:
            logger.error(f"Error handling RuuviTag data: {e}")

    async def handle_hetic_gateway_data(self, payload: str):
        try:
            data = json.loads(payload)
            
            source_endpoint = data.get("source_endpoint", "unknown")
            sensor_data = data.get("data", {})
            
            async with AsyncSessionLocal() as session:
                sensor_id = f"hetic_{source_endpoint}"
                sensor = await self.get_or_create_sensor(session, sensor_id)
                
                await self.store_measurement(
                    session,
                    sensor.id,
                    sensor_data.get("temperature"),
                    sensor_data.get("humidity"),
                    sensor_data.get("pressure"),
                    rssi=data.get("rx_time_ms_epoch")
                )
                
        except Exception as e:
            logger.error(f"Error handling Hetic gateway data: {e}")

    async def handle_sensor_data(self, sensor_id: str, payload: str):
        try:
            data = json.loads(payload)
            
            async with AsyncSessionLocal() as session:
                sensor = await self.get_or_create_sensor(session, sensor_id)
                
                await self.store_measurement(
                    session,
                    sensor.id,
                    data.get("temperature"),
                    data.get("humidity"), 
                    data.get("pressure"),
                    data.get("acceleration_x"),
                    data.get("acceleration_y"),
                    data.get("acceleration_z"),
                    data.get("rssi"),
                    data.get("battery_voltage"),
                    data.get("movement_counter")
                )
                
        except Exception as e:
            logger.error(f"Error handling sensor data: {e}")

    # NOUVELLE MÉTHODE pour traiter pws-packet
    async def handle_pws_packet_data(self, timestamp: str, sink_id: str, sensor_id: str, payload: str):
        try:
            logger.info(f"Processing pws-packet: timestamp={timestamp}, sink_id={sink_id}, sensor_id={sensor_id}")
            logger.info(f"Raw payload: '{payload}' (length: {len(payload)})")
            
            # Vérifier si le payload est vide
            if not payload or payload.strip() == "":
                logger.warning(f"Empty payload for pws-packet sensor {sensor_id}")
                return
                
            async with AsyncSessionLocal() as session:
                # Création de l'ID unique du capteur
                full_sensor_id = f"pws_{sensor_id}"
                sensor = await self.get_or_create_sensor(session, full_sensor_id)
                
                try:
                    # Tentative de parsing JSON
                    data = json.loads(payload)
                    logger.info(f"JSON parsed successfully: {data}")
                    
                    # Extraction des données selon différentes structures possibles
                    sensor_data = data
                    
                    # Structure 1: Données directes au niveau racine
                    if isinstance(data, dict):
                        if "temperature" in data or "humidity" in data or "pressure" in data:
                            sensor_data = data
                            logger.info("Using direct data structure")
                        # Structure 2: Données dans une sous-structure 'data'
                        elif "data" in data and isinstance(data["data"], dict):
                            sensor_data = data["data"]
                            logger.info("Using nested 'data' structure")
                        # Structure 3: Données dans 'payload' ou autre clé
                        elif "payload" in data:
                            sensor_data = data["payload"]
                            logger.info("Using 'payload' structure")
                        # Structure 4: Structure PWS spécifique
                        elif "sink_id" in data:
                            # Extraire les données de capteur depuis la structure PWS
                            sensor_data = {
                                "temperature": data.get("temperature"),
                                "humidity": data.get("humidity"), 
                                "pressure": data.get("pressure"),
                                "battery_voltage": data.get("battery_voltage"),
                                "rssi": data.get("rssi")
                            }
                            logger.info("Using PWS-specific structure")
                        else:
                            sensor_data = data
                            logger.info("Using fallback data structure")
                    
                    # Stockage des données
                    await self.store_measurement(
                        session, 
                        sensor.id, 
                        sensor_data.get("temperature"),
                        sensor_data.get("humidity"),
                        sensor_data.get("pressure"),
                        sensor_data.get("acceleration_x"),
                        sensor_data.get("acceleration_y"), 
                        sensor_data.get("acceleration_z"),
                        sensor_data.get("rssi"),
                        sensor_data.get("battery_voltage"),
                        sensor_data.get("movement_counter")
                    )
                    
                    logger.info(f"Successfully stored pws-packet data for sensor {full_sensor_id}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in pws-packet payload: '{payload}' - Error: {e}")
                    
                    # Tentative de traitement comme données brutes
                    logger.info("Attempting to handle as raw sensor data")
                    
                    # Si le payload contient des données formatées autrement
                    try:
                        # Exemple: "temp:23.5,hum:65.2,press:1013.25"
                        if ":" in payload and "," in payload:
                            raw_data = {}
                            pairs = payload.split(",")
                            for pair in pairs:
                                if ":" in pair:
                                    key, value = pair.split(":", 1)
                                    key = key.strip().lower()
                                    try:
                                        if key in ["temp", "temperature"]:
                                            raw_data["temperature"] = float(value)
                                        elif key in ["hum", "humidity"]:
                                            raw_data["humidity"] = float(value)
                                        elif key in ["press", "pressure"]:
                                            raw_data["pressure"] = float(value)
                                    except ValueError:
                                        continue
                                        
                            if raw_data:
                                await self.store_measurement(
                                    session, sensor.id, 
                                    raw_data.get("temperature"),
                                    raw_data.get("humidity"),
                                    raw_data.get("pressure")
                                )
                                logger.info(f"Stored raw formatted data: {raw_data}")
                            
                    except Exception as raw_e:
                        logger.error(f"Failed to parse raw data: {raw_e}")
                
        except Exception as e:
            logger.error(f"Error handling pws-packet data: {e}")

    async def handle_wirepas_data(self, network_id: str, source_address: str, destination_endpoint: str, payload: str):
        try:
            data = json.loads(payload)
            sensor_data = data.get("data", {})
            
            if not sensor_data or "trace_options" in sensor_data:
                return
            
            async with AsyncSessionLocal() as session:
                sensor_id = f"wirepas_{source_address}"
                sensor = await self.get_or_create_sensor(session, sensor_id)
                
                await self.store_measurement(
                    session,
                    sensor.id,
                    sensor_data.get("temperature"),
                    sensor_data.get("humidity"),
                    sensor_data.get("pressure"),
                    sensor_data.get("acceleration_x"),
                    sensor_data.get("acceleration_y"),
                    sensor_data.get("acceleration_z"),
                    rssi=data.get("rssi"),
                    battery_voltage=sensor_data.get("battery_voltage"),
                    movement_counter=sensor_data.get("movement_counter")
                )
                
        except Exception as e:
            logger.error(f"Error handling Wirepas data: {e}")

    async def get_or_create_sensor(self, session: AsyncSession, source_address: str) -> Sensor:
        from sqlalchemy import select
        
        result = await session.execute(
            select(Sensor).where(Sensor.source_address == source_address)
        )
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            # Nommage approprié selon le type de capteur
            if source_address.startswith("pws_"):
                name = f"PWS Sensor {source_address.replace('pws_', '')}"
            elif source_address.startswith("wirepas_"):
                name = f"Wirepas {source_address.replace('wirepas_', '')}"
            elif source_address.startswith("hetic_"):
                name = f"Hetic {source_address.replace('hetic_', '')}"
            else:
                name = f"RuuviTag {source_address}"
                
            sensor = Sensor(
                source_address=source_address,
                name=name,
                is_active=True
            )
            session.add(sensor)
            await session.commit()
            await session.refresh(sensor)
            logger.info(f"Created new sensor: {source_address} with name: {name}")
            
        return sensor

    async def store_measurement(
        self, 
        session: AsyncSession, 
        sensor_id: int,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None,
        pressure: Optional[float] = None,
        acceleration_x: Optional[float] = None,
        acceleration_y: Optional[float] = None,
        acceleration_z: Optional[float] = None,
        rssi: Optional[int] = None,
        battery_voltage: Optional[float] = None,
        movement_counter: Optional[int] = None
    ):
        try:
            # Vérifier qu'au moins une valeur valide est présente
            if not any([temperature, humidity, pressure, acceleration_x, acceleration_y, acceleration_z, battery_voltage]):
                logger.debug(f"No valid sensor data to store for sensor {sensor_id}")
                return
                
            measurement = Measurement(
                time=datetime.utcnow(),
                sensor_id=sensor_id,
                temperature=temperature,
                humidity=humidity,
                pressure=pressure,
                acceleration_x=acceleration_x,
                acceleration_y=acceleration_y,
                acceleration_z=acceleration_z,
                rssi=rssi,
                battery_voltage=battery_voltage,
                movement_counter=movement_counter
            )
            
            session.add(measurement)
            await session.commit()
            logger.info(f"Stored measurement for sensor {sensor_id}: T={temperature}°C, H={humidity}%, P={pressure}hPa")
            
        except Exception as e:
            logger.error(f"Error storing measurement: {e}")
            await session.rollback()

    async def store_partial_measurement(self, session: AsyncSession, sensor_id: int, measurement_type: str, value: float):
        logger.debug(f"Received partial measurement: {measurement_type}={value} for sensor {sensor_id}")

    async def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            logger.info(f"MQTT client started for {self.broker_host}:{self.broker_port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    async def disconnect(self):
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT client disconnected")
    
    async def request_refresh(self):
        try:
            topic = "wirepas/request/sensor-data"
            message = json.dumps({"action": "refresh_all"})
            self.client.publish(topic, message)
            logger.info(f"Sent refresh request to MQTT topic {topic}")
        except Exception as e:
            logger.error(f"Failed to publish refresh request: {e}")

mqtt_client = MQTTClient()

async def start_mqtt_client():
    await mqtt_client.connect()

async def stop_mqtt_client():
    await mqtt_client.disconnect()