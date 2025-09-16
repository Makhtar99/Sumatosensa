<script setup lang="ts">
import { onMounted } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import { fetchSensor } from '@/services/sensorService'

import Data from '../views/Datas/DataAllSensor.vue'
const isTelephone = useMediaQuery('(max-width: 768px)')

onMounted(async () => {
  await fetchSensor() 
})
</script>

<template>
  <div class="flex flex-col gap-4" :class="[isTelephone ? 'p-4' : '']">
    <h1 class="flex justify-start !my-0 !p-0 text-center title">
      Données des capteurs
    </h1>


    <div :class="[ isTelephone ? '' : 'p-2' ]">
      <Data />
    </div>
  </div>
</template>
