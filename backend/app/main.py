import logging
from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from app.database import get_db

from app.database import engine
from app.models import Base
from app.mqtt_client import start_mqtt_client, stop_mqtt_client
from app.routes import auth, admin, sensors
from app.config import settings
from app.auth import register_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
user = register_user
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Sumātosensā backend...")
    
    # Retry database connection with exponential backoff
    import asyncio
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database connection established successfully")
            break
        except Exception as e:
            logger.error(f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                logger.error("Maximum retry attempts reached. Starting without database connection...")
                logger.warning("Application will start but database operations will fail until connection is restored")
                break
            await asyncio.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    
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
app.include_router(sensors.router)




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