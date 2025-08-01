<script setup>
import { ref, provide, computed } from 'vue'
import Sidebar from '@/layout/Sidebar.vue'
import Topbar from '@/layout/Topbar.vue'

import { useMediaQuery } from '@vueuse/core'

const isSidebarCollapsed = ref(false)
provide('isSidebarCollapsed', isSidebarCollapsed)
const isTelephone = useMediaQuery('(max-width: 768px)')

const contentMargin = computed(() => {
  if (isTelephone.value) return 'ml-[80px]'
  return isSidebarCollapsed.value ? 'ml-[80px]' : 'ml-66'
})

</script>

<template>
  <div class="flex h-screen">
    <Sidebar
      :isSidebarCollapsed="isSidebarCollapsed"
      @toggleSidebar="isSidebarCollapsed = !isSidebarCollapsed"
    />

    <div
      class="flex-1 flex flex-col transition-all duration-300 ease-in-out"
      :class="contentMargin"
    >
      <Topbar />

      <main class="w-full p-4 flex-1 overflow-y-auto max-h-full">
        <RouterView />
      </main>
    </div>
  </div>
</template>
