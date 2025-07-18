<script setup>
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

const humidity = ref<Number | null>(null);
const timestamp = ref<String | null>(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(true);

onMounted(async () => {
    try {
        const data = await fetchSensorData();
        humidity.value = data.humidity;
        timestamp.value = data.timestamp;
    } catch (err) {
        error.value = "Erreur lors de la récupération de l'humidité.";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="humidity">
        <img src="../../assets/svg/drop.png" alt="Drop" style="width: 100px; height: 100px;" />
        <h3>Humidité</h3>
        <div v-if="loading">Chargement...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <p>Humidité: {{ humidity }}%</p>
            <p>Dernière mise à jour: {{ timestamp }}</p>
        </div>
    </div>
</template>

<style scoped>
.humidity {
    background-color: #58A4B0;
    padding: 1rem;
}
</style>
