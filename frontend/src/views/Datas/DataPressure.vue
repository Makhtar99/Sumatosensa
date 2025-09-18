<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

import DataCard from '../Components/DataCard.vue';
import Nano from '../../assets/svg/nanometre.svg';

const pressure = ref<number | null>(1000);
const timestamp = ref<string | null>("12/10/2023 14:30");
const error = ref<string | null>(null);
const loading = ref<boolean>(true);
const roundPressure = (p: number) => Math.round(p * 10) / 10;

onMounted(async () => {
    try {
        const data = await fetchSensorData();
        pressure.value = data.pressure;
        timestamp.value = data.timestamp;
    } catch (err) {
        error.value = "Erreur lors de la récupération de la pression.";
        console.error(err);
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <DataCard
        v-if="!error"
        :title="'Pression'"
        :icon="Nano"
        :value="pressure !== null ? roundPressure(pressure) : 'N/A'"
        unit="hPa"
        :timestamp="timestamp ?? ''"
        color="var(--color-sumato-card-pressure)"
    />
    <div v-else class="p-4 bg-red-100 text-[var(--color-sumato-danger)] rounded-lg">
        {{ error }}
    </div>
</template>