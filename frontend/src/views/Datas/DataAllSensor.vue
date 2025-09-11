<script setup lang="ts">
import { ref } from 'vue'

import Sensor1 from './DataSensor1.vue'
import Sensor2 from './DataSensor2.vue'
import Sensor3 from './DataSensor3.vue'

const selectedSensor = ref<'sensor1' | 'sensor2' | 'sensor3' | 'all'>('all')
</script>


<template>

  <div class="grid grid-cols-2 md:grid-cols-4 gap-2 mb-3">
        
    <button
      @click="selectedSensor = 'all'"
      :class="[
        'px-4 py-2 rounded-lg font-medium transition-all',
        selectedSensor === 'all'
          ? 'bg-[var(--color-primary)]'
          : 'hover:bg-[var(--color-sumato-light)]',
      ]"
    >
      Tous
    </button>

    <button
      @click="selectedSensor = 'sensor1'"
      :class="[
        'px-4 py-2 rounded-lg font-medium transition-all',
        selectedSensor === 'sensor1'
          ? 'bg-[var(--color-primary)]'
          : 'hover:bg-[var(--color-sumato-light)]',
      ]"
    >
      Salon
    </button>

    <button
      @click="selectedSensor = 'sensor2'"
      :class="[
        'px-4 py-2 rounded-lg font-medium transition-all',
        selectedSensor === 'sensor2'
          ? 'bg-[var(--color-primary)]'
          : 'hover:bg-[var(--color-sumato-light)]',
      ]"
    >
      Chambre parentale
    </button>

    <button
      @click="selectedSensor = 'sensor3'"
      :class="[
        'px-4 py-2 rounded-lg font-medium transition-all',
        selectedSensor === 'sensor3'
          ? 'bg-[var(--color-primary)]'
          : 'hover:bg-[var(--color-sumato-light)]',
      ]"
    >
      Grenier
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

</template>