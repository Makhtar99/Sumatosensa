<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SidebarItem from './SidebarItem.vue'
import {apiService } from '@/services/api'

import Home from '../assets/svg/home.svg'
import Config from '../assets/svg/configuration.svg'
import Export from '../assets/svg/export.svg'
import Devices from '../assets/svg/devices.svg'
import History from '../assets/svg/history.svg'
import Management from '../assets/svg/management.svg'
import Alertes from '../assets/svg/alerts.png'
import Notif from '../assets/svg/notif.png'
import Energie from '../assets/svg/energy.png'

const isAdmin = ref(false)
onMounted(async () => {
  isAdmin.value = await apiService.isAdmin();
  // console.log("État de l'admin :", isAdmin.value);
});

</script>

<template>
  <aside class="relative flex flex-col items-center bg-color-background text-color-black h-screen" >

    
    <div class="flex flex-col m-auto justify-center items-center py-4">
      <img src="../assets/img/Logo.png" alt="SumãtoSensã Logo" style="width: 100px; height: 100px;" />
      <span class="font-bold">SumãtoSensã</span>
    </div>

    <nav class="flex flex-col px-4 py-4 space-y-2">
      <SidebarItem :icon="Home" label="Ma Maison" to="/" />
      <SidebarItem :icon="History" label="Historique" to="/history" />
      <SidebarItem :icon="Devices" label="Mes capteurs" to="/devices" />
      <SidebarItem :icon="Export" label="Export" to="/export" />
      <SidebarItem :icon="Alertes" label="Alertes" to="/alerts" />
      <SidebarItem :icon="Notif" label="Notifications" to="/notifications" />
      <SidebarItem :icon="Config" label="Paramètres" to="/settings" />
      <SidebarItem :icon="Energie" label="Énergie" to="/energy" />
      <SidebarItem v-if="isAdmin" :icon="Management" label="Gestion" to="/management" />

    </nav>

    <div class="absolute right-0 top-1/2 transform -translate-y-1/2 h-[95%] w-[4px] rounded" style="border-right: 2px solid var(--color-sumato-connected-devices)"></div>
  </aside>
</template>
