<script setup lang="ts">
import { computed } from 'vue'
import { formatedTimestamp } from '@/assets/functions/FormatedDate'
import { useMediaQuery } from '@vueuse/core'
import { useUserPrefStore } from '@/stores/userpref'

const props = defineProps<{
  piece: string
  location: string
  temperature: number
  humidite: number
  pression: number
  batterie: number
  lastUpdate?: string
  status: string
  messageAlert?: string
}>()

const isTelephone = useMediaQuery('(max-width: 640px)')
const userPref = useUserPrefStore()

const displayTemperature = computed(() => {
  return userPref.tempUnit === 'Fahrenheit'
    ? Math.round((props.temperature * 9) / 5 + 32)
    : Math.round(props.temperature)
})
const displayPressure = computed(() => {
  switch (userPref.pressureUnit) {
    case 'inHg':
      return Number((props.pression * 0.02953).toFixed(2))
    case 'bar':
      return (props.pression / 1000).toFixed(2) // 1 bar = 1000 hPa
    default:
      return Math.round(props.pression)
  }
})
</script>

<template>
  <div class="bg-[var(--color-surface)] border rounded-xl p-6 space-y-4">
    <h2 class="text-lg !mt-0 font-semibold">{{ piece }}</h2>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="text-center">
        <p class="text-2xl font-bold text-[var(--color-sumato-primary)]">
          {{ displayTemperature }}°{{ userPref.tempUnit === 'Fahrenheit' ? 'F' : 'C' }}
        </p>
        <span class="text-sm opacity-70">Température</span>
      </div>

      <div class="text-center">
        <p class="text-2xl font-bold text-blue-600">
          {{ Math.round(humidite) }}%
        </p>
        <span class="text-sm opacity-70">Humidité</span>
      </div>

      <div class="text-center">
        <p class="text-2xl font-bold text-indigo-600">
          {{ displayPressure }} {{ userPref.pressureUnit }}
        </p>
        <span class="text-sm opacity-70">Pression</span>
      </div>

      <div class="text-center">
        <p
          :class="[
            'text-2xl font-bold',
            batterie > 50
              ? 'text-green-600'
              : batterie > 20
              ? 'text-yellow-600'
              : 'text-[var(--color-sumato-danger)]'
          ]"
        >
          {{ batterie }}%
        </p>
        <span class="text-sm opacity-70">Batterie</span>
      </div>
    </div>
    <div class="flex justify-between items-center mt-4 text-sm text-gray-600">
      <span
        :class="{
          '!text-green-600': status === 'Connecté',
          '!text-yellow-600': status === 'Batterie faible',
          '!text-[var(--color-sumato-danger)]': status === 'Hors ligne'
        }"
        class="font-medium"
      >
        ● {{ status }}
      </span>

      <span v-if="messageAlert" class="!text-[var(--color-sumato-danger)] font-bold">
        ⚠️ {{ messageAlert }}
      </span>

      <span class="text-gray-500">
        {{ lastUpdate ? (isTelephone ? formatedTimestamp(lastUpdate) : 'Mise à jour : ' + formatedTimestamp(lastUpdate)) : '' }}
      </span>
    </div>
  </div>
</template>
