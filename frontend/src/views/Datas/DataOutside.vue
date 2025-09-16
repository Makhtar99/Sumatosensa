<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { fetchWeatherData } from '../../services/weatherService';
import DataCard from '../Components/DataCard.vue';
import { usePersistentRef, useTemperatureUnit } from '@/assets/functions/degree';

// const cities = ['Paris', 'La Rochelle', 'Marseille', 'Lyon'];
const selectedCity = ref('Paris');
const rawTemperature = ref<number | null>(null);
const error = ref<string | null>(null);
const loading = ref<boolean>(true);
const timestamp = ref<string | null>(null);

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
        const data = await fetchWeatherData(selectedCity.value);
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

// const onCityChange = () => {
//     loadWeather();
// };
</script>

<template>
  <div class="flex flex-col bg-[var(--color-sumato-card-exterior)] rounded-xl h-full">
    <DataCard
        :title="'Météo à ' + selectedCity"
        :icon="Garage"
        :value="temperature !== null ? Math.round(temperature) : 'N/A'"
        :unit="temperatureUnit === 'Celsius' ? '°C' : '°F'"
        :timestamp="timestamp ?? ''"
        color="var(--color-sumato-card-exterior)"
    />

    <div v-if="loading" class="text-sumato-500">Chargement...</div>
    <div v-else-if="error" class="text-sumato-warning">{{ error }}</div>

    <!-- <div v-else class="flex items-center justify-center pb-2">
      <label for="city" class="sr-only">Choisir une ville</label> -->
    <!-- <select
        id="city"
        v-model="selectedCity"
        @change="onCityChange"
        class="pb-2 w-[90%] rounded-lg border transition"
      >
        <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
      </select> -->
    <!-- </div> -->
  </div>
</template>
<!-- 

<script setup lang="ts">
import { ref, watch } from 'vue'
import { usePrefsStore } from '@/stores/prefs'
import { fetchWeatherData } from '../../services/weatherService'
import DataCard from '../Components/DataCard.vue'
import Garage from '../../assets/svg/garage.svg'

const prefs = usePrefsStore()

const temperature = ref<number | null>(null)
const error = ref<string | null>(null)
const loading = ref<boolean>(false)
const timestamp = ref<string | null>(null)

const loadWeather = async (city: string) => {
  loading.value = true
  error.value = null
  try {
    const data = await fetchWeatherData(city)
    temperature.value = Math.round(data)
    timestamp.value = new Date().toLocaleString()
  } catch (err) {
    console.error(err)
    error.value = 'Failed to fetch weather data.'
  } finally {
    loading.value = false
  }
}

watch(
  () => prefs.selectedCity,
  (city, _prev) => { if (city) loadWeather(city) },
  { immediate: true }
)
</script>

<template>
  <div class="flex flex-col gap-3 bg-[var(--color-sumato-card-exterior)] rounded-xl">
    <DataCard
      :title="'Météo à ' + prefs.selectedCity"
      :icon="Garage"
      :value="temperature ?? 'N/A'"
      unit="°C"
      :timestamp="timestamp ?? ''"
      color="var(--color-sumato-card-exterior)"
    />

    <div v-if="loading" class="text-sumato-500">Chargement...</div>
    <div v-else-if="error" class="text-sumato-warning">{{ error }}</div>
  </div>
</template> -->
