<script setup lang="ts">
import { ref, onMounted } from 'vue';
import DataCard from '../Components/DataCard.vue';
import { fetchSensorData } from '../../services/sensorService';

import HighTemp from '../../assets/svg/high_temp.png';
import NormalTemp from '../../assets/svg/normal_temp.png';
import LowTemp from '../../assets/svg/low_temp.png';

const temperature = ref<number | null>(null);
const timestamp = ref<string | null>(null);
const error = ref<string | null>(null);
const loading = ref<boolean>(false);

const getIcon = () => {
  if (temperature.value === null) return LowTemp;
  if (temperature.value > 30) return HighTemp;
  if (temperature.value > 20) return NormalTemp;
  return LowTemp;
};

onMounted(async () => {
  try {
    loading.value = true;
    const data = await fetchSensorData();
    temperature.value = data.temperature;
    timestamp.value = data.timestamp;
    error.value = null;
  } catch (err) {
    console.error(err);
    error.value = "Erreur lors de la récupération de la température.";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <DataCard
    v-if="!error"
    :title="'Température'"
    :icon="getIcon()"
    :value="temperature !== null ? Math.round(temperature) : 'N/A'"
    unit="°C"
    :timestamp="timestamp ?? ''"
    color="var(--color-sumato-card-temp)"
  />
  <div v-else class="p-4 bg-red-100 text-[var(--color-sumato-danger)] rounded-lg">
    {{ error }}
  </div>
</template>
