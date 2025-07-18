<script setup>
import { ref, onMounted } from 'vue';
import { fetchSensorData } from '../../services/sensorService';

import HighTemp from '../../assets/svg/high_temp.png'
import NormalTemp from '../../assets/svg/normal_temp.png'
import LowTemp from '../../assets/svg/low_temp.png'

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
        <img v-if="temperature > 30" :src="HighTemp" alt="High Temperature" style="width: 100px; height: 100px;" />
        <img v-else-if="temperature > 20" :src="NormalTemp" alt="Normal Temperature" style="width: 100px; height: 100px;" />
        <img v-else :src="LowTemp" alt="Low Temperature" style="width: 100px; height: 100px;" />
        <div v-if="loading">Chargement...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <h3>Température: {{ temperature }}°C</h3>
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
