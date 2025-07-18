<script setup>
defineProps({
  icon: String,
  label: String,
  to: String
});
</script>

<template>
  <router-link :to="to" v-slot="{ isActive }">
    <div
      :class="[
        'sidebarItem flex items-center gap-3 p-3 rounded-2xl',
        isActive ? 'sidebar-is-active' : ''
      ]"
    >
      <img :src="icon" :alt="label" class="w-6 h-6" :class="isActive ? 'filter brightness-0 invert' : ''" />
      <span class="text-sm font-medium">{{ label }}</span>
    </div>
  </router-link>
</template>
