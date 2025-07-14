from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='admin')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True)
    mac_address = Column(String(17), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    battery_level = Column(Float)
    firmware_version = Column(String(20))
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    measurements = relationship("Measurement", back_populates="sensor")
    alert_thresholds = relationship("AlertThreshold", back_populates="sensor")

class Measurement(Base):
    __tablename__ = "measurements"
    
    time = Column(DateTime(timezone=True), nullable=False, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False, primary_key=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    acceleration_x = Column(Float)
    acceleration_y = Column(Float)
    acceleration_z = Column(Float)
    rssi = Column(Integer)
    battery_voltage = Column(Float)
    movement_counter = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sensor = relationship("Sensor", back_populates="measurements")

class AlertThreshold(Base):
    __tablename__ = "alert_thresholds"
    
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    parameter = Column(String(20), nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    is_active = Column(Boolean, default=True)
    severity = Column(String(20), default='warning')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    sensor = relationship("Sensor", back_populates="alert_thresholds")
    alerts = relationship("Alert", back_populates="threshold")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    threshold_id = Column(Integer, ForeignKey("alert_thresholds.id"), nullable=False)
    parameter = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    threshold_value = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(Text)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sensor = relationship("Sensor")
    threshold = relationship("AlertThreshold", back_populates="alerts")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String(50), nullable=False)
    format = Column(String(10), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    sensors_included = Column(ARRAY(Integer))
    file_path = Column(String(255))
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    user = relationship("User")