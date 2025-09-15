<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import { fetchSensor } from '@/services/sensorService'

import Sensor1 from '../views/Datas/DataSensor1.vue'
import Sensor2 from '../views/Datas/DataSensor2.vue'
import Sensor3 from '../views/Datas/DataSensor3.vue'

import { useUserPrefStore } from '@/stores/userpref'

const isTelephone = useMediaQuery('(max-width: 768px)')
const selectedSensor = ref<'sensor1' | 'sensor2' | 'sensor3' | 'all'>('all')

const userPref = useUserPrefStore()

onMounted(async () => {
  await fetchSensor() 
})
</script>

<template>
  <div :class="[isTelephone ? 'p-2' : 'p-6']">

    <h1 class="title !mt-0 mb-6" :class="[ isTelephone ? 'flex justify-center' : '' ]">Données des capteurs</h1>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2 mb-3">
      <button
        @click="selectedSensor = 'all'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'all'
            ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
            : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Tous
      </button>

      <button
        @click="selectedSensor = 'sensor1'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'sensor1'
            ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
            : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        {{ userPref.sensor1name }}
      </button>

      <button
        @click="selectedSensor = 'sensor2'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'sensor2'
            ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
            : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        {{ userPref.sensor2name }}
      </button>

      <button
        @click="selectedSensor = 'sensor3'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'sensor3'
            ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
            : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        {{ userPref.sensor3name }}
      </button>
    </div>

    <Sensor1 v-if="selectedSensor === 'sensor1'" />
    <Sensor2 v-else-if="selectedSensor === 'sensor2'" />
    <Sensor3 v-else-if="selectedSensor === 'sensor3'" />
    <div v-else class="flex flex-col gap-3">
      <Sensor1 />
      <Sensor2 />
      <Sensor3 />
    </div>
  </div>
</template>
