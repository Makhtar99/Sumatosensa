import os
from datetime import timedelta

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8
    
    @property
    def DATABASE_URL(self) -> str:
        # Try production DATABASE_URL first, then fallback to Docker Compose format
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            # Fallback to Docker Compose format for local development
            postgres_user = os.getenv("POSTGRES_USER", "sumatosensa_user")
            postgres_password = os.getenv("POSTGRES_PASSWORD", "sumatosensa_password") 
            postgres_db = os.getenv("POSTGRES_DB", "sumatosensa")
            postgres_host = os.getenv("DATABASE_HOST", "sumatosensa_db")
            postgres_port = os.getenv("DATABASE_PORT", "5432")
            
            db_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        
        # Convert postgres:// to postgresql+asyncpg:// for async SQLAlchemy
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif db_url.startswith("postgresql://") and "asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url
    
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "")
    
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"]

settings = Settings()