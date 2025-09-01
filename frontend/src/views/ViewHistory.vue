<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

import temperatureData from '../assets/json/temperature_data.json'
import humidityData from '../assets/json/humidity_data.json'
import pressureData from '../assets/json/pressure_data.json'

const tabs = ['Température', 'Humidité', 'Pression']
type TabName = typeof tabs[number]
const selectedTab = ref<TabName>('Température')

const places = ['Salon', 'Grenier', 'Cuisine']
const selectedPlace = ref('Salon')

const isTelephone = useMediaQuery('(max-width: 768px)')

const dataMap: Record<TabName, { date: string; room: string; value: number }[]> = {
  Température: temperatureData,
  Humidité: humidityData,
  Pression: pressureData,
}

const filteredData = computed(() => {
  return dataMap[selectedTab.value].filter(d => d.room === selectedPlace.value)
})
</script>

<template>
  <div :class="[isTelephone ? 'pt-6' : 'p-6']">
    <h2 class="title !mt-0 mb-6">Historique des données</h2>

    <div :class="[ isTelephone ? 'flex justify-around items-center pb-3 ' : 'flex justify-between items-center my-6' ]">
        <div :class="[ isTelephone ? 'flex flex-col gap-4' : 'flex flex-wrap gap-4' ]">
        <button
            v-for="tab in tabs"
            :key="tab"
            @click="selectedTab = tab"
            :class="[
            'px-4 py-2 rounded-lg font-medium transition',
            selectedTab === tab
                ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
                : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
            ]"
        >
            {{ tab }}
        </button>
        </div>
        <div :class="[ isTelephone ? 'flex flex-col gap-4' : 'flex flex-wrap gap-4' ]">
            <button
                v-for="place in places"
                :key="place"
                @click="selectedPlace = place"
                :class="[
                'px-4 py-2 rounded-lg font-medium transition',
                selectedPlace === place
                    ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
                    : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
                ]"
            >
                {{ place }}
            </button>
        </div>
    </div>



    <DataTable
      :value="filteredData"
      class="shadow rounded-xl bg-white"
      stripedRows
      paginator
      :rows="8"
      scrollable
    >
      <Column field="date" header="Date" />
      <Column field="room" header="Pièce" />
      <Column field="value" :header="selectedTab" />
    </DataTable>
  </div>
</template>