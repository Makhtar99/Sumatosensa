<template>
  <div class="p-6">
    <h1 class="title mb-6">Gestion des rôles utilisateurs</h1>
    
    <div v-if="loading" class="text-center">
      <p>Chargement...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ error }}</p>
    </div>

    <div v-else class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              ID
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Nom d'utilisateur
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Rôle
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Statut
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ user.id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ user.username }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ user.email }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <select
                v-model="user.role"
                @change="updateUserRole(user)"
                class="block w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                :disabled="user.id === currentUserId"
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="[
                'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                user.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              ]">
                {{ user.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button
                v-if="user.id !== currentUserId"
                @click="toggleUserStatus(user)"
                :class="[
                  'mr-2 px-3 py-1 rounded text-white text-xs',
                  user.is_active
                    ? 'bg-red-600 hover:bg-red-700'
                    : 'bg-green-600 hover:bg-green-700'
                ]"
              >
                {{ user.is_active ? 'Désactiver' : 'Activer' }}
              </button>
              <button
                v-if="user.id !== currentUserId"
                @click="deleteUser(user)"
                class="px-3 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700"
              >
                Supprimer
              </button>
              <span v-else class="text-gray-400 text-xs">
                (Votre compte)
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface User {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  created_at: string
}

const users = ref<User[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const currentUserId = ref<number | null>(null)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function fetchUsers() {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      error.value = 'Token d\'authentification manquant'
      return
    }

    const response = await fetch(`${API_URL}/admin/users`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`Erreur ${response.status}: ${response.statusText}`)
    }

    users.value = await response.json()
    
    // Get current user ID
    const meResponse = await fetch(`${API_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (meResponse.ok) {
      const currentUser = await meResponse.json()
      currentUserId.value = currentUser.id
    }
    
  } catch (err: any) {
    error.value = err.message || 'Erreur lors du chargement des utilisateurs'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

async function updateUserRole(user: User) {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      error.value = 'Token d\'authentification manquant'
      return
    }

    const response = await fetch(`${API_URL}/admin/users/${user.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        role: user.role
      })
    })

    if (!response.ok) {
      throw new Error(`Erreur lors de la mise à jour du rôle`)
    }

    // Success feedback
    console.log(`Rôle de ${user.username} mis à jour: ${user.role}`)
    
  } catch (err: any) {
    error.value = err.message || 'Erreur lors de la mise à jour du rôle'
    console.error('Erreur:', err)
    // Revert the change
    await fetchUsers()
  }
}

async function toggleUserStatus(user: User) {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      error.value = 'Token d\'authentification manquant'
      return
    }

    const response = await fetch(`${API_URL}/admin/users/${user.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        is_active: !user.is_active
      })
    })

    if (!response.ok) {
      throw new Error(`Erreur lors de la mise à jour du statut`)
    }

    user.is_active = !user.is_active
    
  } catch (err: any) {
    error.value = err.message || 'Erreur lors de la mise à jour du statut'
    console.error('Erreur:', err)
  }
}

async function deleteUser(user: User) {
  if (!confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur ${user.username} ?`)) {
    return
  }

  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      error.value = 'Token d\'authentification manquant'
      return
    }

    const response = await fetch(`${API_URL}/admin/users/${user.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`Erreur lors de la suppression`)
    }

    // Remove user from list
    users.value = users.value.filter(u => u.id !== user.id)
    
  } catch (err: any) {
    error.value = err.message || 'Erreur lors de la suppression de l\'utilisateur'
    console.error('Erreur:', err)
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
}
</style>