import axios from "axios";

export interface SensorData {
  temperature: number;
  humidity: number;
  pressure: number;
  timestamp: string;
  battery_voltage: number;
}

const API_BASE_URL = "http://localhost:8000";

type SensorListItem = {
  id: number;
  name?: string;
  last_measurement: null | {
    time: string;
    temperature: number;
    humidity: number;
    pressure: number;
    battery_voltage: number;
  }
};

type LatestResponse = {
  sensor_id: number;
  sensor_name?: string;
  measurement: null | {
    time: string;
    temperature: number;
    humidity: number;
    pressure: number;
    battery_voltage: number;
  };
};

export async function fetchSensor(): Promise<SensorListItem[]> {
  const res = await axios.get<SensorListItem[]>(`${API_BASE_URL}/sensors/`);
  const sensors = res.data;
  return sensors
}

async function fetchFirstSensorId(): Promise<number> {
  const res = await axios.get<SensorListItem[]>(`${API_BASE_URL}/sensors/`);
  const sensors = res.data;
  if (!sensors || sensors.length === 0) {
    throw new Error("Aucun capteur disponible");
  }
  return sensors[0].id;
}

export const fetchSensorData = async (): Promise<SensorData> => {
  try {
    const sensorId = await fetchFirstSensorId();
    const latest = await axios.get<LatestResponse>(
      `${API_BASE_URL}/sensors/${sensorId}/latest`
    );

    if (!latest.data || !latest.data.measurement) {
      throw new Error("Aucune mesure disponible");
    }
    const m = latest.data.measurement;

    return {
      temperature: m.temperature,
      humidity: m.humidity,
      pressure: m.pressure,
      timestamp: m.time,
      battery_voltage: m.battery_voltage,
    };
  } catch (error) {
    console.error("Erreur lors de la récupération des données du capteur:", error);
    throw new Error("Impossible de récupérer les données du capteur");
  }
};

export const fetchLatestBySensorId = async (sensorId: number): Promise<LatestResponse> => {
  try {
    const res = await axios.get<LatestResponse>(`${API_BASE_URL}/sensors/${sensorId}/latest`);
    return res.data;
  } catch (error) {
    console.error(`Erreur lors de /sensors/${sensorId}/latest:`, error);
    throw new Error(`Impossible de récupérer la dernière mesure du capteur ${sensorId}`);
  }
};
