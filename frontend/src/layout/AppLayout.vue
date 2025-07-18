<script setup>
import Sidebar from '@/layout/Sidebar.vue'
import Topbar from '@/layout/Topbar.vue'
</script>


<template>
  <div class="flex h-screen">
    <Sidebar />
    <div class="flex-1 flex flex-col">
      <Topbar />
      <main class="w-full p-4 flex-1 overflow-y-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>