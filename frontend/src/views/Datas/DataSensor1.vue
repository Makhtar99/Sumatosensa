<script setup lang="ts">
import { ref, computed } from 'vue'
import sensors from '../../assets/json/sensors_data.json'

const selectedRoom = ref('Salon')
const sensorList = ref(sensors)

const currentSensor = computed(() =>
  sensorList.value.find(sensor => sensor.piece === selectedRoom.value) ?? {
    piece: '',
    temperature: 0,
    humidite: 0,
    pression: 0,
    batterie: 0,
    statut: 'hors ligne',
    last_update: ''
  }
)

const getBatteryColor = (batterie: number) => {
  if (batterie > 50) return 'text-green-600'
  if (batterie > 20) return 'text-yellow-600'
  return 'text-red-600'
}
</script>

<template>
  <div class="p-6">
    <h1 class="title mb-6">Salon</h1>
  </div>

  <div class="bg-[var(--color-surface)] shadow-lg rounded-xl p-6 space-y-4">
    <h2 class="text-lg font-semibold">{{ currentSensor.piece }}</h2>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="text-center">
        <p class="text-2xl font-bold text-sumato-primary">{{ currentSensor.temperature }}°C</p>
        <span class="text-sm opacity-70">Température</span>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-blue-600">{{ currentSensor.humidite }}%</p>
        <span class="text-sm opacity-70">Humidité</span>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-indigo-600">{{ currentSensor.pression }} hPa</p>
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
          'text-green-600': currentSensor.statut === 'connecté',
          'text-yellow-600': currentSensor.statut === 'batterie faible',
          'text-red-600': currentSensor.statut === 'hors ligne',
        }"
      >
        ● {{ currentSensor.statut }}
      </span>
      <span class="text-sm text-gray-500"
        >Dernière mise à jour : {{ currentSensor.last_update }}</span
      >
    </div>
  </div>
</template>
