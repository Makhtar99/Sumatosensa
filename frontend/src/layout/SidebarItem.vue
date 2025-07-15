<script setup>
defineProps({
  icon: String,
  label: String,
  to: String
})
</script>

<template>
  <router-link
    :to="to"
    class="flex items-center gap-3 p-3 rounded-2xl hover:text-white transition"
    active-class=""
  >
    <img :src=icon :alt="label" style="color: white;">
    <span class="text-sm font-medium">{{ label }}</span>
  </router-link>
</template>

<style scoped>  
.sidebarItem:hover {
  background: var(--color-red);
  color: var(--color-white);
}
</style>