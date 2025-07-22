from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class SensorResponse(BaseModel):
    id: int
    mac_address: str
    name: str
    is_active: bool
    battery_level: Optional[float] = None
    firmware_version: Optional[str] = None
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MeasurementResponse(BaseModel):
    time: datetime
    sensor_id: int
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    acceleration_x: Optional[float] = None
    acceleration_y: Optional[float] = None
    acceleration_z: Optional[float] = None
    rssi: Optional[int] = None
    battery_voltage: Optional[float] = None
    movement_counter: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SensorDataResponse(BaseModel):
    sensor: SensorResponse
    measurements: list[MeasurementResponse]
