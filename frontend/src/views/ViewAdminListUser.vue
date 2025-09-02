<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService, type User, type AdminDashboard } from '@/services/api'
import { useMediaQuery } from '@vueuse/core'
import DarkModeButton from '@/views/Components/DarkModeButton.vue'

const dashboard = ref<AdminDashboard | null>(null)
const users = ref<User[]>([])
const isLoading = ref(true)
const isTelephone = useMediaQuery('(max-width: 768px)')

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


<template>
  <div class="min-h-screen bg-[var(--color-surface)] text-[var(--color-sumato-text)]">

    <header class="bg-[var(--color-sumato-surface)] border-b border-[var(--color-sumato-border)]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div v-if="!isTelephone" class="flex justify-between items-center py-6">
          <h1 class="text-2xl !m-0 !p-0 md:text-3xl font-bold">
            Dashboard Admin
          </h1>

          <div class="flex items-center gap-3">
            
            <dark-mode-button />

            <router-link to="/"
              class="flex items-center gap-1 text-gray-500 hover:text-gray-700">
              <span>Retour</span>
            </router-link>

          </div>
        </div>

        <div v-else class="flex justify-between items-center py-6">
          <h1 class="text-2xl !m-0 !p-0 md:text-3xl font-bold">
            Dashboard Admin
          </h1>

          <div class="flex flex-col items-center gap-3">
            
            <dark-mode-button />

            <router-link to="/"
              class="flex items-center gap-1 text-gray-500 hover:text-gray-700">
              <span>Retour</span>
            </router-link>
          </div>
        </div>

      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="bg-[var(--color-sumato-surface)] border border-[var(--color-sumato-border)] rounded-xl shadow">
            <div class="p-5">
              <div class="flex items-center gap-4">
                <div class="w-8 h-8 rounded-full flex items-center justify-center bg-[var(--color-primary)]">
                  <span class="text-white font-bold">S</span>
                </div>
                <dl class="w-0 flex-1">
                  <dt class="text-sm opacity-80 truncate">Capteurs totaux</dt>
                  <dd class="text-lg font-semibold">{{ dashboard?.total_sensors || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="bg-[var(--color-sumato-surface)] border border-[var(--color-sumato-border)] rounded-xl shadow">
            <div class="p-5">
              <div class="flex items-center gap-4">
                <div class="w-8 h-8 rounded-full flex items-center justify-center bg-[var(--color-sumato-accent)]">
                  <span class="text-white font-bold">A</span>
                </div>
                <dl class="w-0 flex-1">
                  <dt class="text-sm opacity-80 truncate">Capteurs actifs</dt>
                  <dd class="text-lg font-semibold">{{ dashboard?.active_sensors || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="bg-[var(--color-sumato-surface)] border border-[var(--color-sumato-border)] rounded-xl shadow">
            <div class="p-5">
              <div class="flex items-center gap-4">
                <div class="w-8 h-8 rounded-full flex items-center justify-center bg-[var(--color-sumato-danger)]">
                  <span class="text-white font-bold">!</span>
                </div>
                <dl class="w-0 flex-1">
                  <dt class="text-sm opacity-80 truncate">Alertes non résolues</dt>
                  <dd class="text-lg font-semibold">{{ dashboard?.unresolved_alerts || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>

          <div class="bg-[var(--color-sumato-surface)] border border-[var(--color-sumato-border)] rounded-xl shadow">
            <div class="p-5">
              <div class="flex items-center gap-4">
                <div class="w-8 h-8 rounded-full flex items-center justify-center bg-[var(--notif-warning-text)]">
                  <span class="text-white font-bold">U</span>
                </div>
                <dl class="w-0 flex-1">
                  <dt class="text-sm opacity-80 truncate">Utilisateurs</dt>
                  <dd class="text-lg font-semibold">{{ dashboard?.total_users || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-[var(--color-sumato-surface)] border border-[var(--color-sumato-border)] shadow rounded-xl overflow-hidden">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg !mt-0 font-semibold">Utilisateurs</h3>
            <p class="mt-1 text-sm opacity-80">Liste des utilisateurs du système</p>
          </div>

          <div v-if="isLoading" class="px-4 py-6 sm:px-6">
            <div class="text-center opacity-80">Chargement...</div>
          </div>

          <div v-else>
            <ul class="divide-y divide-[var(--color-sumato-border)]">
              <li
                v-for="user in users"
                :key="user.id"
                class="px-4 py-4 sm:px-6"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="h-10 w-10 rounded-full bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)] flex items-center justify-center">
                      <span class="font-medium opacity-90">
                        {{ user.username.charAt(0).toUpperCase() }}
                      </span>
                    </div>
                    <div>
                      <div class="text-sm font-medium">
                        {{ user.username }}
                      </div>
                      <div class="text-sm opacity-80">
                        {{ user.email }}
                      </div>
                    </div>
                  </div>

                  <div class="flex items-center">
                    <span
                      :class="[
                        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
                        user.role === 'admin'
                          ? 'border-[var(--color-primary)] text-[var(--color-primary)]'
                          : 'border-[var(--color-sumato-border)] opacity-90'
                      ]"
                    >
                      {{ user.role }}
                    </span>

                    <span
                      :class="[
                        'ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
                        user.is_active
                          ? 'border-[var(--color-sumato-accent)] text-[var(--color-sumato-accent)]'
                          : 'border-[var(--color-sumato-danger)] text-[var(--color-sumato-danger)]'
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