<script setup lang="ts">
import { ref, computed } from 'vue'
import Sidebar from './AppSidebar.vue'
import Topbar from './AppTopbar.vue'

import { useMediaQuery } from '@vueuse/core'

const isSidebarCollapsed = ref(false)

const isTelephone = useMediaQuery('(max-width: 768px)')

const contentMargin = computed(() => {
  if (isTelephone.value) return 'ml-[80px]'
  return isSidebarCollapsed.value ? 'ml-[80px]' : 'ml-[256px]'
})

</script>

<template>
  <div class="flex h-screen bg-[var(--color-sumato-surface)] transition-colors duration-300">
    <Sidebar v-model:isSidebarCollapsed="isSidebarCollapsed" />
    />

    <div
      class="flex-1 flex flex-col bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] transition-all duration-300 ease-in-out"
      :class="contentMargin"
    >
      <Topbar />

      <main class="flex-1 overflow-y-auto max-h-full" :class="[isTelephone ? 'p-0' : 'p-4 w-full']">
        <RouterView />
      </main>
    </div>
  </div>
</template>
