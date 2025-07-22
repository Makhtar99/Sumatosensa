from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.auth import get_current_active_user
from app.database import get_db
from app.models import User, Sensor, Measurement
from app.schemas import SensorResponse, MeasurementResponse, SensorDataResponse

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("/", response_model=List[SensorResponse])
async def get_all_sensors(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    active_only: bool = Query(False, description="Filter active sensors only")
):
    query = select(Sensor).order_by(desc(Sensor.last_seen))
    
    if active_only:
        query = query.where(Sensor.is_active == True)
    
    result = await db.execute(query)
    sensors = result.scalars().all()
    
    return [SensorResponse.model_validate(sensor) for sensor in sensors]

@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(
    sensor_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return SensorResponse.model_validate(sensor)

@router.get("/{sensor_id}/measurements", response_model=List[MeasurementResponse])
async def get_sensor_measurements(
    sensor_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="Number of measurements to retrieve"),
    hours: Optional[int] = Query(None, ge=1, description="Filter measurements from last N hours")
):
    sensor_exists = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    if not sensor_exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    query = select(Measurement).where(Measurement.sensor_id == sensor_id).order_by(desc(Measurement.time))
    
    if hours:
        since_time = datetime.utcnow() - timedelta(hours=hours)
        query = query.where(Measurement.time >= since_time)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    measurements = result.scalars().all()
    
    return [MeasurementResponse.model_validate(measurement) for measurement in measurements]

@router.get("/{sensor_id}/data", response_model=SensorDataResponse)
async def get_sensor_data(
    sensor_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, ge=1, le=500, description="Number of measurements to retrieve"),
    hours: Optional[int] = Query(None, ge=1, description="Filter measurements from last N hours")
):
    sensor_result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = sensor_result.scalar_one_or_none()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    query = select(Measurement).where(Measurement.sensor_id == sensor_id).order_by(desc(Measurement.time))
    
    if hours:
        since_time = datetime.utcnow() - timedelta(hours=hours)
        query = query.where(Measurement.time >= since_time)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    measurements = result.scalars().all()
    
    return SensorDataResponse(
        sensor=SensorResponse.model_validate(sensor),
        measurements=[MeasurementResponse.model_validate(measurement) for measurement in measurements]
    )

@router.get("/data", response_model=List[SensorDataResponse])
async def get_all_sensors_data(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    active_only: bool = Query(True, description="Filter active sensors only"),
    limit: int = Query(10, ge=1, le=100, description="Number of measurements per sensor"),
    hours: Optional[int] = Query(24, ge=1, description="Filter measurements from last N hours")
):
    query = select(Sensor).order_by(desc(Sensor.last_seen))
    
    if active_only:
        query = query.where(Sensor.is_active == True)
    
    result = await db.execute(query)
    sensors = result.scalars().all()
    
    sensors_data = []
    
    for sensor in sensors:
        measurements_query = select(Measurement).where(Measurement.sensor_id == sensor.id).order_by(desc(Measurement.time))
        
        if hours:
            since_time = datetime.utcnow() - timedelta(hours=hours)
            measurements_query = measurements_query.where(Measurement.time >= since_time)
        
        measurements_query = measurements_query.limit(limit)
        
        measurements_result = await db.execute(measurements_query)
        measurements = measurements_result.scalars().all()
        
        sensors_data.append(SensorDataResponse(
            sensor=SensorResponse.model_validate(sensor),
            measurements=[MeasurementResponse.model_validate(measurement) for measurement in measurements]
        ))
    
    return sensors_data

@router.get("/mac/{mac_address}", response_model=SensorResponse)
async def get_sensor_by_mac(
    mac_address: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Sensor).where(Sensor.mac_address == mac_address))
    sensor = result.scalar_one_or_none()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return SensorResponse.model_validate(sensor)

@router.get("/mac/{mac_address}/measurements", response_model=List[MeasurementResponse])
async def get_sensor_measurements_by_mac(
    mac_address: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="Number of measurements to retrieve"),
    hours: Optional[int] = Query(None, ge=1, description="Filter measurements from last N hours")
):
    sensor_result = await db.execute(select(Sensor).where(Sensor.mac_address == mac_address))
    sensor = sensor_result.scalar_one_or_none()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    query = select(Measurement).where(Measurement.sensor_id == sensor.id).order_by(desc(Measurement.time))
    
    if hours:
        since_time = datetime.utcnow() - timedelta(hours=hours)
        query = query.where(Measurement.time >= since_time)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    measurements = result.scalars().all()
    
    return [MeasurementResponse.model_validate(measurement) for measurement in measurements]
