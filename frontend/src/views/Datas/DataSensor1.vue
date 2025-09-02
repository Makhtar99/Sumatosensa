<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { fetchSensor } from '@/services/sensorService'

import { voltageToPercent } from '@/assets/functions/sensors/VoltageToPercent';
import { formatedTimestamp } from '@/assets/functions/FormatedDate';

const error = ref<string | null>(null);
const loading = ref<boolean>(false);

const currentSensor = ref({
  piece: 'Capteur 1',
  temperature: 0,
  humidite: 0,
  pression: 0,
  batterie: 0,
  statut: '',
  last_update: ''
})

const currentSensorStatus = computed(() => {
  if (currentSensor.value.batterie === 0) {
    return 'Hors ligne'
  }
  if (currentSensor.value.batterie < 20) {
    return 'Batterie faible'
  }
  return 'Connecté'
})


const getBatteryColor = (batterie: number) => {
  if (batterie > 50) return 'text-green-600'
  if (batterie > 20) return 'text-yellow-600'
  return 'text-[var(--color-sumato-danger)]'
}

onMounted(async () => {
  try {
    loading.value = true
    const resp = await fetchSensor()
    const thisSensor = ref(resp[0])
    // console.log(thisSensor.value.last_measurement, 'measurement 1')

    currentSensor.value.piece = thisSensor.value.name || `Capteur ${thisSensor.value.id}`

    if (thisSensor.value.last_measurement) {
      const m = thisSensor.value.last_measurement
      currentSensor.value.temperature = m.temperature
      currentSensor.value.humidite = m.humidity
      currentSensor.value.pression = m.pressure
      currentSensor.value.last_update = formatedTimestamp(m.time)
      currentSensor.value.batterie = voltageToPercent(m.battery_voltage)
      error.value = null
    } else {
      currentSensor.value.statut = 'En ligne'
      currentSensor.value.last_update = ''
      error.value = "Aucune mesure disponible pour le capteur 1."
    }
  } catch (e) {
    console.error(e)
    error.value = "Erreur lors de la récupération des données du capteur 1."
  } finally {
    loading.value = false
  }
})
</script>

<template>

  <div class="bg-[var(--color-surface)] border border-[var(--color-sumato-border)] rounded-xl p-6 space-y-4">
    <h2 class="text-lg !mt-0 font-semibold">{{ currentSensor.piece }} / Salon</h2>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="text-center">
        <p class="text-2xl font-bold text-[var(--color-sumato-primary)]">{{ Math.round(currentSensor.temperature) }}°C</p>
        <span class="text-sm opacity-70">Température</span>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-blue-600">{{ Math.round(currentSensor.humidite) }}%</p>
        <span class="text-sm opacity-70">Humidité</span>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-indigo-600">{{ Math.round(currentSensor.pression) }} hPa</p>
        <span class="text-sm opacity-70">Pression</span>
      </div>
      <div class="text-center">
        <p :class="['text-2xl font-bold', getBatteryColor(currentSensor.batterie)]">
          {{ currentSensor.batterie }}%
        </p>
        <span class="text-sm opacity-70">Batterie</span>
      </div>
    </div>
    <div class="flex justify-between items-center mt-4">
      <span
        class="font-medium"
        :class="{
          '!text-green-600': currentSensorStatus === 'Connecté',
          '!text-yellow-600': currentSensorStatus === 'Batterie faible',
          '!text-[var(--color-sumato-danger)]': currentSensorStatus === 'Hors ligne',
        }"

      >
        ● {{ currentSensorStatus }}
      </span>
      <span class="text-sm text-gray-500"
        >Dernière mise à jour : {{ currentSensor.last_update }}</span
      >
    </div>
  </div>
</template>
