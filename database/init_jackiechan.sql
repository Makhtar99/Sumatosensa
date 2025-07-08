-- 1. Table des alertes principales
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Table des types d’alertes liées aux capteurs
CREATE TABLE alerts_sensor (
    id SERIAL PRIMARY KEY,
    alert_id INTEGER NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    sensor_type TEXT NOT NULL CHECK (sensor_type IN ('temperature', 'humidity', 'pressure', 'acceleration')),
    threshold_min REAL,
    threshold_max REAL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Table des événements déclenchés par des alertes
CREATE TABLE alerts_events (
    id SERIAL PRIMARY KEY,
    alert_sensor_id INTEGER NOT NULL REFERENCES alerts_sensor(id) ON DELETE CASCADE,
    device_id UUID NOT NULL,
    triggered_value REAL NOT NULL,
    triggered_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Table des capteurs connectés (devices)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    location TEXT,
    last_seen TIMESTAMPTZ DEFAULT NOW()
);
