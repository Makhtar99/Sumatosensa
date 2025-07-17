from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.auth import get_current_admin_user
from app.database import get_db
from app.models import User, Sensor, Alert
from app.schemas import UserResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]

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