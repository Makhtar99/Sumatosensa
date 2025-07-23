<script setup lang="ts">
import { ref, onMounted } from 'vue';
import DataCard from '../Components/DataCard.vue';
// import { fetchSensorData } from '../../services/sensorService';

import Nano from '../../assets/svg/nanometre.svg';

const pressure = ref<Number | null>(null);
const timestamp = ref<String | null>("12/10/2023 14:30");
const error = ref<String | null>(null);
const loading = ref<Boolean>(true);

const getIcon = () => {
    return Nano;
}

// onMounted(async () => {
//     try {
//         const data = await fetchSensorData();
//         pressure.value = data.pressure;
//         timestamp.value = data.timestamp;
//     } catch (err) {
//         error.value = "Erreur lors de la récupération de la pression.";
//     } finally {
//         loading.value = false;
//     }
// });
</script>

<template>
    <DataCard
        v-if="!error"
        :title="'Pression'"
        :icon="getIcon()"
        :value="pressure"
        unit="hPa"
        :timestamp="timestamp"
        color="var(--color-sumato-pressure)"
    />
    <div v-else class="p-4 bg-red-100 text-red-600 rounded-lg">
        {{ error }}
    </div>
</template>