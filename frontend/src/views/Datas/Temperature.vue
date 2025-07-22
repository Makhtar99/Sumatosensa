<script setup lang="ts">
import { ref, onMounted } from 'vue';
// import { fetchSensorData } from '../../services/sensorService';

import HighTemp from '../../assets/svg/high_temp.png'
import NormalTemp from '../../assets/svg/normal_temp.png'
import LowTemp from '../../assets/svg/low_temp.png'

const temperature = ref(15); // Default temperature for initial rendering

// const temperature = ref<Number | null>(null);
const timestamp = ref<String | null>(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(false);

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
    <div class="temp text-white p-4 rounded-lg" style="background-color: var(--color-sumato-comfort);">
        <img v-if="temperature > 30" :src="HighTemp" alt="High Temperature" />
        <img v-else-if="temperature > 20" :src="NormalTemp" alt="Normal Temperature" />
        <img v-else :src="LowTemp" alt="Low Temperature" />
        <div class="temperature-data">
            <h4>Température:</h4>
            <div v-if="loading">Chargement...</div>
            <div v-else-if="error">{{ error }}</div>
            <div v-else>
                <p>{{ temperature }} °C</p>
                <p>Dernière mise à jour: {{ timestamp }}</p>
            </div>
        </div>
    </div>
</template>