<script setup lang="ts">
import { ref, onMounted } from 'vue';
import DataCard from '../Components/DataCard.vue';
// import { fetchSensorData } from '../../services/sensorService';

import HighTemp from '../../assets/svg/high_temp.png'
import NormalTemp from '../../assets/svg/normal_temp.png'
import LowTemp from '../../assets/svg/low_temp.png'
// import { fa } from 'zod/locales';

const temperature = ref(18);
const timestamp = ref<String | null>("12/10/2023 14:30");
const error = ref<String | null>(null);
const loading = ref<Boolean>(false);

const getIcon = () => {
    if (temperature.value > 30) return HighTemp;
    if (temperature.value > 20) return NormalTemp;
    return LowTemp;
}

// onMounted(async () => {
//     try {
//         loading.value = true;
//         const data = await fetchSensorData();
//         temperature.value = data.temperature;
//         timestamp.value = data.timestamp;
//     } catch (err) {
//         loading.value = false;
//         error.value = "Erreur lors de la récupération de la température.";
//     } finally {
//         loading.value = false;
//     }
// });
</script>

<template>
   <DataCard
    v-if="!error"
        :title="'Température'"
        :icon="getIcon()"
        :value="temperature"
        unit="°C"
        :timestamp="timestamp"
        color="var(--color-sumato-comfort)"
    />
    <div v-else class="p-4 bg-red-100 text-red-600 rounded-lg">
        {{ error }}
    </div>
</template>