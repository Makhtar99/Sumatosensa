<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

const humidity = ref<Number | null>(null);
const timestamp = ref<String | null>(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(false);

onMounted(async () => {
    try {
        const data = await fetchSensorData();
        loading.value = true;
        humidity.value = data.humidity;
        timestamp.value = data.timestamp;
    } catch (err) {
        loading.value = false;
        error.value = "Erreur lors de la récupération de l'humidité.";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="humidity p-4" style="background-color: var(--color-sumato-neutral);">
        <img src="../../assets/svg/drop.png" alt="Drop" />
        <div class="humidity-data">
            <h4>Humidité</h4>
            <div v-if="loading">Chargement...</div>
            <div v-else-if="error">{{ error }}</div>
            <div v-else>
                <p>Humidité: {{ humidity }}%</p>
                <p>Dernière mise à jour: {{ timestamp }}</p>
            </div>
        </div>
    </div>
</template>
