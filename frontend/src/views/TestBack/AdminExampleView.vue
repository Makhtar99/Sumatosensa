<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <h1 class="text-3xl font-bold text-gray-900">
              Dashboard Admin
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-700">
              {{ authStore.user?.username }}
            </span>
            <router-link
              to="/"
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Retour
            </router-link>
            <button
              @click="handleLogout"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold">S</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Capteurs totaux
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ dashboard?.total_sensors || 0 }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold">A</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Capteurs actifs
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ dashboard?.active_sensors || 0 }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold">!</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Alertes non résolues
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ dashboard?.unresolved_alerts || 0 }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold">U</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Utilisateurs
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ dashboard?.total_users || 0 }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Utilisateurs
            </h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              Liste des utilisateurs du système
            </p>
          </div>
          <div v-if="isLoading" class="px-4 py-5 sm:px-6">
            <div class="text-center">Chargement...</div>
          </div>
          <div v-else>
            <ul class="divide-y divide-gray-200">
              <li v-for="user in users" :key="user.id" class="px-4 py-4 sm:px-6">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 bg-gray-300 rounded-full flex items-center justify-center">
                        <span class="text-gray-700 font-medium">
                          {{ user.username.charAt(0).toUpperCase() }}
                        </span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">
                        {{ user.username }}
                      </div>
                      <div class="text-sm text-gray-500">
                        {{ user.email }}
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center">
                    <span
                      :class="[
                        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                        user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                      ]"
                    >
                      {{ user.role }}
                    </span>
                    <span
                      :class="[
                        'ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                        user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      ]"
                    >
                      {{ user.is_active ? 'Actif' : 'Inactif' }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { apiService, type User, type AdminDashboard } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const dashboard = ref<AdminDashboard | null>(null)
const users = ref<User[]>([])
const isLoading = ref(true)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}

const loadDashboard = async () => {
  try {
    dashboard.value = await apiService.getAdminDashboard()
  } catch (error) {
    console.error('Erreur lors du chargement du dashboard:', error)
  }
}

const loadUsers = async () => {
  try {
    users.value = await apiService.getUsers()
  } catch (error) {
    console.error('Erreur lors du chargement des utilisateurs:', error)
  }
}

onMounted(async () => {
  isLoading.value = true
  await Promise.all([loadDashboard(), loadUsers()])
  isLoading.value = false
})
</script>