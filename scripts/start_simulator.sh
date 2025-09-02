#!/bin/bash

echo "🚀 Démarrage du simulateur de capteurs RuuviTag"
echo "================================================"

# Vérification que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements_simulator.txt

echo ""
echo "🔧 Vérification de la configuration Docker..."

# Vérification que Docker est démarré
if ! docker info &> /dev/null; then
    echo "❌ Docker n'est pas démarré. Veuillez démarrer Docker Desktop."
    exit 1
fi

# Vérification/démarrage du broker MQTT
if ! docker ps | grep -q mosquitto; then
    echo "🦟 Démarrage du broker Mosquitto..."
    docker-compose up -d mqtt
    sleep 3
else
    echo "✅ Broker Mosquitto déjà en cours d'exécution"
fi

echo ""
echo "🎯 Démarrage du simulateur..."
echo "   Capteurs simulés:"
echo "   - 📍 Chambre parentale (C4:64:E3:4A:5B:1C)"
echo "   - 📍 Salon (D1:A2:B3:C4:D5:E6)" 
echo "   - 📍 Grenier (F7:8E:9F:1A:2B:3C)"
echo ""
echo "💡 Appuyez sur Ctrl+C pour arrêter le simulateur"
echo "================================================"

# Démarrage du simulateur
python3 mqtt_simulator.py