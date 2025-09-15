<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { apiService } from '../services/api'
import { useMediaQuery } from '@vueuse/core'
import { useUserPrefStore } from '@/stores/userpref'

import Temp from './Datas/DataTemperature.vue'
import Humidity from './Datas/DataHumidity.vue'
import Pressure from './Datas/DataPressure.vue'
import Outside from './Datas/DataOutside.vue'
import ConnectedDevices from './Datas/DataConnectedDevices.vue'


const isConnected = ref(false)
const username = ref<string | null>(null)
const isTelephone = useMediaQuery('(max-width: 768px)')


const userPref = useUserPrefStore()


const celsiusValue = ref<number>(0)
const outsideCelsius = ref<number>(0)

const humidityValue = ref<number>(0)
const pressureValue = ref<number>(0)


const temperature = computed(() => {
  return userPref.tempUnit === 'Fahrenheit'
    ? Math.round((celsiusValue.value * 9) / 5 + 32)
    : celsiusValue.value
})

const outsideTemperature = computed(() => {
  return userPref.tempUnit === 'Fahrenheit'
    ? Math.round((outsideCelsius.value * 9) / 5 + 32)
    : outsideCelsius.value
})

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  isConnected.value = !!token
  if (!token) return

})
</script>

<template>
  <div class="grid grid-cols-1 xl:grid-cols-4 gap-6 p-6 w-full">
    <div class="xl:col-span-3 flex flex-col gap-6">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <h1 v-if="username" class="title !mt-0" :class="[ isTelephone ? 'justify-center' : '' ]">
          Bienvenue {{ username.charAt(0).toUpperCase() + username.slice(1) }} !
        </h1>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Temp :temperature="temperature" :unit="userPref.tempUnit" />
        <Humidity :humidity="humidityValue" />
        <Pressure :pressure="pressureValue" />
        <Outside :temperature="outsideTemperature" :unit="userPref.tempUnit" />
      </div>
    </div>

    <div class="h-fit m-auto">
      <ConnectedDevices />
    </div>
  </div>
</template>
