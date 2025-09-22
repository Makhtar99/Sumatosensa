from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=1800,  # Recycle connections every 30 minutes
    pool_reset_on_return='commit',
    connect_args={
        "command_timeout": 30,
        "server_settings": {
            "application_name": "sumatosensa_backend",
        }
    }
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

@asynccontextmanager
async def get_async_session():
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_db():
    """FastAPI dependency for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()