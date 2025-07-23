<script setup lang="ts">

import { ref, onMounted } from 'vue'
import { apiService } from '../services/api'


import Temp from '../views/Datas/Temperature.vue'
import Humidity from '../views/Datas/Humidity.vue'
import Pressure from '../views/Datas/Pressure.vue'
import Outside from '../views/Datas/Outside.vue'
import ConnectedDevices from './Datas/ConnectedDevices.vue'

const isConnected = ref(false)
const username = ref(<String | null>(null))

onMounted(async () => {
    const token = localStorage.getItem('access_token')
    isConnected.value = !!token
  if (token) {
    try {
      const user = await apiService.getCurrentUser()
      username.value = user.username
      console.log("Utilisateur connecté :", user)
    } catch (error) {
      console.error("Impossible de récupérer l'utilisateur :", error)
    }
  } else {
    console.log("Aucune session utilisateur trouvée.")
  }
})
</script>

<template>
  <div class="grid grid-cols-1 xl:grid-cols-4 gap-6 p-6 w-full">
    <!-- Zone utilisateur + image -->
    <div class="xl:col-span-3 flex flex-col gap-6">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <h1 class="title">
          Bienvenue <span v-if="username"> {{ username }}</span> !
        </h1>
        <!-- <img src="../assets/svg/smart-house.png" alt="Maison connectée" class="hidden md:block w-64 h-64 object-contain" /> -->
      </div>

      <!-- Données -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Temp />
        <Humidity />
        <Pressure />
        <Outside />
      </div>
    </div>

    <!-- Appareils connectés -->
    <div class="h-fit">
      <ConnectedDevices />
    </div>
  </div>
</template>
