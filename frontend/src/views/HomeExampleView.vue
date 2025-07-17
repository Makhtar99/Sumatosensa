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
            <p class="text-gray-600 mb-8">
              Surveillance de l'environnement de travail - Température, Humidité, Pression
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Salle de réunion</h3>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-gray-600">Température:</span>
                    <span class="font-semibold">22.5°C</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Humidité:</span>
                    <span class="font-semibold">45%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Pression:</span>
                    <span class="font-semibold">1013 hPa</span>
                  </div>
                </div>
              </div>
              
              <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Open Space</h3>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-gray-600">Température:</span>
                    <span class="font-semibold">21.8°C</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Humidité:</span>
                    <span class="font-semibold">42%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Pression:</span>
                    <span class="font-semibold">1014 hPa</span>
                  </div>
                </div>
              </div>
              
              <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Bureau individuel</h3>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-gray-600">Température:</span>
                    <span class="font-semibold">23.1°C</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Humidité:</span>
                    <span class="font-semibold">48%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Pression:</span>
                    <span class="font-semibold">1012 hPa</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}
</script>