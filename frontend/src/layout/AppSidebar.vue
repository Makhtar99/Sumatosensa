<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useMediaQuery } from '@vueuse/core'
import SidebarItem from './AppSidebarItem.vue'

import Home from '../assets/svg/home.svg'
import Config from '../assets/svg/configuration.svg'
import Export from '../assets/svg/export.svg'
import Devices from '../assets/svg/devices.svg'
import Notif from '../assets/svg/ph_bell.svg'
import Energie from '../assets/svg/energy.svg'

import ArrowLeft from '../assets/svg/ph_arrow-circle-left.svg'
import ArrowRight from '../assets/svg/ph_arrow-circle-right.svg'

const props = defineProps({
  isSidebarCollapsed: Boolean
})
const emit = defineEmits(['toggleSidebar'])

const isTelephone = useMediaQuery('(max-width: 768px)')

const sidebarWidthClass = computed(() => {
  if (isTelephone.value) return 'w-[80px]'
  return props.isSidebarCollapsed ? 'md:w-[80px]' : 'md:w-[256px]'
})
</script>

<template>
  <aside
    class="fixed top-0 left-0 z-50 h-screen bg-[var(--color-surface)] text-[var(--color-sumato-text)] shadow-lg transition-all duration-300 ease-in-out overflow-y-auto"
    :class="sidebarWidthClass"
  >

  <button
      @click="emit('toggleSidebar')"
      class="absolute top-4 right-2 w-8 h-8 rounded-full bg-[var(--color-primary)] text-[var(--color-sumato-text)] items-center justify-center hover:bg-sumato-primary-hover transition duration-200 hidden md:flex"
    >
      <img :src="props.isSidebarCollapsed ? ArrowRight : ArrowLeft" alt="Toggle" class="w-4 h-4" />
    </button>

    <div class="pt-10 pb-6 px-4 mt-6 flex flex-col items-center space-y-1">
      <RouterLink to="/" class="flex items-center space-x-2">
        <img
          src="../assets/img/Logo.png"
          alt="SumãtoSensã"
          :class="[props.isSidebarCollapsed ? 'w-12 h-12' : 'w-16 h-16']"
        />
      </RouterLink>
      <span
        v-if="!props.isSidebarCollapsed && !isTelephone"
        class="text-lg font-bold hidden md:block"
      >
        SumãtoSensã
      </span>
    </div>

    <nav class="flex-1 w-full px-4 space-y-2">
      <SidebarItem :icon="Home" label="Ma Maison" to="/" />
      <SidebarItem :icon="Devices" label="Mes capteurs" to="/devices" />
      <SidebarItem :icon="Notif" label="Notifications" to="/notifications" />
      <SidebarItem :icon="Config" label="Paramètres" to="/settings" />
      <SidebarItem :icon="Energie" label="Énergie" to="/energy" />
      <SidebarItem :icon="Export" label="Gestion" to="/management" />
    </nav>

    <div class="absolute right-0 top-4 bottom-4 w-[3px] bg-sumato-connected-devices rounded"></div>
  </aside>
</template>