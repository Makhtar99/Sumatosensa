import axios from "axios";

const API_KEY = import.meta.env.VITE_WEATHER_API_KEY;
const BASE_URL = import.meta.env.VITE_WEATHER_BASE_URL;

export const fetchWeatherData = async (city: string): Promise<any> => {
  try {
    console.log("API KEY:", API_KEY)
    console.log("BASE URL:", BASE_URL)
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