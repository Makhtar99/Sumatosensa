import axios from "axios";

const API_KEY = import.meta.env.VITE_WEATHER_API_KEY;
const BASE_URL = "https://api.openweathermap.org/data/2.5/weather";

export const fetchWeatherData = async (city: string): Promise<any> => {
  try {
    const response = await axios.get(BASE_URL, {
      params: {
        q: city,
        appid: API_KEY,
        units: "metric",
        },
    });

    return response.data.main.temp
} catch (error) {
    console.error("Erreur lors de la récupération de la température:", error);
    throw new Error("Impossible de récupérer les données météo");
  }
};