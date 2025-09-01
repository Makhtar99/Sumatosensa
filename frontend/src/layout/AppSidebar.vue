<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
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
import WhiteArrowLeft from '../assets/svg/white-arrow-left.svg'
import WhiteArrowRight from '../assets/svg/white-arrow-right.svg'

const props = defineProps({ isSidebarCollapsed: Boolean })
const emit = defineEmits<{ (e: 'update:isSidebarCollapsed', value: boolean): void }>()
const toggle = () => emit('update:isSidebarCollapsed', !props.isSidebarCollapsed)

const isTelephone = useMediaQuery('(max-width: 768px)')

const isDark = ref(false)
const readTheme = () => document.documentElement.getAttribute('data-theme') === 'dark'

let themeObserver: MutationObserver | null = null
onMounted(() => {
  isDark.value = readTheme()
  themeObserver = new MutationObserver((m) => {
    if (m.some(x => x.attributeName === 'data-theme')) {
      isDark.value = readTheme()
    }
  })
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })
})
onBeforeUnmount(() => themeObserver?.disconnect())

const arrowLeftSrc = computed(() => (isDark.value ? WhiteArrowLeft : ArrowLeft))
const arrowRightSrc = computed(() => (isDark.value ? WhiteArrowRight : ArrowRight))

const sidebarWidthClass = computed(() => {
  if (isTelephone.value) return 'w-full h-[80px]'
  return props.isSidebarCollapsed ? 'md:w-[80px]' : 'md:w-[256px]'
})

const navClass = computed(() => {
  if (isTelephone.value) {
    return 'w-full h-full grid grid-cols-5 place-items-center px-2 bg-[var(--color-sumato-surface)]'
  }
  return 'flex-1 w-full px-4 space-y-2'
})

const param = computed(() => (isTelephone.value ? 'Param' : 'Paramètres'))
</script>

<template>
  <aside
    class="fixed z-50 bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] shadow-lg transition-all duration-300 ease-in-out"
    :class="[ sidebarWidthClass, isTelephone ? 'bottom-0 left-0 right-0' : 'top-0 left-0 h-screen overflow-y-auto' ]"
  >
    <button
      @click="toggle"
      class="absolute top-4 right-2 w-8 h-8 rounded-full items-center justify-center hover:bg-sumato-primary-hover transition duration-200 hidden md:flex"
    >
      <img :src="props.isSidebarCollapsed ? arrowRightSrc : arrowLeftSrc" alt="Toggle" class="w-4 h-4" />
    </button>

    <div class="pt-10 pb-6 px-4 mt-6 flex flex-col items-center space-y-1" :class="[isTelephone ? 'hidden' : '']">
      <RouterLink to="/" class="flex items-center space-x-2">
        <img
          src="../assets/img/Logo.png"
          alt="SumãtoSensã"
          :class="[props.isSidebarCollapsed ? 'w-12 h-12' : 'w-16 h-16']"
        />
      </RouterLink>
      <span v-if="!props.isSidebarCollapsed" class="text-lg font-bold hidden md:block">SumãtoSensã</span>
    </div>

    <nav :class="navClass">
      <SidebarItem :icon="Home"    label="Maison"        to="/dashboard" />
      <SidebarItem :icon="Devices" label="Capteurs"      to="/sensors" />
      <SidebarItem :icon="Notif"   label="Alertes"       to="/notifications" />
      <SidebarItem :icon="Export"  label="Gestion"       to="/management" />
      <SidebarItem :icon="Config"  :label="param"        to="/settings" />
    </nav>

    <div class="absolute right-0 top-4 bottom-4 w-[3px] bg-sumato-connected-devices rounded hidden md:block" :class="[ isTelephone ? 'flex-col' : '' ]">
      <ConnectedDeviceCard />
      <ConnectedDeviceCard />
      <ConnectedDeviceCard />
      <ConnectedDeviceCard />
    </div>
  </aside>
</template>