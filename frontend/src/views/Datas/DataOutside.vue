<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { fetchWeatherData } from '../../services/weatherService';
import DataCard from '../Components/DataCard.vue';
import { usePersistentRef, useTemperatureUnit } from '@/assets/functions/degree';
import { useUserPrefStore } from '@/stores/userpref';

const rawTemperature = ref<number | null>(null);
const error = ref<string | null>(null);
const loading = ref<boolean>(true);
const timestamp = ref<string | null>(null);
const userPrefStore = useUserPrefStore();
const userCity = computed(() => userPrefStore.userCity);

import Garage from '../../assets/svg/garage.svg';

// unite
const temperatureUnit = usePersistentRef<"Celsius" | "Fahrenheit">(
  "temperatureUnit",
  "Celsius"
);

// conversion
const temperature = computed(() => {
  if (rawTemperature.value === null) return null;
  return useTemperatureUnit(
    computed(() => rawTemperature.value ?? 0),
    temperatureUnit
  ).value;
});

const loadWeather = async () => {
    loading.value = true;
    error.value = null;

    try {
        const data = await fetchWeatherData(userCity.value);
        rawTemperature.value = data; 
        timestamp.value = new Date().toLocaleString();
    } catch (err) {
        error.value = "Failed to fetch weather data.";
        console.error(err);
    } finally {
        loading.value = false;
    }
};

onMounted(loadWeather);

</script>

<template>
  <div class="flex flex-col bg-[var(--color-sumato-card-exterior)] rounded-xl h-full">
    <DataCard
        :title="'Météo à ' + userCity"
        :icon="Garage"
        :value="temperature !== null ? Math.round(temperature) : 'N/A'"
        :unit="temperatureUnit === 'Celsius' ? '°C' : '°F'"
        :timestamp="timestamp ?? ''"
        color="var(--color-sumato-card-exterior)"
    />

    <div v-if="loading" class="text-sumato-500">Chargement...</div>
    <div v-else-if="error" class="text-sumato-warning">{{ error }}</div>

  </div>
</template>
