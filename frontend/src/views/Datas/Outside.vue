<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchWeatherData } from '../../services/weatherService';

const cities = ['Paris', 'La Rochelle', 'Marseille', 'Lyon']; // Liste des villes
const selectedCity = ref('Paris'); // Ville par défaut
const temperature = ref<number | null>(null);
const error = ref<string | null>(null);
const loading = ref<boolean>(true);
const timestamp = ref<string | null>(null);

import Garage from '../../assets/svg/garage.svg';

const loadWeather = async () => {
    loading.value = true;
    error.value = null;

    try {
        const data = await fetchWeatherData(selectedCity.value);
        temperature.value = data;
        timestamp.value = new Date().toLocaleString();
    } catch (err) {
        error.value = "Failed to fetch weather data.";
    } finally {
        loading.value = false;
    }
};

onMounted(loadWeather);

const onCityChange = () => {
    loadWeather();
};
</script>


<template>
    <div class="outside">
        <img :src="Garage" alt="Garage svg" />
        <h4>Extérieur</h4>

        <div v-if="loading">Loading...</div>
        <div v-else-if="error">{{ error }}</div>

        <div v-else class="outside-data">
            <p>Température : {{ temperature !== null ? Math.round(temperature) + '°C' : 'N/A' }}</p>
            <p>Dernière mise à jour : {{ timestamp }}</p>

            <select v-model="selectedCity" @change="onCityChange">
                <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
            </select>
        </div>
    </div>
</template>
