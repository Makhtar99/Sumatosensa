<script setup lang="ts">
import { ref, computed } from 'vue'

import { Chart, registerables } from 'chart.js'
import { Line } from 'vue-chartjs'

import { exportToCSV } from '../assets/functions/ExportSCV'
import { exportToExcel } from '../assets/functions/ExportExcel'

Chart.register(...registerables)

import temperatureData from '../assets/json/temperature_data.json'
import humidityData from '../assets/json/humidity_data.json'
import pressureData from '../assets/json/pressure_data.json'

const tabs = ['Température', 'Humidité', 'Pression'] as const
type TabName = (typeof tabs)[number]
const selectedTab = ref<TabName>('Température')
const places = ['Salon', 'Grenier', 'Cuisine']
const selectedPlace = ref('Salon')

const dataMap: Record<TabName, { date: string; room: string; value: number }[]> = {
  Température: temperatureData,
  Humidité: humidityData,
  Pression: pressureData,
}

const selectedTimeFilter = ref('all')

function matchesTimeFilter(dateString: string): boolean {
  const date = new Date(dateString)
  const hour = date.getHours()
  const day = date.getDay() // 0 = dimanche, 6 = samedi

  switch (selectedTimeFilter.value) {
    case 'morning':
      return hour >= 6 && hour < 12
    case 'afternoon':
      return hour >= 12 && hour < 18
    case 'evening':
      return hour >= 18 && hour < 24
    case 'night':
      return hour >= 0 && hour < 6
    case 'weekday':
      return day >= 1 && day <= 5
    case 'weekend':
      return day === 0 || day === 6
    default:
      return true
  }
}

const filteredData = computed(() => {
  return dataMap[selectedTab.value].filter(
    (d) => d.room === selectedPlace.value && matchesTimeFilter(d.date),
  )
})
</script>

<template>
  <div class="p-6">
    <h2 class="title !mt-0 mb-6">Export de données</h2>

    <div class="flex flex-col gap-4 my-6">
      <div class="flex flex-col gap-6 justify-between">
        <div class="flex justify-between">
          <div class="flex gap-4">
            <label class="text-[var(--color-sumato-text)] font-medium">Filtrer par :</label>
            <select
              v-model="selectedTimeFilter"
              class="border border-[var(--color-sumato-border)] rounded-lg px-3 py-1"
            >
              <option value="all">Tous</option>
              <option value="morning">Matin (6h–12h)</option>
              <option value="afternoon">Après-midi (12h–18h)</option>
              <option value="evening">Soirée (18h–00h)</option>
              <option value="night">Nuit (00h–6h)</option>
              <option value="weekday">Semaine (lun–ven)</option>
              <option value="weekend">Week-end (sam–dim)</option>
            </select>
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
            v-for="tab in tabs"
            :key="tab"
            @click="selectedTab = tab"
            :class="[
              'px-4 py-2 rounded-lg font-medium',
              selectedTab === tab
                ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
                : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]',
            ]"
          >
            {{ tab }}
          </button>
        </div>
        <div class="flex gap-4">
          <button
            v-for="place in places"
            :key="place"
            @click="selectedPlace = place"
            :class="[
              'px-4 py-2 rounded-lg font-medium',
              selectedPlace === place
                ? 'bg-[var(--color-primary)] text-[var(--color-sumato-text)]'
                : 'bg-[var(--color-sumato-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]',
            ]"
          >
            {{ place }}
          </button>
        </div>
      </div>
    </div>

    <div class="bg-white shadow rounded-xl p-6">
      <div class="mb-6">
        <Line
          :data="{
            labels: filteredData.map((d) => d.date),
            datasets: [
              {
                label: `${selectedTab} - ${selectedPlace}`,
                data: filteredData.map((d) => d.value),
                borderColor: 'var(--color-sumato-primary-hover)',
                backgroundColor: 'rgba(59, 130, 246, 0.3)',
                fill: true,
                tension: 0.3,
              },
            ],
          }"
          :options="{ responsive: true, maintainAspectRatio: false }"
          style="height: 300px"
        />
      </div>
    </div>
  </div>
</template>
