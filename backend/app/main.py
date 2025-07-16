import logging
from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from app.database import get_db
from app.mqtt_client import start_mqtt_client, stop_mqtt_client
from app.models import Base
from app.database import engine
from app.user_services import User

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
user = User
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    logger.info("Starting Sumātosensā backend...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified")
    
    await start_mqtt_client()
    logger.info("MQTT client started")
    
    yield
    
    logger.info("Shutting down Sumātosensā backend...")
    await stop_mqtt_client()
    logger.info("MQTT client stopped")

app = FastAPI(
    title="Sumātosensā API",
    description="Smart Sensors Solution for Workplace Environment",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {
        "message": "Sumātosensā API", 
        "description": "Smart Sensors Solution for Workplace Environment",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sumatosensa-backend"}




@app.post("/", response_model=dict)
async def create_user(username: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await user.create_user(db, username, email, password)
    return {"id": user.id, "username": user.username, "email": user.email}


@app.get("/", response_model=List[dict])
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await user.get_all_users(db)
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]


@app.get("/{user_id}", response_model=dict)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}


@app.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, username: str = None, email: str = None, password: str = None, db: AsyncSession = Depends(get_db)):
    user = await user.update_user(db, user_id, username, email, password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}


@app.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User ID {user_id} deleted successfully"}