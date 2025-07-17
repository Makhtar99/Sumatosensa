<script setup>
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

import Nano from '../../assets/svg/nanometre.svg';

const pressure = ref<Number | null>(null);
const timestamp = ref<String | null>(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(true);

onMounted(async () => {
    try {
        const data = await fetchSensorData();
        pressure.value = data.pressure;
        timestamp.value = data.timestamp;
    } catch (err) {
        error.value = "Erreur lors de la récupération de la pression.";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="pressure">
        <img :src="Nano" alt="Nano svg" style="width: 100px; height: 100px;" />
        <h2>Pression</h2>
        <div v-if="loading">Chargement...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <p>Pression: {{ pressure }} hPa</p>
            <p>Dernière mise à jour: {{ timestamp }}</p>
        </div>
    </div>
</template>

<style scoped>
.pressure {
    background-color: #FCD490;
    padding: 1rem;
}
</style>
