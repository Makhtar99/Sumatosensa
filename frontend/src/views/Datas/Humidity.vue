<script setup lang="ts">
import { ref, onMounted } from 'vue';
import DataCard from '../Components/DataCard.vue';
// import { fetchSensorData } from '../../services/sensorService';

const humidity = ref<Number | null>(58);
const timestamp = ref<String | null>("12/10/2023 14:30");
const error = ref<String | null>(null);
const loading = ref<Boolean>(false);

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
        :value="humidity"
        unit="%"
        :timestamp="timestamp"
        color="var(--color-sumato-neutral)"
    />
    <div v-else class="p-4 bg-red-100 text-red-600 rounded-lg">
        {{ error }}
    </div>
</template>
