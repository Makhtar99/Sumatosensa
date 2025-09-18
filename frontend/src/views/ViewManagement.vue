<script setup lang="ts">
import { ref } from 'vue'
import { useMediaQuery } from '@vueuse/core'

import ExportView from './ViewExport.vue' 
import HistoryView from './ViewHistory.vue'
import Gestion from './ViewGestionSensor.vue'

const selectedView = ref<'history' | 'export' | 'gestion'>('history')
const isTelephone = useMediaQuery('(max-width: 768px)')
</script>

<template>
  <div class="flex flex-col gap-4" :class="isTelephone ? 'p-4' : ''">
    
    <h1 class="flex justify-start !my-0 !p-0 text-center title">
      Gestion des données
    </h1>

    <div class="flex gap-4" :class="[ isTelephone ? 'justify-center' : '' ]">
      <button
        @click="selectedView = 'history'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedView === 'history'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Historique
      </button>
      <button
        @click="selectedView = 'export'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedView === 'export'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Exporter
      </button>
      <button
        @click="selectedView = 'gestion'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedView === 'gestion'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Capteurs
      </button>
    </div>

    <HistoryView v-if="selectedView === 'history'" />
    <ExportView v-else-if="selectedView === 'export'" />
    <Gestion v-else />
  </div>
</template>
