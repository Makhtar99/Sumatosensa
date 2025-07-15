import axios from "axios";

export interface SensorData {
  temperature: number;
  humidity: number;
  pressure: number;
  timestamp: string;
}

export const fetchSensorData = async (): Promise<SensorData> => {
    try {
        const response = await axios.get('http://localhost:3000/sensors/data');
        return response.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des données du capteur:", error);
        throw new Error("Impossible de récupérer les données du capteur");
    }
}

