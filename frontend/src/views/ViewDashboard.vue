<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService } from '../services/api'

import Temp from './Datas/DataTemperature.vue'
import Humidity from './Datas/DataHumidity.vue'
import Pressure from './Datas/DataPressure.vue'
import Outside from './Datas/DataOutside.vue'
import ConnectedDevices from './Datas/DataConnectedDevices.vue'

const isConnected = ref(false)
const username = ref(<string | null>null)

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  isConnected.value = !!token
  if (!token) {
    console.log('Aucune session utilisateur trouvée.')
    return
  } else {
    try {
      const user = await apiService.getCurrentUser()
      username.value = user.username
      console.log('Utilisateur connecté :', user)
    } catch (error) {
      console.error("Impossible de récupérer l'utilisateur :", error)
    }
  }
})
</script>

<template>
  <div class="grid grid-cols-1 xl:grid-cols-4 gap-6 p-6 w-full">
    <div class="xl:col-span-3 flex flex-col gap-6">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <h1 class="title">
          Bienvenue <span v-if="username"> {{ username }}</span> !
        </h1>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Temp />
        <Humidity />
        <Pressure />
        <Outside />
      </div>
    </div>

    <div class="h-fit">
      <ConnectedDevices />
    </div>
  </div>
</template>
