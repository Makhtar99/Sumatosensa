import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.mqtt_client import start_mqtt_client, stop_mqtt_client
from app.models import Base
from app.database import engine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

