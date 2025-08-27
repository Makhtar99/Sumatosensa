from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.database import get_db
from app.models import Sensor, Measurement, AlertThreshold
from app.auth import get_current_user
from app.schemas import SensorResponse, MeasurementResponse, SensorListResponse

router = APIRouter(prefix="/sensors", tags=["sensors"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[SensorResponse])
async def get_all_sensors(
    active_only: bool = Query(True, description="Filtrer uniquement les capteurs actifs"),
    session: AsyncSession = Depends(get_db)
):
    try:
        query = select(Sensor)
        if active_only:
            query = query.where(Sensor.is_active == True)
        
        result = await session.execute(query.order_by(Sensor.name))
        sensors = result.scalars().all()
        
        sensor_data = []
        for sensor in sensors:
            last_measurement_query = select(Measurement).where(
                Measurement.sensor_id == sensor.id
            ).order_by(desc(Measurement.time)).limit(1)
            
            last_measurement_result = await session.execute(last_measurement_query)
            last_measurement = last_measurement_result.scalar_one_or_none()
            
            sensor_dict = {
                "id": sensor.id,
                "mac_address": sensor.mac_address,
                "name": sensor.name,
                "is_active": sensor.is_active,
                "battery_level": sensor.battery_level,
                "firmware_version": sensor.firmware_version,
                "last_seen": sensor.last_seen,
                "created_at": sensor.created_at,
                "updated_at": sensor.updated_at,
                "last_measurement": {
                    "temperature": last_measurement.temperature if last_measurement else None,
                    "humidity": last_measurement.humidity if last_measurement else None,
                    "pressure": last_measurement.pressure if last_measurement else None,
                    "battery_voltage": last_measurement.battery_voltage if last_measurement else None,
                    "time": last_measurement.time if last_measurement else None
                } if last_measurement else None
            }
            sensor_data.append(sensor_dict)
            
        return sensor_data
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des capteurs: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(
    sensor_id: int,
    session: AsyncSession = Depends(get_db)
):
    try:
        query = select(Sensor).where(Sensor.id == sensor_id)
        result = await session.execute(query)
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Capteur introuvable")
            
        return sensor
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du capteur {sensor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/{sensor_id}/measurements")
async def get_sensor_measurements(
    sensor_id: int,
    limit: int = Query(100, ge=1, le=1000, description="Nombre de mesures à récupérer"),
    hours: Optional[int] = Query(None, ge=1, le=8760, description="Dernières X heures"),
    start_date: Optional[datetime] = Query(None, description="Date de début (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Date de fin (ISO format)"),
    session: AsyncSession = Depends(get_db)
):
    try:
        sensor_query = select(Sensor).where(Sensor.id == sensor_id)
        sensor_result = await session.execute(sensor_query)
        sensor = sensor_result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Capteur introuvable")
        
        query = select(Measurement).where(Measurement.sensor_id == sensor_id)
        
        if hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = query.where(Measurement.time >= cutoff_time)
        elif start_date or end_date:
            if start_date:
                query = query.where(Measurement.time >= start_date)
            if end_date:
                query = query.where(Measurement.time <= end_date)
        
        query = query.order_by(desc(Measurement.time)).limit(limit)
        
        result = await session.execute(query)
        measurements = result.scalars().all()
        
        formatted_measurements = []
        for measurement in measurements:
            measurement_dict = {
                "time": measurement.time,
                "temperature": measurement.temperature,
                "humidity": measurement.humidity,
                "pressure": measurement.pressure,
                "acceleration_x": measurement.acceleration_x,
                "acceleration_y": measurement.acceleration_y,
                "acceleration_z": measurement.acceleration_z,
                "rssi": measurement.rssi,
                "battery_voltage": measurement.battery_voltage,
                "movement_counter": measurement.movement_counter
            }
            formatted_measurements.append(measurement_dict)
        
        return {
            "sensor_id": sensor_id,
            "sensor_name": sensor.name,
            "sensor_mac": sensor.mac_address,
            "measurement_count": len(formatted_measurements),
            "measurements": formatted_measurements
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des mesures du capteur {sensor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/{sensor_id}/latest")
async def get_latest_measurement(
    sensor_id: int,
    session: AsyncSession = Depends(get_db)
):
    try:
        sensor_query = select(Sensor).where(Sensor.id == sensor_id)
        sensor_result = await session.execute(sensor_query)
        sensor = sensor_result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Capteur introuvable")
        
        query = select(Measurement).where(
            Measurement.sensor_id == sensor_id
        ).order_by(desc(Measurement.time)).limit(1)
        
        result = await session.execute(query)
        measurement = result.scalar_one_or_none()
        
        if not measurement:
            return {
                "sensor_id": sensor_id,
                "sensor_name": sensor.name,
                "sensor_mac": sensor.mac_address,
                "measurement": None,
                "message": "Aucune mesure disponible"
            }
        
        return {
            "sensor_id": sensor_id,
            "sensor_name": sensor.name,
            "sensor_mac": sensor.mac_address,
            "measurement": {
                "time": measurement.time,
                "temperature": measurement.temperature,
                "humidity": measurement.humidity,
                "pressure": measurement.pressure,
                "acceleration_x": measurement.acceleration_x,
                "acceleration_y": measurement.acceleration_y,
                "acceleration_z": measurement.acceleration_z,
                "rssi": measurement.rssi,
                "battery_voltage": measurement.battery_voltage,
                "movement_counter": measurement.movement_counter,
"age_seconds": int((datetime.utcnow() - measurement.time).total_seconds()) if measurement.time else 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la dernière mesure du capteur {sensor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/{sensor_id}/stats")
async def get_sensor_stats(
    sensor_id: int,
    hours: int = Query(24, ge=1, le=8760, description="Période pour les statistiques en heures"),
    session: AsyncSession = Depends(get_db)
):
    try:
        from sqlalchemy import func
        
        sensor_query = select(Sensor).where(Sensor.id == sensor_id)
        sensor_result = await session.execute(sensor_query)
        sensor = sensor_result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Capteur introuvable")
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        stats_query = select(
            func.count(Measurement.time).label('count'),
            func.avg(Measurement.temperature).label('avg_temp'),
            func.min(Measurement.temperature).label('min_temp'),
            func.max(Measurement.temperature).label('max_temp'),
            func.avg(Measurement.humidity).label('avg_humidity'),
            func.min(Measurement.humidity).label('min_humidity'),
            func.max(Measurement.humidity).label('max_humidity'),
            func.avg(Measurement.pressure).label('avg_pressure'),
            func.min(Measurement.pressure).label('min_pressure'),
            func.max(Measurement.pressure).label('max_pressure'),
            func.avg(Measurement.battery_voltage).label('avg_battery')
        ).where(
            and_(
                Measurement.sensor_id == sensor_id,
                Measurement.time >= cutoff_time
            )
        )
        
        result = await session.execute(stats_query)
        stats = result.first()
        
        return {
            "sensor_id": sensor_id,
            "sensor_name": sensor.name,
            "period_hours": hours,
            "measurement_count": stats.count or 0,
            "statistics": {
                "temperature": {
                    "average": round(float(stats.avg_temp or 0), 2),
                    "minimum": round(float(stats.min_temp or 0), 2),
                    "maximum": round(float(stats.max_temp or 0), 2)
                },
                "humidity": {
                    "average": round(float(stats.avg_humidity or 0), 2),
                    "minimum": round(float(stats.min_humidity or 0), 2),
                    "maximum": round(float(stats.max_humidity or 0), 2)
                },
                "pressure": {
                    "average": round(float(stats.avg_pressure or 0), 2),
                    "minimum": round(float(stats.min_pressure or 0), 2),
                    "maximum": round(float(stats.max_pressure or 0), 2)
                },
                "battery": {
                    "average": round(float(stats.avg_battery or 0), 3)
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques du capteur {sensor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")