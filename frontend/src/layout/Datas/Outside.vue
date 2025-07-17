<script setup>
import { ref, onMounted } from 'vue';
import { fetchWeatherData } from '../../services/weatherService';

const city = "Paris";
const temperature = ref(null);
const error = ref<String | null>(null);
const loading = ref<Boolean>(true);

import Garage from '../../assets/svg/garage.svg';

onMounted(async () => {
    try {
        const data = await fetchWeatherData(city);
        temperature.value = data;
    } catch (err) {
        error.value = "Failed to fetch weather data.";
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="outside">

        <img :src="Garage" alt="Garage svg" style="width: 100px; height: 100px;" />
        <h2>Température à {{ city }}</h2>
        <div v-if="loading">Loading...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <p>Temperature: {{ temperature }}°C</p>
        </div>
    </div>
</template>

<style scoped>

</style>