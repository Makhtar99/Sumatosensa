<script setup>
import SidebarItem from './SidebarItem.vue'

import Dashboard from '../assets/svg/dashboard.svg'
import Config from '../assets/svg/configuration.svg'
import Export from '../assets/svg/export.svg'
import WhiteBoard from '../assets/svg/whiteboard.svg'
import Restaurant from '../assets/svg/restaurant.svg'
import Meeting from '../assets/svg/meeting.svg'
</script>


<template>
  <aside class="flex flex-col items-center bg-color-background text-color-black h-screen border-r border-r-red">

    <div class="flex flex-col m-auto justify-center items-center py-4">
      <router-link to="/" class="text-2xl font-bold text-color-red">
        <img src="../assets/img/Logo.png" alt="SumãtoSensã Logo" class="w-16 h-16 mb-2 ">
      </router-link>
      <span class="font-bold">SumãtoSensã</span>
    </div>

    <nav class="flex flex-col px-4 py-4 space-y-2">
      <SidebarItem :icon="Dashboard" label="Dashboard" to="/" />
      <SidebarItem :icon="Export" label="Export" to="/export" />
      <SidebarItem :icon="Config" label="Paramètres" to="/config" />
      <SidebarItem :icon="WhiteBoard" label="Amphithéatre" to="/whiteboard" />
      <SidebarItem :icon="Restaurant" label="salle de Restauration" to="/restaurant" />
      <SidebarItem :icon="Meeting" label="Salle de Réunions" to="/meeting" />
    </nav>
  </aside>
</template>