import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_async_session
from app.models import Sensor, Measurement
from app.mqtt_client import mqtt_client 

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("/infos")
async def get_latest_measurements(session: AsyncSession = Depends(get_async_session)):
    logger.info("Route /sensors/infos called")

    mqtt_client.request_refresh() 
    await asyncio.sleep(2)  

    sensors = await session.execute(select(Sensor))
    sensors = sensors.scalars().all()
    results = []

    for sensor in sensors:
        stmt = (
            select(Measurement)
            .where(Measurement.sensor_id == sensor.id)
            .order_by(desc(Measurement.timestamp))
            .limit(1)
        )
        measurement = await session.execute(stmt)
        measurement = measurement.scalar_one_or_none()
        results.append({
            "sensor_id": sensor.id,
            "mac_address": sensor.mac_address,
            "temperature": measurement.temperature if measurement else None,
            "humidity": measurement.humidity if measurement else None,
            "pressure": measurement.pressure if measurement else None,
        })

    return results