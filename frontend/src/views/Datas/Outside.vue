<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchWeatherData } from '../../services/weatherService';
import DataCard from '../Components/DataCard.vue';

const cities = ['Paris', 'La Rochelle', 'Marseille', 'Lyon'];
const selectedCity = ref('Paris');
const temperature = ref<number | null>(null);
const error = ref<string | null>(null);
const loading = ref<boolean>(true);
const timestamp = ref<string | null>(null);

import Garage from '../../assets/svg/garage.svg';

const getIcon = () => {
    return Garage;
}

const loadWeather = async () => {
    loading.value = true;
    error.value = null;

    try {
        const data = await fetchWeatherData(selectedCity.value);
        temperature.value = Math.round(data);
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
  <div class="outside flex flex-col gap-3">
    <DataCard
        :title="'Météo à ' + selectedCity"
        :icon="getIcon()"
        :value="temperature"
        unit="°C"
        :timestamp="timestamp"
        color="var(--color-sumato-weather)"
    />

    <div v-if="loading" class="text-sumato-500">Chargement...</div>
    <div v-else-if="error" class="text-sumato-warning">{{ error }}</div>

    <div v-else class="flex flex-col gap-2">
    <select
        id="city"
        v-model="selectedCity"
        @change="onCityChange"
        class="px-3 py-2 rounded-lg border border-sumato-300 focus:outline-none focus:ring-2 focus:ring-sumato-primary text-sumato-700 dark:bg-sumato-dark-200 dark:text-white transition"
      >
        <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>
  </div>
</template>
