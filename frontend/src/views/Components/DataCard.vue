<script setup lang="ts">
defineProps<{
  title: string
  icon: string
  value: string | number
  unit: string
  timestamp?: string
  color?: string
}>()
</script>

<template>
  <div class="p-2 rounded-xl text-white hover:transform hover:translate-y-[-2px] hover:shadow-lg" :style="{ backgroundColor: color || 'var(--color-sumato-comfort)' }">
    <div class="flex flex-col items-center gap-4">
      <img :src="icon" alt="Icon" class="w-25 h-25 object-contain" />
      <div class="text-center">
        <h4 class="text-lg font-semibold">{{ title }}</h4>
        <p class="text-2xl font-bold">{{ value }} {{ unit }}</p>
        <p v-if="timestamp" class="text-xs text-white/80">Maj: {{ timestamp }}</p>
      </div>
    </div>
  </div>
</template>
