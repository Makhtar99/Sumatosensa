#!/usr/bin/env python3
import asyncio
import logging
from datetime import datetime
from app.database import AsyncSessionLocal
from app.models import Sensor, Measurement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_test_data():
    """Crée des données de test directement en base"""
    async with AsyncSessionLocal() as session:
        try:
            # Vérifier s'il y a déjà des mesures
            from sqlalchemy import select
            result = await session.execute(select(Measurement).limit(1))
            existing_measurement = result.scalar_one_or_none()
            
            if existing_measurement:
                logger.info("Des mesures existent déjà, pas besoin de créer des données de test")
                return
            
            # Récupérer tous les capteurs
            result = await session.execute(select(Sensor))
            sensors = result.scalars().all()
            
            if not sensors:
                logger.error("Aucun capteur trouvé, impossible de créer des mesures")
                return
            
            # Créer une mesure de test pour chaque capteur
            for i, sensor in enumerate(sensors):
                measurement = Measurement(
                    time=datetime.utcnow(),
                    sensor_id=sensor.id,
                    temperature=20.0 + i * 2.5,
                    humidity=40.0 + i * 5.0,
                    pressure=1010.0 + i * 3.0,
                    battery_voltage=2.9 + i * 0.05,
                    rssi=-60 - i * 5
                )
                
                session.add(measurement)
                logger.info(f"Mesure de test créée pour le capteur {sensor.id}: T={measurement.temperature}°C")
            
            await session.commit()
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des données de test: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(create_test_data())