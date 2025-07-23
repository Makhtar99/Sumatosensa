<script setup lang="ts">
import { ref, computed } from 'vue'
import { saveAs } from 'file-saver'
import * as XLSX from 'xlsx'
import { Chart, registerables } from 'chart.js'
import { Line } from 'vue-chartjs'


Chart.register(...registerables)

import temperatureData from '../assets/json/temperature_data.json'
import humidityData from '../assets/json/humidity_data.json'
import pressureData from '../assets/json/pressure_data.json'

const tabs = ['Température', 'Humidité', 'Pression'] as const
type TabName = typeof tabs[number]
const selectedTab = ref<TabName>('Température')
const places = ['Salon', 'Grenier', 'Cuisine']
const selectedPlace = ref('Salon')

const dataMap: Record<TabName, { date: string; room: string; value: number }[]> = {
  Température: temperatureData,
  Humidité: humidityData,
  Pression: pressureData,
}

const filteredData = computed(() => {
  return dataMap[selectedTab.value].filter(d => d.room === selectedPlace.value)
})

function exportToCSV(dataset: any[], name: string) {
  if (!dataset.length) return
  const csv = [
    Object.keys(dataset[0]).join(','),
    ...dataset.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  saveAs(blob, `${name}.csv`)
}

function exportToExcel(dataset: any[], name: string) {
  const worksheet = XLSX.utils.json_to_sheet(dataset)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')
  const blob = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
  saveAs(new Blob([blob]), `${name}.xlsx`)
}
</script>

<template>
  <div class="p-6">
    <h1 class="title">📦 Export de données</h1>

    <div class="flex flex-col gap-4 my-6">
      <div class="flex justify-between">
        <div class="flex gap-4">
          <button
            v-for="tab in tabs"
            :key="tab"
            @click="selectedTab = tab"
            :class="[
              'px-4 py-2 rounded-lg font-medium',
              selectedTab === tab
                ? 'bg-[var(--color-primary)] text-white'
                : 'bg-[var(--color-sumato-border)] text-[var(--color-text)]'
            ]"
          >
            {{ tab }}
          </button>
        </div>
        <div class="flex gap-4 justify-end">
          <button
            class="px-4 py-2 bg-[var(--color-sumato-primary)] text-white rounded-lg hover:bg-[var(--color-sumato-primary-hover)]"
            @click="exportToCSV(filteredData, selectedTab + '_' + selectedPlace + '_export')"
          >
            Exporter CSV
          </button>
          <button
            class="px-4 py-2 bg-[var(--color-sumato-primary)] text-white rounded-lg hover:bg-[var(--color-sumato-primary-hover)]"
            @click="exportToExcel(filteredData, selectedTab + '_' + selectedPlace + '_export')"
          >
            Exporter Excel
          </button>
        </div>
      </div>

      <div class="flex gap-4">
        <button
          v-for="place in places"
          :key="place"
          @click="selectedPlace = place"
          :class="[
            'px-4 py-2 rounded-lg font-medium',
            selectedPlace === place
              ? 'bg-[var(--color-primary)] text-white'
              : 'bg-[var(--color-sumato-border)] text-[var(--color-text)]'
          ]"
        >
          {{ place }}
        </button>
      </div>

    </div>

    <div class="bg-white shadow rounded-xl p-6">
      <div class="mb-6">
        <Line
          :data="{
            labels: filteredData.map(d => d.date),
            datasets: [{
              label: `${selectedTab} - ${selectedPlace}`,
              data: filteredData.map(d => d.value),
              borderColor: 'var(--color-sumato-primary-hover)',
              backgroundColor: 'rgba(59, 130, 246, 0.3)',
              fill: true,
              tension: 0.3
            }]
          }"
          :options="{ responsive: true, maintainAspectRatio: false }"
          style="height: 300px;"
        />
      </div>
    </div>
  </div>
</template>
