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

const loadWeather = async () => {
    loading.value = true;
    error.value = null;

    try {
        const data = await fetchWeatherData(selectedCity.value);
        temperature.value = Math.round(data);
        timestamp.value = new Date().toLocaleString();
    } catch (err) {
        error.value = "Failed to fetch weather data.";
        console.error(err);
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
  <div class="flex flex-col gap-3 bg-[var(--color-sumato-card-exterior)] rounded-xl">
    <DataCard
        :title="'Météo à ' + selectedCity"
        :icon="Garage"
        :value="temperature ?? 'N/A'"
        unit="°C"
        :timestamp="timestamp ?? ''"
        color="var(--color-sumato-card-exterior)"
    />

    <div v-if="loading" class="text-sumato-500">Chargement...</div>
    <div v-else-if="error" class="text-sumato-warning">{{ error }}</div>

    <div v-else class="flex items-center justify-center pb-2">
      <label for="city" class="sr-only">Choisir une ville</label>
    <select
        id="city"
        v-model="selectedCity"
        @change="onCityChange"
        class="pb-2 w-[90%] rounded-lg border transition"
      >
        <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>
  </div>
</template>
