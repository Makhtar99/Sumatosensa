<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <h1 class="text-3xl font-bold text-gray-900">
              Sumātosensā
            </h1>
            <span class="ml-2 text-sm text-gray-500">Smart Sensors</span>
          </div>
          <div class="flex items-center space-x-4">
            <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
              <span class="text-sm text-gray-700">
                Connecté : {{ authStore.user?.username }}
              </span>
              <router-link
                to="/admin"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </router-link>
              <button
                @click="handleLogout"
                class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Déconnexion
              </button>
            </div>
            <div v-else>
              <router-link
                to="/login"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Connexion Admin
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="border-4 border-dashed border-gray-200 rounded-lg p-8">
          <div class="text-center">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">
              Données des capteurs en temps réel
            </h2>
            <div class="flex items-center justify-center mb-6">
              <p class="text-gray-600">
                Surveillance de l'environnement de travail - Température, Humidité, Pression
              </p>
              <button
                @click="loadSensors"
                :disabled="loading"
                class="ml-4 inline-flex items-center px-3 py-1.5 border border-gray-300 rounded text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span v-else>🔄</span>
                {{ loading ? 'Actualisation...' : 'Actualiser' }}
              </button>
            </div>

            <!-- Error State -->
            <div v-if="error" class="mb-6">
              <div class="bg-red-50 border-l-4 border-red-400 p-4 rounded">
                <p class="text-sm text-red-800">{{ error }}</p>
              </div>
            </div>

            <!-- Sensors Grid -->
            <div v-if="sensors.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div 
                v-for="sensor in sensors" 
                :key="sensor.id"
                class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
              >
                <h3 class="text-lg font-semibold text-gray-900 mb-2">
                  {{ sensor.name.replace('RuuviTag ', '') }}
                </h3>
                
                <div v-if="sensor.last_measurement" class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-gray-600">🌡️ Température:</span>
                    <span class="font-semibold">{{ sensor.last_measurement.temperature?.toFixed(1) }}°C</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">💧 Humidité:</span>
                    <span class="font-semibold">{{ sensor.last_measurement.humidity?.toFixed(1) }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">🔽 Pression:</span>
                    <span class="font-semibold">{{ sensor.last_measurement.pressure?.toFixed(0) }} hPa</span>
                  </div>
                  <div class="mt-3 pt-2 border-t border-gray-100">
                    <div class="text-xs text-gray-500">
                      Mise à jour: {{ formatTime(sensor.last_measurement.time) }}
                    </div>
                  </div>
                </div>
                
                <div v-else class="text-center text-gray-500">
                  <div class="text-2xl mb-2">📊</div>
                  <div class="text-sm">Aucune donnée</div>
                </div>
              </div>
            </div>

            <!-- No Sensors State -->
            <div v-else-if="!loading" class="text-center py-8">
              <div class="text-gray-400 text-4xl mb-4">📡</div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Aucun capteur trouvé</h3>
              <p class="text-gray-600">Vérifiez que le simulateur MQTT fonctionne.</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { apiService, type Sensor } from '@/services/api'

const authStore = useAuthStore()
const router = useRouter()
const sensors = ref<Sensor[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
let refreshInterval: number | null = null

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}

const loadSensors = async () => {
  try {
    loading.value = true
    error.value = null
    sensors.value = await apiService.getSensors(true)
  } catch (err) {
    console.error('Erreur lors du chargement des capteurs:', err)
    error.value = err instanceof Error ? err.message : 'Erreur inconnue'
  } finally {
    loading.value = false
  }
}

const formatTime = (timeString: string | null): string => {
  if (!timeString) return 'N/A'
  const date = new Date(timeString)
  return date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await loadSensors()
  refreshInterval = setInterval(loadSensors, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>