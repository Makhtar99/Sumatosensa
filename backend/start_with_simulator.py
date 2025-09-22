#!/usr/bin/env python3
import asyncio
import uvicorn
from app.main import app
from app.mqtt_client import start_mqtt_client
import json
import random
import logging
import os
from datetime import datetime
from typing import Dict
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class RuuviTagSimulator:
    def __init__(self, mac_address: str, location: str):
        self.mac_address = mac_address
        self.location = location
        self.base_temperature = random.uniform(20.0, 24.0)
        self.base_humidity = random.uniform(40.0, 60.0)
        self.base_pressure = random.uniform(1000.0, 1020.0)
        self.battery_voltage = random.uniform(2.8, 3.0)
        self.movement_counter = 0
        
    def generate_realistic_data(self) -> Dict:
        current_hour = datetime.now().hour
        
        
        temp_variation = 2 * (current_hour - 12) / 12 if current_hour > 12 else -2 * (12 - current_hour) / 12
        temperature = self.base_temperature + temp_variation + random.uniform(-1.0, 1.0)
        
        humidity = max(30.0, min(70.0, self.base_humidity - temp_variation + random.uniform(-5.0, 5.0)))
        
        pressure = self.base_pressure + random.uniform(-2.0, 2.0)
        
        movement_detected = random.random() < 0.1
        if movement_detected:
            self.movement_counter += 1
            acceleration_x = random.uniform(-2.0, 2.0)
            acceleration_y = random.uniform(-2.0, 2.0)
            acceleration_z = random.uniform(0.8, 1.2)
        else:
            acceleration_x = random.uniform(-0.1, 0.1)
            acceleration_y = random.uniform(-0.1, 0.1)
            acceleration_z = random.uniform(0.95, 1.05)
        
        rssi = random.randint(-80, -40)
        
        self.battery_voltage = max(2.5, self.battery_voltage - 0.001 * random.random())
        
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "pressure": round(pressure, 2),
            "acceleration_x": round(acceleration_x, 3),
            "acceleration_y": round(acceleration_y, 3),
            "acceleration_z": round(acceleration_z, 3),
            "rssi": rssi,
            "battery_voltage": round(self.battery_voltage, 3),
            "movement_counter": self.movement_counter,
            "timestamp": datetime.utcnow().isoformat(),
            "mac_address": self.mac_address,
            "location": self.location
        }

class EmbeddedMQTTSimulator:
    def __init__(self, broker_host="localhost", broker_port=1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        
        self.sensors = [
            RuuviTagSimulator("C4:64:E3:4A:5B:1C", "Salle de réunion"),
            RuuviTagSimulator("D1:A2:B3:C4:D5:E6", "Open Space"),
            RuuviTagSimulator("F7:8E:9F:1A:2B:3C", "Bureau individuel")
        ]
        
        self.running = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info(f"Simulateur MQTT connecté au broker {self.broker_host}:{self.broker_port}")
        else:
            logger.error(f"Échec de connexion au broker MQTT. Code: {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.warning(f"Simulateur MQTT déconnecté. Code: {rc}")
        
    async def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            
            timeout = 10
            while not self.connected and timeout > 0:
                await asyncio.sleep(0.5)
                timeout -= 0.5
                
            if not self.connected:
                logger.warning("Timeout de connexion au broker MQTT pour le simulateur")
                return False
                
            logger.info("Simulateur MQTT démarré avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur de connexion au broker MQTT: {e}")
            return False
            
    async def disconnect(self):
        self.running = False
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Simulateur MQTT arrêté")
            
    def publish_sensor_data(self, sensor: RuuviTagSimulator, data: Dict):
        if not self.connected:
            return
            
        mac = sensor.mac_address
        
        try:
            self.client.publish(f"sensors/ruuvitag/{mac}/data", json.dumps(data))
            self.client.publish(f"sensors/ruuvitag/{mac}/temperature", str(data["temperature"]))
            self.client.publish(f"sensors/ruuvitag/{mac}/humidity", str(data["humidity"]))
            self.client.publish(f"sensors/ruuvitag/{mac}/pressure", str(data["pressure"]))
            self.client.publish(f"sensors/ruuvitag/{mac}/battery", str(data["battery_voltage"]))
            self.client.publish(f"sensor/{mac}/data", json.dumps(data))
        except Exception as e:
            logger.error(f"Erreur lors de la publication des données: {e}")
        
    async def simulate_sensors(self, interval: int = 60):
        logger.info(f"Démarrage de la simulation avec {len(self.sensors)} capteurs (interval: {interval}s)")
        
        self.running = True
        while self.running:
            try:
                for sensor in self.sensors:
                    if not self.connected:
                        logger.warning("Connexion MQTT perdue, tentative de reconnexion...")
                        if not await self.connect():
                            break
                            
                    data = sensor.generate_realistic_data()
                    self.publish_sensor_data(sensor, data)
                    
                    logger.info(f"📊 Données simulées - {sensor.location}: "
                              f"T={data['temperature']}°C, H={data['humidity']}%, P={data['pressure']}hPa")
                    
                    await asyncio.sleep(2)
                    
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Erreur lors de la simulation: {e}")
                await asyncio.sleep(10)

simulator_instance = None

async def start_simulator():
    global simulator_instance
    broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
    broker_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    
    simulator_instance = EmbeddedMQTTSimulator(broker_host, broker_port)
    
    if await simulator_instance.connect():
        asyncio.create_task(simulator_instance.simulate_sensors(60))
        logger.info("Simulateur MQTT intégré démarré")
    else:
        logger.warning("Simulateur MQTT non démarré - connexion échouée")

async def stop_simulator():
    global simulator_instance
    if simulator_instance:
        await simulator_instance.disconnect()
        simulator_instance = None
        logger.info("Simulateur MQTT arrêté")

if __name__ == "__main__":
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    async def startup():
        await start_mqtt_client()
        await asyncio.sleep(5)
        await start_simulator()
    
    asyncio.create_task(startup())
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )