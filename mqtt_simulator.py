import asyncio
import json
import random
import time
from datetime import datetime
from typing import List, Dict
import paho.mqtt.client as mqtt
import logging

logging.basicConfig(level=logging.INFO)
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
        
        # Simulation de variation journalière
        temp_variation = 2 * (current_hour - 12) / 12 if current_hour > 12 else -2 * (12 - current_hour) / 12
        temperature = self.base_temperature + temp_variation + random.uniform(-1.0, 1.0)
        
        # Humidité inversement proportionnelle à la température
        humidity = max(30.0, min(70.0, self.base_humidity - temp_variation + random.uniform(-5.0, 5.0)))
        
        # Pression avec légères variations
        pressure = self.base_pressure + random.uniform(-2.0, 2.0)
        
        # Accélération (mouvement aléatoire occasionnel)
        movement_detected = random.random() < 0.1
        if movement_detected:
            self.movement_counter += 1
            acceleration_x = random.uniform(-2.0, 2.0)
            acceleration_y = random.uniform(-2.0, 2.0)
            acceleration_z = random.uniform(0.8, 1.2)  # Gravitée
        else:
            acceleration_x = random.uniform(-0.1, 0.1)
            acceleration_y = random.uniform(-0.1, 0.1)
            acceleration_z = random.uniform(0.95, 1.05)
        
        # RSSI (force du signal)
        rssi = random.randint(-80, -40)
        
        # Batterie qui se décharge lentement
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

class MQTTSimulator:
    def __init__(self, broker_host="localhost", broker_port=1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        
        # Configuration des capteurs simulés
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
            
            # Attendre la connexion
            timeout = 10
            while not self.connected and timeout > 0:
                await asyncio.sleep(0.5)
                timeout -= 0.5
                
            if not self.connected:
                raise Exception("Timeout de connexion au broker MQTT")
                
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
        """Publie les données d'un capteur sur différents topics MQTT"""
        mac = sensor.mac_address
        
        # Topic principal avec toutes les données
        self.client.publish(f"sensors/ruuvitag/{mac}/data", json.dumps(data))
        
        # Topics spécifiques pour chaque métrique
        self.client.publish(f"sensors/ruuvitag/{mac}/temperature", str(data["temperature"]))
        self.client.publish(f"sensors/ruuvitag/{mac}/humidity", str(data["humidity"]))
        self.client.publish(f"sensors/ruuvitag/{mac}/pressure", str(data["pressure"]))
        self.client.publish(f"sensors/ruuvitag/{mac}/battery", str(data["battery_voltage"]))
        
        # Topic d'accélération combiné
        acceleration_data = {
            "x": data["acceleration_x"],
            "y": data["acceleration_y"],
            "z": data["acceleration_z"],
            "movement_counter": data["movement_counter"]
        }
        self.client.publish(f"sensors/ruuvitag/{mac}/acceleration", json.dumps(acceleration_data))
        
        # Topic générique pour les capteurs
        self.client.publish(f"sensor/{mac}/data", json.dumps(data))
        
    async def simulate_sensors(self, interval: int = 30):
        """Simule l'envoi de données des capteurs RuuviTag"""
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
                    
                    logger.info(f"📊 Données envoyées - {sensor.location} ({sensor.mac_address}): "
                              f"T={data['temperature']}°C, H={data['humidity']}%, P={data['pressure']}hPa")
                    
                    # Petit délai entre chaque capteur
                    await asyncio.sleep(1)
                    
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Erreur lors de la simulation: {e}")
                await asyncio.sleep(5)
                
    async def simulate_anomalies(self):
        """Simule des anomalies occasionnelles pour tester les alertes"""
        while self.running:
            try:
                # Une anomalie toutes les 5 minutes en moyenne
                await asyncio.sleep(random.randint(180, 600))
                
                if not self.running:
                    break
                    
                # Choisir un capteur aléatoire
                sensor = random.choice(self.sensors)
                
                # Type d'anomalie
                anomaly_type = random.choice(["temperature_high", "temperature_low", "humidity_high", "pressure_low"])
                
                anomaly_data = sensor.generate_realistic_data()
                
                if anomaly_type == "temperature_high":
                    anomaly_data["temperature"] = random.uniform(28.0, 35.0)
                elif anomaly_type == "temperature_low":
                    anomaly_data["temperature"] = random.uniform(10.0, 16.0)
                elif anomaly_type == "humidity_high":
                    anomaly_data["humidity"] = random.uniform(80.0, 95.0)
                elif anomaly_type == "pressure_low":
                    anomaly_data["pressure"] = random.uniform(980.0, 995.0)
                    
                self.publish_sensor_data(sensor, anomaly_data)
                
                logger.warning(f"🚨 ANOMALIE simulée - {sensor.location}: {anomaly_type} = "
                             f"{anomaly_data.get(anomaly_type.split('_')[0], 'N/A')}")
                
            except Exception as e:
                logger.error(f"Erreur lors de la simulation d'anomalies: {e}")
                await asyncio.sleep(30)

async def main():
    # Configuration
    BROKER_HOST = "localhost"
    BROKER_PORT = 1883
    SIMULATION_INTERVAL = 30  # secondes
    
    print("🚀 Démarrage du simulateur de capteurs RuuviTag")
    print(f"📡 Connexion au broker MQTT: {BROKER_HOST}:{BROKER_PORT}")
    print(f"⏱️  Intervalle de simulation: {SIMULATION_INTERVAL} secondes")
    print("=" * 60)
    
    simulator = MQTTSimulator(BROKER_HOST, BROKER_PORT)
    
    try:
        # Connexion au broker MQTT
        if not await simulator.connect():
            logger.error("Impossible de se connecter au broker MQTT")
            return
            
        # Lancement des tâches de simulation
        tasks = [
            asyncio.create_task(simulator.simulate_sensors(SIMULATION_INTERVAL)),
            asyncio.create_task(simulator.simulate_anomalies())
        ]
        
        print("✅ Simulateur démarré. Appuyez sur Ctrl+C pour arrêter.")
        print("📊 Surveillance des topics MQTT:")
        for sensor in simulator.sensors:
            print(f"   - sensors/ruuvitag/{sensor.mac_address}/*")
        print()
        
        # Attente infinie
        await asyncio.gather(*tasks)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du simulateur...")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
    finally:
        await simulator.disconnect()
        print("👋 Simulateur arrêté")

if __name__ == "__main__":
    asyncio.run(main())