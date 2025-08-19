import asyncio
import logging
from typing import List
from datetime import datetime
from pydantic import BaseModel
from app.schemas import SensorResponse, SensorRenameRequest, SensorCreateRequest


from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.database import get_async_session
from app.models import Sensor, Measurement
from app.mqtt_client import mqtt_client
from app.schemas import SensorResponse, SensorRenameRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sensors", tags=["sensors"])

class IncomingSensorData(BaseModel):
    source_address: int
    data: dict
    
@router.post("/from-mqtt", response_model=SensorResponse)
async def create_sensor_from_mqtt(payload: IncomingSensorData, session: AsyncSession = Depends(get_async_session)):

    existing = await session.execute(select(Sensor).where(Sensor.mac_address == mac_address))
    sensor = existing.scalar_one_or_none()

    if sensor:
        sensor.last_seen = datetime.utcnow()
        sensor.firmware_version = firmware
    else:
        sensor = Sensor(
            mac_address=mac_address,
            name=f"Sensor-{mac_address}",
            firmware_version=firmware,
            is_active=True
        )
        session.add(sensor)

    await session.commit()
    await session.refresh(sensor)



@router.get("/infos", response_model=List[SensorResponse])
async def get_latest_measurements(session: AsyncSession = Depends(get_async_session)):
    logger.info("Route /sensors/infos called")

    await mqtt_client.request_refresh()
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

@router.post("/register", response_model=SensorResponse)
async def register_sensor(
    request: SensorCreateRequest,
    session: AsyncSession = Depends(get_async_session)
):
    sensor = Sensor(
        mac_address=request.mac_address,
        name=request.name,
        firmware_version=request.firmware_version,
        battery_level=request.battery_level,
    )
    session.add(sensor)
    await session.commit()
    await session.refresh(sensor)
    return sensor

@router.put("/{sensor_id}/rename", response_model=SensorResponse)
async def rename_sensor(sensor_id: int, data: SensorRenameRequest, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor.name = data.name
    await session.commit()
    await session.refresh(sensor)

    return sensor

@router.delete("/{sensor_id}", status_code=204)
async def delete_sensor(sensor_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    await session.delete(sensor)
    await session.commit()
    return Response(status_code=204)

@router.get("/debug")
async def debug_measurements(session: AsyncSession = Depends(get_async_session)):
    results = await session.execute(select(Measurement).order_by(desc(Measurement.time)).limit(10))
    measurements = results.scalars().all()
    for m in measurements:
        logger.info(f"{m.time} - Sensor {m.sensor_id}: temp={m.temperature}, hum={m.humidity}, pres={m.pressure}")
    return {"count": len(measurements)}
