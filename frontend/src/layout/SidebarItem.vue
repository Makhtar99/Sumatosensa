<template>
  <router-link
    :to="to"
    class="flex items-center gap-3 px-3 py-2 rounded hover:bg-gray-800 transition"
    active-class="bg-gray-800"
  >
    <span class="text-xl">{{ icon }}</span>
    <span class="text-sm font-medium">{{ label }}</span>
  </router-link>
</template>

<script setup>
defineProps({
  icon: String,
  label: String,
  to: String
})
</script>
