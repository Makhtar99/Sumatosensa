<script setup>
import { ref, provide } from 'vue'
import Sidebar from '@/layout/Sidebar.vue'
import Topbar from '@/layout/Topbar.vue'

const isSidebarCollapsed = ref(false)
provide('isSidebarCollapsed', isSidebarCollapsed)
</script>

<template>
  <div class="flex h-screen">
    <Sidebar :isSidebarCollapsed="isSidebarCollapsed" @toggleSidebar="isSidebarCollapsed = !isSidebarCollapsed" />
    
    <div class="flex-1 flex flex-col transition-all duration-300 ease-in-out"
         :class="[isSidebarCollapsed ? 'ml-27' : 'ml-66']">
      <Topbar />

      <main class="w-full p-4 flex-1 overflow-y-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
