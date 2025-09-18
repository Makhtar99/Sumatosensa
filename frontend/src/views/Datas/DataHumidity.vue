<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

import DataCard from '../Components/DataCard.vue';
import Drop from '../../assets/svg/drop.png';

const humidity = ref<number | null>(58);
const timestamp = ref<string | null>("12/10/2023 14:30");
const error = ref<string | null>(null);
const loading = ref<boolean>(false);

onMounted(async () => {
    try {
        loading.value = true;
        const data = await fetchSensorData();
        humidity.value = data.humidity;
        timestamp.value = data.timestamp;
    } catch (err) {
        loading.value = false;
        console.error(err);
        error.value = "Erreur lors de la récupération de l'humidité.";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <DataCard
        v-if="!error"
        :title="'Humidité'"
        :icon="Drop"
        :value="humidity !== null ? Math.round(humidity) : 'N/A'"
        unit="%"
        :timestamp="timestamp ?? ''"
        color="var(--color-sumato-card-humidity)"
    />
    <div v-else class="p-4 bg-red-100 text-[var(--color-sumato-danger)] rounded-lg">
        {{ error }}
    </div>
</template>
