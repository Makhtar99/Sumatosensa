import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.mqtt_client import start_mqtt_client, stop_mqtt_client
from app.routes import auth, admin
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Sumātosensā backend...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await start_mqtt_client()
    yield
    await stop_mqtt_client()

app = FastAPI(title="Sumātosensā API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Sumātosensā API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(auth.router)
app.include_router(admin.router)

