<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SidebarItem from './SidebarItem.vue'
import { apiService } from '@/services/api'

import Home from '../assets/svg/home.svg'
import Config from '../assets/svg/configuration.svg'
import Export from '../assets/svg/export.svg'
import Devices from '../assets/svg/devices.svg'
import History from '../assets/svg/history.svg'
import Management from '../assets/svg/management.svg'
import Alertes from '../assets/svg/alert.svg'
import Notif from '../assets/svg/ph_bell.svg'
import Energie from '../assets/svg/energy.svg'

import ArrowLeft from '../assets/svg/ph_arrow-circle-left.svg'
import ArrowRight from '../assets/svg/ph_arrow-circle-right.svg'

const props = defineProps({
  isSidebarCollapsed: Boolean
})
const emit = defineEmits(['toggleSidebar'])

const isAdmin = ref(false)
onMounted(async () => {
  isAdmin.value = await apiService.isAdmin()
})
</script>

<template>
  <aside
    class="fixed top-0 left-0 z-50 h-screen bg-white shadow-lg transition-all duration-300 ease-in-out"
    :class="[isSidebarCollapsed ? 'w-25' : 'w-64']"
  >
    <div class="py-6 px-4 flex flex-col items-center space-y-1">
      <img src="../assets/img/Logo.png" alt="SumãtoSensã" class="w-16 h-16" />
      <span v-if="!isSidebarCollapsed" class="text-lg font-bold hidden md:block">SumãtoSensã</span>
    </div>
    
    <button
      @click="emit('toggleSidebar')"
      class="absolute top-4 right-4 w-8 h-8 rounded-full bg-sumato-primary text-white flex items-center justify-center hover:bg-sumato-primary-hover transition"
    >
      <img v-if="isSidebarCollapsed" :src="ArrowRight" alt="Arrow Right" class="w-4 h-4" />
      <img v-else :src="ArrowLeft" alt="Arrow Left" class="w-4 h-4" />
    </button>

    <nav class="flex-1 w-full px-4 space-y-2">
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

    <div class="absolute right-0 top-4 bottom-4 w-[3px] bg-sumato-connected-devices rounded"></div>
  </aside>
</template>
