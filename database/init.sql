-- Init sql  スマートセンサー / Sumātosensā project.
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    admin BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    mac_address VARCHAR(17) UNIQUE NOT NULL, 
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    battery_level FLOAT, 
    firmware_version VARCHAR(20),
    last_seen TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS measurements (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id),
    temperature FLOAT NOT NULL, 
    humidity FLOAT NOT NULL, 
    pressure FLOAT NOT NULL, 
    acceleration_x FLOAT, 
    acceleration_y FLOAT, 
    acceleration_z FLOAT, 
    rssi INTEGER, 
    battery_voltage FLOAT, 
    movement_counter INTEGER, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
SELECT create_hypertable('measurements', 'time', if_not_exists => TRUE);
CREATE TABLE IF NOT EXISTS alert_thresholds (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    sensor_id INTEGER REFERENCES sensors(id), 
    parameter VARCHAR(20) NOT NULL CHECK (parameter IN ('temperature', 'humidity', 'pressure')),
    min_value FLOAT,
    max_value FLOAT,
    is_active BOOLEAN DEFAULT true,
    severity VARCHAR(20) DEFAULT 'warning' CHECK (severity IN ('info', 'warning', 'critical')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS measurements_daily (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id),
    temperature FLOAT NOT NULL, 
    humidity FLOAT NOT NULL, 
    pressure FLOAT NOT NULL, 
    acceleration_x FLOAT, 
    acceleration_y FLOAT, 
    acceleration_z FLOAT, 
    rssi INTEGER, 
    battery_voltage FLOAT, 
    movement_counter INTEGER, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
SELECT create_hypertable('measurements_daily', 'time', if_not_exists => TRUE);
CREATE TABLE IF NOT EXISTS alert_thresholds (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    sensor_id INTEGER REFERENCES sensors(id), 
    parameter VARCHAR(20) NOT NULL CHECK (parameter IN ('temperature', 'humidity', 'pressure')),
    min_value FLOAT,
    max_value FLOAT,
    is_active BOOLEAN DEFAULT true,
    severity VARCHAR(20) DEFAULT 'warning' CHECK (severity IN ('info', 'warning', 'critical')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id),
    threshold_id INTEGER NOT NULL REFERENCES alert_thresholds(id),
    parameter VARCHAR(20) NOT NULL,
    value FLOAT NOT NULL,
    threshold_value FLOAT NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT,
    is_resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    report_type VARCHAR(50) NOT NULL CHECK (report_type IN ('daily', 'weekly', 'monthly', 'custom')),
    format VARCHAR(10) NOT NULL CHECK (format IN ('PDF', 'CSV')),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    sensors_included INTEGER[],
    file_path VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_measurements_time ON measurements (time DESC);
CREATE INDEX IF NOT EXISTS idx_measurements_sensor_id ON measurements (sensor_id);
CREATE INDEX IF NOT EXISTS idx_measurements_sensor_time ON measurements (sensor_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_sensors_mac_address ON sensors (mac_address);
CREATE INDEX IF NOT EXISTS idx_sensors_location ON sensors (location_id);
CREATE INDEX IF NOT EXISTS idx_alerts_sensor_id ON alerts (sensor_id);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE MATERIALIZED VIEW IF NOT EXISTS measurements_hourly
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) as avg_temperature,
    AVG(humidity) as avg_humidity,
    AVG(pressure) as avg_pressure,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature,
    MIN(humidity) as min_humidity,
    MAX(humidity) as max_humidity,
    COUNT(*) as measurement_count
FROM measurements
GROUP BY bucket, sensor_id;
CREATE MATERIALIZED VIEW IF NOT EXISTS measurements_daily
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 day', time) AS bucket,
    sensor_id,
    AVG(temperature) as avg_temperature,
    AVG(humidity) as avg_humidity,
    AVG(pressure) as avg_pressure,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature,
    MIN(humidity) as min_humidity,
    MAX(humidity) as max_humidity,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY temperature) as median_temperature,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY humidity) as median_humidity,
    COUNT(*) as measurement_count
FROM measurements
GROUP BY bucket, sensor_id;
SELECT add_retention_policy('measurements', INTERVAL '1 year', if_not_exists => true);
SELECT add_retention_policy('measurements_daily', INTERVAL '1 year', if_not_exists => true);
SELECT add_retention_policy('measurements_hourly', INTERVAL '1 years', if_not_exists => true);
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sensors_updated_at BEFORE UPDATE ON sensors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_alert_thresholds_updated_at BEFORE UPDATE ON alert_thresholds FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
