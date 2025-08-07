#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connecté au broker MQTT")
        # S'abonner à tous les topics des capteurs
        topics = [
            "sensors/ruuvitag/+/+",
            "sensor/+/data",
            "gw-event/received_data",
            "wirepas-json-event/packet/+/+/+"
        ]
        for topic in topics:
            client.subscribe(topic)
            print(f"📡 Abonné au topic: {topic}")
    else:
        print(f"❌ Échec de connexion. Code: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = msg.payload.decode('utf-8')
        
        # Essayer de parser en JSON si possible
        try:
            data = json.loads(payload)
            if isinstance(data, dict) and 'temperature' in data:
                print(f"🌡️  {topic}: T={data.get('temperature')}°C, H={data.get('humidity')}%, P={data.get('pressure')}hPa")
            else:
                print(f"📊 {topic}: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print(f"📝 {topic}: {payload}")
            
    except Exception as e:
        print(f"❌ Erreur traitement message: {e}")

def main():
    print("🔍 Test de connexion MQTT - Écoute des capteurs")
    print("=" * 50)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        print("🔌 Connexion au broker localhost:1883...")
        client.connect("localhost", 1883, 60)
        client.loop_start()
        
        print("👂 Écoute des messages MQTT... (Ctrl+C pour arrêter)")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du test...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("👋 Connexion fermée")

if __name__ == "__main__":
    main()