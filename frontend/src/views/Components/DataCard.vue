<script setup lang="ts">
import { formatedTimestamp } from '@/assets/functions/FormatedDate'
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
  <div class="p-2 rounded-xl text-[var(--text-color)]" :style="{ backgroundColor: color }">
    <div class="flex flex-col items-center gap-4">
      <img :src="icon" alt="Icon" class="w-25 h-25 object-contain" />
      <div class="text-center">
        <h4 class="text-lg font-semibold">{{ title }}</h4>
        <h5 class="font-bold">{{ value }} {{ unit }}</h5>
        <h6 v-if="timestamp" class="text-[var(--text-color)]">Mise à jour : {{ formatedTimestamp(timestamp) }}</h6>
      </div>
    </div>
  </div>
</template>
