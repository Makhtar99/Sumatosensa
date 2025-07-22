<script setup lang="ts">

import { ref, onMounted } from 'vue'
import { apiService } from '../services/api'

const isConnected = ref(false)
const username = ref(<String | null>(null))


onMounted(async () => {
    const token = localStorage.getItem('access_token')
    isConnected.value = !!token
    console.log("État de la connexion :", isConnected.value)
    
  if (token) {
    try {
      const user = await apiService.getCurrentUser()
      username.value = user.username
      console.log("👤 Utilisateur connecté :", user)
    } catch (error) {
      console.error("❌ Impossible de récupérer l'utilisateur :", error)
    }
  } else {
    console.log("🔒 Aucune session utilisateur trouvée.")
  }
})



import Temp from '../views/Datas/Temperature.vue'
import Humidity from '../views/Datas/Humidity.vue'
import Pressure from '../views/Datas/Pressure.vue'
import Outside from '../views/Datas/Outside.vue'
import ConnectedDevices from './Datas/ConnectedDevices.vue'
</script>

<template>
    <div class="flex gap-5">
        <div class="flex flex-col">
            <h1 class="text-2xl font-bold" style="margin: 0; padding: 0;">Bienvenue <span v-if="username"> {{ username }}</span> !</h1>
            <div>
                <img src="../assets/img/house.png" alt="mézon" style="width: 90%; height: 300px; margin-left: 20px; margin-top: 20px;" />
            </div>
            <div class="dashboard_data">
                <Temp />
                <Humidity />
                <Pressure />
                <Outside />
            </div>
        </div>
        <div class="flex flex-col justify-between" style="width: 20%; margin: auto;">
            <ConnectedDevices />
        </div>
    </div>
</template>