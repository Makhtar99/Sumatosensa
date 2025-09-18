import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export interface SensorData {
  temperature: number;
  humidity: number;
  pressure: number;
  timestamp: string;
  battery_voltage: number;
}

export type SensorListItem = {
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

export type CreateSensorPayload = {
  name: string
  // ajoute ici d'autres champs si ton backend les attend à la création
}

export type UpdateSensorPayload = {
  name?: string
  // ajoute ici d'autres champs éditables si besoin
}

// list
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

// GET ID
export async function getSensor(sensorId: number): Promise<SensorListItem> {
  const { data } = await axios.get<SensorListItem>(`${API_BASE_URL}/sensors/${sensorId}/`);
  return data;
}

// CREATE
export async function createSensor(payload: CreateSensorPayload): Promise<SensorListItem> {
  const { data } = await axios.post<SensorListItem>(`${API_BASE_URL}/sensors/`, payload);
  return data;
}

// UPDATE
export const updateSensor = async (sensorId: number, data: Partial<SensorListItem>): Promise<SensorListItem> => {
  try {
    const response = await axios.put<SensorListItem>(`${API_BASE_URL}/sensors/${sensorId}/`, data);
    return response.data;
  } catch (error) {
    console.error(`Erreur lors de la mise à jour du capteur ${sensorId}:`, error);
    throw new Error(`Impossible de mettre à jour le capteur ${sensorId}`);
  }
};

// DELETE
export async function deleteSensor(sensorId: number): Promise<void> {
  try {
    await axios.delete(`${API_BASE_URL}/sensors/${sensorId}/`);
  } catch (error) {
    console.error(`Erreur lors de la suppression du capteur ${sensorId}:`, error);
    throw new Error(`Impossible de supprimer le capteur ${sensorId}`);
  }
}