<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { fetchSensor } from '@/services/sensorService'
import { useUserPrefStore } from '@/stores/userpref'
import { computeSensorStatus, computeSensorAlert, voltageToPercent } from '@/assets/functions/sensors/SensorFunctions'

import DataSensor from '../Components/DataSensor.vue'

const error = ref<string | null>(null)
const loading = ref(false)
const userPref = useUserPrefStore()

const currentSensor = ref({
  piece: 'Capteur 2',
  location: 'Chambre parentale',
  temperature: 0,
  humidite: 0,
  pression: 0,
  batterie: 0,
  last_update: ''
})

const status = computed(() => computeSensorStatus(currentSensor.value.batterie))

const alertMessage = computed(() => computeSensorAlert(currentSensor.value))

onMounted(async () => {
  try {
    loading.value = true
    const resp = await fetchSensor()
    const sensor = resp[1]

    currentSensor.value.piece = userPref.sensor2name

    if (sensor.last_measurement) {
      const m = sensor.last_measurement
      currentSensor.value.temperature = m.temperature
      currentSensor.value.humidite = m.humidity
      currentSensor.value.pression = m.pressure
      currentSensor.value.batterie = voltageToPercent(m.battery_voltage)
      currentSensor.value.last_update = m.time
    } else {
      error.value = "Aucune mesure disponible pour le capteur."
    }
  } catch (e) {
    console.error(e)
    error.value = "Erreur lors de la récupération des données."
  } finally {
    loading.value = false
  }
})
</script>


<template>
  <DataSensor
    v-if="!error"
    v-bind="currentSensor"
    :status="status"
    :message-alert="alertMessage"
  />

  <div v-else class="p-4 bg-red-100 text-[var(--color-sumato-danger)] rounded-lg">
    {{ error }}
  </div>
</template>
