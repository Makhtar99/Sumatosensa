<script setup>
import SidebarItem from './SidebarItem.vue'

import Home from '../assets/svg/home.svg'
import Config from '../assets/svg/configuration.svg'
import Export from '../assets/svg/export.svg'
import Devices from '../assets/svg/devices.svg'
import History from '../assets/svg/history.svg'
import Management from '../assets/svg/management.svg'
</script>

<template>
  <aside class="flex flex-col items-center bg-color-background text-color-black h-screen border-r border-r-red">

    <div class="flex flex-col m-auto justify-center items-center py-4">
      <img src="../assets/img/Logo.png" alt="SumãtoSensã Logo" class="w-16 h-16 mb-2 ">
      <span class="font-bold">SumãtoSensã</span>
    </div>

    <nav class="flex flex-col px-4 py-4 space-y-2">
      <SidebarItem :icon="Home" label="Home" to="/" />
      <SidebarItem :icon="History" label="History" to="/history" />
      <SidebarItem :icon="Devices" label="Devices" to="/devices" />
      <SidebarItem :icon="Management" label="Management" to="/management" />
      <SidebarItem :icon="Export" label="Export" to="/exort" />
      <SidebarItem :icon="Config" label="Settings" to="/settings" />

    </nav>
  </aside>
</template>
