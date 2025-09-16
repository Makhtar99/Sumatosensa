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
import DashboardChart from './Components/Dashboard/DashboardChart.vue'
import DarhboardSkeleton from './Components/Dashboard/DarhboardSkeleton.vue'

const onLoading = ref(true)
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

const selectedPeriod = ref<'today' | 'thisWeek' | 'fullMonth'>('fullMonth')

onMounted(async () => {
  onLoading.value = true
  const token = localStorage.getItem('access_token')
  isConnected.value = !!token
  if (!token) {
    return
  } else {
    try {
      const user = await apiService.getCurrentUser()
      username.value = user.username
    } catch (error) {
      console.error("Impossible de récupérer l'utilisateur :", error)
    }
  }
  onLoading.value = false
})
</script>

<template>
  <div>
    <DarhboardSkeleton v-if="onLoading" />
  </div>

  <div v-if="!onLoading" class="w-full max-w-screen h-full flex flex-col justify-between gap-6"
    :class="[isTelephone ? 'p-4' : 'pr-[2rem] pb-8']">
    <div>
      <h1 v-if="username" class="flex justify-start !my-0 !p-0 text-center title">
        Bienvenue {{ username.charAt(0).toUpperCase() + username.slice(1) }}&nbsp;!
      </h1>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <Temp :temperature="temperature" :unit="userPref.tempUnit" />
      <Humidity :humidity="humidityValue" />
      <Pressure :pressure="pressureValue" />
      <Outside :temperature="outsideTemperature" :unit="userPref.tempUnit" />
    </div>

    <div class="flex flex-col items-center gap-6">
      <select v-model="selectedPeriod" class="w-full max-w-xs">
        <option value="today">Aujourd’hui</option>
        <option value="thisWeek">Semaine en cours</option>
        <option value="fullMonth">Mois complet</option>
      </select>

      <DashboardChart v-model:selectedPeriod="selectedPeriod"
        class="w-full md:max-w-[1100px] 2xl:max-w-[1400px] mb-8 space-y-3" />
    </div>

    <ConnectedDevices />
  </div>
</template>
