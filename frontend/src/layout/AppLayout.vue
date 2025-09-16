<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import Sidebar from './AppSidebar.vue'
import Topbar from './AppTopbar.vue'
import Footer from './AppFooter.vue'

const isSidebarCollapsed = ref(false)
const isTelephone = useMediaQuery('(max-width: 768px)')

const contentMargin = computed(() => {
  if (isTelephone.value) return 'ml-[0px]'
  return isSidebarCollapsed.value ? 'ml-[76px]' : 'ml-[256px]'
})

</script>

<template>
  <div class="flex h-screen transition-colors duration-300 max-w-full overflow-hidden">
    <Sidebar v-model:isSidebarCollapsed="isSidebarCollapsed" />

    <div
      class="flex-1 flex flex-col transition-all duration-300 ease-in-out"
      :class="[contentMargin, { 'overflow-y-auto mb-[76px]': isTelephone }]"
    >
      <Topbar />

      <main class="flex-1 overflow-y-scroll mb-10 max-h-full max-w-full" :class="[isTelephone ? 'p-0' : 'p-4 w-full']">
        <RouterView />
      </main>
    </div>
    <Footer class="fixed bottom-0" />
  </div>
</template>
