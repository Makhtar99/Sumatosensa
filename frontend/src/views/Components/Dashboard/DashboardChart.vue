<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useUserPrefStore } from '@/stores/userpref'
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import weeklyData from '../../../assets/json/weekly_data.json'

const userPref = useUserPrefStore()

Chart.register(...registerables)

const anomaliesContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!anomaliesContainer.value) return

  const container = anomaliesContainer.value
  let scrollAmount = 0

  const interval = setInterval(() => {
    if (!container) return
    scrollAmount += 1
    if (scrollAmount >= container.scrollWidth - container.clientWidth) {
      scrollAmount = 0
    }
    container.scrollLeft = scrollAmount
  }, 30)
})

const selectedPeriod = defineModel<'today' | 'thisWeek' | 'fullMonth'>(
  'selectedPeriod',
)

const allDates = weeklyData.map(d => new Date(d.day))
const latestDate = new Date(Math.max(...allDates.map(d => d.getTime())))

function matchesTimeFilter(dateStr: string): boolean {
  const entryDate = new Date(dateStr)

  const todayStart = new Date(latestDate)
  todayStart.setHours(0, 0, 0, 0)

  const todayEnd = new Date(latestDate)
  todayEnd.setHours(23, 59, 59, 999)

  const startOfThisWeek = new Date(latestDate)
  startOfThisWeek.setDate(latestDate.getDate() - latestDate.getDay())
  startOfThisWeek.setHours(0, 0, 0, 0)

  const endOfThisWeek = new Date(latestDate)
  endOfThisWeek.setHours(23, 59, 59, 999)

  const startOfLastWeek = new Date(startOfThisWeek)
  startOfLastWeek.setDate(startOfThisWeek.getDate() - 7)

  const endOfLastWeek = new Date(startOfThisWeek)
  endOfLastWeek.setDate(startOfThisWeek.getDate() - 1)
  endOfLastWeek.setHours(23, 59, 59, 999)

  switch (selectedPeriod.value) {
    case "today":
      return entryDate >= todayStart && entryDate <= todayEnd
    case "thisWeek":
      return entryDate >= startOfThisWeek && entryDate <= endOfThisWeek
    default:
      return true
  }
}


const filteredData = computed(() => {
  return weeklyData.filter((entry) => matchesTimeFilter(entry.day))
})

const chartData = computed(() => {
  const labelsSet = new Set<string>()
  const roomsMap: Record<string, number[]> = {}

  filteredData.value.forEach((entry) => {
    labelsSet.add(entry.day)
    if (!roomsMap[entry.room]) roomsMap[entry.room] = []
    roomsMap[entry.room].push(entry.temperature_avg)
  })

  return {
    labels: Array.from(labelsSet).sort(),
    datasets: Object.keys(roomsMap).map((room) => ({
      label: room,
      data: roomsMap[room],
      borderColor: getColor(room),
      backgroundColor: getColor(room) + '33',
      fill: true,
      tension: 0.3,
      pointRadius: 2,
      pointHoverRadius: 5,
    })),
  }
})

const anomalies = computed(() => {
  return weeklyData.filter((entry) => {
    if (!matchesTimeFilter(entry.day)) return false

    let isAnomaly = false

    if (userPref.tempUnit === "Celsius") {
      if (entry.temperature_avg < userPref.alertMinTemperatureC || entry.temperature_avg > userPref.alertMaxTemperatureC) {
        isAnomaly = true
      }
    } else if (userPref.tempUnit === "Fahrenheit") {
      const tempF = (entry.temperature_avg * 9) / 5 + 32
      if (tempF < userPref.alertMinTemperatureF || tempF > userPref.alertMaxTemperatureF) {
        isAnomaly = true
      }
    }

    if (entry.humidity_avg < userPref.alertMinHumidite || entry.humidity_avg > userPref.alertMaxHumidite) {
      isAnomaly = true
    }

    if (userPref.pressureUnit === "hPa") {
      if (entry.pressure_avg < userPref.alertMinPressionhpa || entry.pressure_avg > userPref.alertMaxPressionhpa) {
        isAnomaly = true
      }
    } else if (userPref.pressureUnit === "bar") {
      const pressBar = entry.pressure_avg / 1000
      if (pressBar < userPref.alertMinPressionbar || pressBar > userPref.alertMaxPressionbar) {
        isAnomaly = true
      }
    }

    return isAnomaly
  })
})

function getColor(room) {
  switch (room) {
    case 'Salon':
      return '#3b82f6'
    case 'Cuisine':
      return '#10b981'
    case 'Grenier':
      return '#f59e0b'
    default:
      return '#6b7280'
  }
}
</script>

<template>
  <div class="w-full h-[250px] sm:h-[300px] md:h-[350px] lg:h-[400px] box-border">
    <Line
      :data="chartData"
      :options="{
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: {
              autoSkip: false,
              maxRotation: 60,
              minRotation: 30,
            },
          },
          y: {
            ticks: {
              callback: (val) => `${val} °C`,
            },
          },
        },
        plugins: {
          legend: { position: 'bottom' },
          title: {
            display: true,
            text: 'Température moyenne par pièce',
          },
        },
      }"
    />

    <div
      v-if="anomalies.length"
      ref="anomaliesContainer"
      class="anomalies-slide border-y-2 py-2 px-4 text-sm overflow-x-scroll"
    >
      <span
        v-for="(entry, index) in anomalies"
        :key="index"
        class="inline-block mr-6"
      >
        ⚠️ <strong>{{ entry.room }}</strong> - {{ entry.temperature_avg.toFixed(1) }} °C le {{ entry.day }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.anomalies-slide::-webkit-scrollbar {
  display: none;
}
.anomalies-slide {
  display: flex;
  gap: 2rem;
  white-space: nowrap;
  padding-inline: 2rem;
  padding: 1rem 0;
  align-items: center;
}
</style>
