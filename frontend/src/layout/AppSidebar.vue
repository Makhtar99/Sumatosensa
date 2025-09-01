<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useMediaQuery } from '@vueuse/core'
import SidebarItem from './AppSidebarItem.vue'

import Home from '../assets/svg/home.svg'
import Config from '../assets/svg/configuration.svg'
import Export from '../assets/svg/export.svg'
import Devices from '../assets/svg/devices.svg'
import Notif from '../assets/svg/ph_bell.svg'

import ArrowLeft from '../assets/svg/ph_arrow-circle-left.svg'
import ArrowRight from '../assets/svg/ph_arrow-circle-right.svg'

const props = defineProps({ isSidebarCollapsed: Boolean })
const emit = defineEmits<{ (e: 'update:isSidebarCollapsed', value: boolean): void }>()
const toggle = () => emit('update:isSidebarCollapsed', !props.isSidebarCollapsed)

const isTelephone = useMediaQuery('(max-width: 768px)')

const sidebarWidthClass = computed(() => {
  // ⬅️ Pleine largeur en mobile, barre en bas
  if (isTelephone.value) return 'w-full h-[72px]'
  return props.isSidebarCollapsed ? 'md:w-[80px]' : 'md:w-[256px]'
})

const navClass = computed(() => {
  if (isTelephone.value) {
    // ⬅️ 5 colonnes de largeur égale
    return 'w-full h-full grid grid-cols-5 place-items-center px-2 bg-[var(--color-sumato-surface)]'
  }
  return 'flex-1 w-full px-4 space-y-2'
})
</script>

<template>
  <aside
    class="fixed z-50 bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] shadow-lg transition-all duration-300 ease-in-out"
    :class="[ sidebarWidthClass, isTelephone ? 'bottom-0 left-0 right-0' : 'top-0 left-0 h-screen overflow-y-auto' ]"
  >
    <!-- Bouton toggle (desktop only) -->
    <button
      @click="toggle"
      class="absolute top-4 right-2 w-8 h-8 rounded-full bg-[var(--color-primary)] text-[var(--color-sumato-text)] items-center justify-center hover:bg-sumato-primary-hover transition duration-200 hidden md:flex"
    >
      <img :src="props.isSidebarCollapsed ? ArrowRight : ArrowLeft" alt="Toggle" class="w-4 h-4" />
    </button>

    <!-- Logo/Title masqués en mobile -->
    <div class="pt-10 pb-6 px-4 mt-6 flex flex-col items-center space-y-1" :class="[isTelephone ? 'hidden' : '']">
      <RouterLink to="/" class="flex items-center space-x-2">
        <img
          src="../assets/img/Logo.png"
          alt="SumãtoSensã"
          :class="[props.isSidebarCollapsed ? 'w-12 h-12' : 'w-16 h-16']"
        />
      </RouterLink>
      <span v-if="!props.isSidebarCollapsed" class="text-lg font-bold hidden md:block">
        SumãtoSensã
      </span>
    </div>

    <!-- NAV -->
    <nav :class="navClass">
      <!-- En grid mobile, chaque item occupe 1/5 de largeur automatiquement -->
      <SidebarItem :icon="Home"    label="Maison"        to="/dashboard" />
      <SidebarItem :icon="Devices" label="Capteurs"      to="/sensors" />
      <SidebarItem :icon="Notif"   label="Notifications" to="/notifications" />
      <SidebarItem :icon="Export"  label="Gestion"       to="/management" />
      <SidebarItem :icon="Config"  label="Paramètres"    to="/settings" />
    </nav>

    <!-- Décor: caché en mobile -->
    <div class="absolute right-0 top-4 bottom-4 w-[3px] bg-sumato-connected-devices rounded hidden md:block"></div>
  </aside>
</template>
