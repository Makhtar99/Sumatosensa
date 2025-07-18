from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from app.database import get_db

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_async_session
from app.models import Sensor, Measurement

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("/temperatures")
async def get_latest_temperatures(db: AsyncSession = Depends(get_async_session)):
    sensors = await db.execute(select(Sensor))
    sensors = sensors.scalars().all()
    results = []
    for sensor in sensors:
        stmt = (
            select(Measurement)
            .where(Measurement.sensor_id == sensor.id)
            .where(Measurement.temperature != None)
            .order_by(desc(Measurement.timestamp))
            .limit(1)
        )
        measurement = await db.execute(stmt)
        measurement = measurement.scalar_one_or_none()
        results.append({
            "sensor_id": sensor.id,
            "mac_address": sensor.mac_address,
            "temperature": measurement.temperature if measurement else None,
            "timestamp": measurement.timestamp.isoformat() if measurement else None
        })
    return results

@router.get("/pressures")
async def get_latest_pressures(session: AsyncSession = Depends(get_async_session)):
    sensors = await session.execute(select(Sensor))
    sensors = sensors.scalars().all()
    results = []
    for sensor in sensors:
        stmt = (
            select(Measurement)
            .where(Measurement.sensor_id == sensor.id)
            .where(Measurement.pressure != None)
            .order_by(desc(Measurement.timestamp))
            .limit(1)
        )
        measurement = await session.execute(stmt)
        measurement = measurement.scalar_one_or_none()
        results.append({
            "sensor_id": sensor.id,
            "mac_address": sensor.mac_address,
            "pressure": measurement.pressure if measurement else None,
            "timestamp": measurement.timestamp.isoformat() if measurement else None
        })
    return results

@router.get("/humidities")
async def get_latest_humidities(session: AsyncSession = Depends(get_async_session)):
    sensors = await session.execute(select(Sensor))
    sensors = sensors.scalars().all()
    results = []
    for sensor in sensors:
        stmt = (
            select(Measurement)
            .where(Measurement.sensor_id == sensor.id)
            .where(Measurement.humidity != None)
            .order_by(desc(Measurement.timestamp))
            .limit(1)
        )
        measurement = await session.execute(stmt)
        measurement = measurement.scalar_one_or_none()
        results.append({
            "sensor_id": sensor.id,
            "mac_address": sensor.mac_address,
            "humidity": measurement.humidity if measurement else None,
            "timestamp": measurement.timestamp.isoformat() if measurement else None
        })
    return results

