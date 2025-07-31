import pytest
from app.auth import verify_password, get_password_hash, create_access_token
from app.models import User, Sensor


def test_password_hashing():
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_password_verification():
    password = "secure_password"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_jwt_token_creation():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_user_model_creation():
    user = User()
    user.username = "testuser"
    user.email = "test@example.com"  
    user.password_hash = "hashed_password"
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password"


def test_sensor_model_creation():
    sensor = Sensor()
    sensor.mac_address = "AA:BB:CC:DD:EE:FF"
    sensor.name = "Test Sensor"
    sensor.battery_level = 85.5
    
    assert sensor.mac_address == "AA:BB:CC:DD:EE:FF"
    assert sensor.name == "Test Sensor"
    assert sensor.battery_level == 85.5


def test_different_passwords_have_different_hashes():
    password1 = "password1"
    password2 = "password2"
    
    hash1 = get_password_hash(password1)
    hash2 = get_password_hash(password2)
    
    assert hash1 != hash2


def test_mac_address_formats():
    valid_macs = [
        "AA:BB:CC:DD:EE:FF",
        "00:11:22:33:44:55",
        "FF:EE:DD:CC:BB:AA"
    ]
    
    for mac in valid_macs:
        sensor = Sensor()
        sensor.mac_address = mac
        sensor.name = "Test Sensor"
        assert sensor.mac_address == mac


def test_battery_levels():
    test_levels = [0.0, 25.5, 50.0, 75.7, 100.0]
    
    for level in test_levels:
        sensor = Sensor()
        sensor.mac_address = "AA:BB:CC:DD:EE:FF"
        sensor.name = "Test Sensor"
        sensor.battery_level = level
        assert sensor.battery_level == level