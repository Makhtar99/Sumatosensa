<script setup lang="ts">
import { ref } from 'vue';
import DataCard from '../Components/DataCard.vue';
// import { fetchSensorData } from '../../services/sensorService';

const humidity = ref<number | null>(58);
const timestamp = ref<string | null>("12/10/2023 14:30");
const error = ref<string | null>(null);
// const loading = ref<boolean>(false);

import Drop from '../../assets/svg/drop.png';

const getIcon = () => {
    return Drop;
}

// onMounted(async () => {
//     try {
//         const data = await fetchSensorData();
//         loading.value = true;
//         humidity.value = data.humidity;
//         timestamp.value = data.timestamp;
//     } catch (err) {
//         loading.value = false;
//         console.log(err);
//         error.value = "Erreur lors de la récupération de l'humidité.";
//     } finally {
//         loading.value = false;
//     }
// });
</script>

<template>
    <DataCard
    v-if="!error"
        :title="'Humidité'"
        :icon="getIcon()"
        :value="humidity ?? 'N/A'"
        unit="%"
        :timestamp="timestamp ?? ''"
        color="var(--color-sumato-card-humidity)"
    />
    <div v-else class="p-4 bg-red-100 text-red-600 rounded-lg">
        {{ error }}
    </div>
</template>
