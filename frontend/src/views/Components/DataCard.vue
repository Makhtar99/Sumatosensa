<script setup lang="ts">
import { formatedTimestamp } from '@/assets/functions/FormatedDate'
import { useMediaQuery } from '@vueuse/core'

const isTelephone = useMediaQuery('(max-width: 640px)')

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
  <div class="p-2 rounded-xl" :style="{ backgroundColor: color }">
    <div class="flex flex-col items-center gap-4 justify-between">
      <img :src="icon" alt="Icon" class="w-25 h-25 object-contain" />
      <div class="text-center">
        <h2 class="font-bold !text-4xl !p-0 !m-0">{{ value }} {{ unit }}</h2>
      </div>
      <div>
        <h4 class="text-lg font-semibold !m-0">{{ title }}</h4>
      </div>
      <div>
        <p v-if="timestamp"> {{ isTelephone ? '' : 'Mise à jour :' }} {{ formatedTimestamp(timestamp) }}</p>
      </div>
    </div>
  </div>
</template>
