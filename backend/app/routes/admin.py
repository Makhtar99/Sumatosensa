from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from typing import List, Optional
from datetime import datetime

from app.auth import get_current_admin_user
from app.database import get_db
from app.models import User, Sensor, Alert, Measurement
from app.schemas import UserResponse, SensorResponse, UserUpdate

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    if update_data:
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
    
    return UserResponse.model_validate(user)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    return {"message": "User deleted successfully"}

@router.get("/dashboard")
async def get_admin_dashboard(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    sensors_count = await db.execute(select(func.count(Sensor.id)))
    total_sensors = sensors_count.scalar()
    
    active_sensors_count = await db.execute(
        select(func.count(Sensor.id)).where(Sensor.is_active == True)
    )
    active_sensors = active_sensors_count.scalar()
    
    unresolved_alerts_count = await db.execute(
        select(func.count(Alert.id)).where(Alert.is_resolved == False)
    )
    unresolved_alerts = unresolved_alerts_count.scalar()
    
    users_count = await db.execute(select(func.count(User.id)))
    total_users = users_count.scalar()
    
    return {
        "total_sensors": total_sensors,
        "active_sensors": active_sensors,
        "unresolved_alerts": unresolved_alerts,
        "total_users": total_users
    }

# CRUD DEVICES (Admin only)
@router.post("/sensors", response_model=SensorResponse)
async def create_sensor(
    source_address: str,
    name: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    sensor = Sensor(
        source_address=source_address,
        name=name,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(sensor)
    await db.commit()
    await db.refresh(sensor)
    return SensorResponse.model_validate(sensor)

@router.put("/sensors/{sensor_id}", response_model=SensorResponse)
async def update_sensor(
    sensor_id: int,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    if name is not None:
        sensor.name = name
    if is_active is not None:
        sensor.is_active = is_active
    
    sensor.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(sensor)
    return SensorResponse.model_validate(sensor)

@router.delete("/sensors/{sensor_id}")
async def delete_sensor(
    sensor_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    sensor = result.scalar_one_or_none()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    await db.execute(delete(Sensor).where(Sensor.id == sensor_id))
    await db.commit()
    return {"message": "Sensor deleted successfully"}

@router.get("/export/sensors")
async def export_sensors_data(
    format: str = "json",  # "json" ou "csv"
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sensor_ids: Optional[List[int]] = None,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    if format not in ["json", "csv"]:
        raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")
    
    query = select(Measurement)
    
    if start_date:
        query = query.where(Measurement.time >= start_date)
    if end_date:
        query = query.where(Measurement.time <= end_date)
    if sensor_ids:
        query = query.where(Measurement.sensor_id.in_(sensor_ids))
    
    result = await db.execute(query.order_by(Measurement.time.desc()))
    measurements = result.scalars().all()
    
    if format == "json":
        return {
            "data": [
                {
                    "time": measurement.time.isoformat(),
                    "sensor_id": measurement.sensor_id,
                    "temperature": measurement.temperature,
                    "humidity": measurement.humidity,
                    "pressure": measurement.pressure,
                    "acceleration_x": measurement.acceleration_x,
                    "acceleration_y": measurement.acceleration_y,
                    "acceleration_z": measurement.acceleration_z,
                    "rssi": measurement.rssi,
                    "battery_voltage": measurement.battery_voltage,
                    "movement_counter": measurement.movement_counter
                } for measurement in measurements
            ],
            "count": len(measurements),
            "exported_at": datetime.utcnow().isoformat()
        }
    
    # TODO: Implémenter l'export CSV
    return {"message": "CSV export not implemented yet"}