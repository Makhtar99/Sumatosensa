<script setup>
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

const temperature = ref<Number | null>(null);
const timestamp = ref<String | null>(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(true);

onMounted(async () => {
    try {
        const data = await fetchSensorData();
        temperature.value = data.temperature;
        timestamp.value = data.timestamp;
    } catch (err) {
        error.value = "Erreur lors de la récupération de la température.";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="temp">
        <h2>Température</h2>
        <div v-if="loading">Chargement...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <p>Température: {{ temperature }}°C</p>
            <p>Dernière mise à jour: {{ timestamp }}</p>
        </div>
    </div>
</template>

<style scoped>
.temp {
    background-color: #62C370;
    color: white;
    padding: 1rem;
}
</style>
