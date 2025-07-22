<script setup lang="ts">
import { ref, onMounted } from 'vue';
// import { fetchSensorData } from '../../services/sensorService';

import Nano from '../../assets/svg/nanometre.svg';

const pressure = ref<Number | null>(null);
const timestamp = ref<String | null>(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(true);

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
    <div class="pressure" style="background-color: var(--color-sumato-pressure); padding: 1rem; border-radius: 8px;">
        <img :src="Nano" alt="Nano svg" />
        <div class="pressure-data">
            <h4>Pression</h4>
            <div v-if="loading">Chargement...</div>
            <div v-else-if="error">{{ error }}</div>
            <div v-else>
                <p>Pression: {{ pressure }} hPa</p>
                <p>Dernière mise à jour: {{ timestamp }}</p>
            </div>
        </div>
    </div>
</template>

