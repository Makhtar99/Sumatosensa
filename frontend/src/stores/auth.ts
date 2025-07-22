import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { apiService, type LoginRequest, type User } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => user.value !== null)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(credentials: LoginRequest) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiService.login(credentials)
      user.value = response.user
      return response
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur de connexion'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    isLoading.value = true
    error.value = null
    
    try {
      await apiService.logout()
    } catch (err) {
      console.error('Erreur lors de la déconnexion:', err)
    } finally {
      user.value = null
      isLoading.value = false
    }
  }

  async function getCurrentUser() {
    isLoading.value = true
    error.value = null
    
    try {
      const currentUser = await apiService.getCurrentUser()
      user.value = currentUser
      return currentUser
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur de récupération utilisateur'
      apiService.removeToken()
      user.value = null
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function deleteUser(userId: number) {
    isLoading.value = true
    error.value = null
    try {
      await apiService.deleteUser(userId)
      if (user.value?.id === userId) {
        user.value = null // Déconnexion si l'utilisateur supprimé est l'utilisateur courant
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur de suppression utilisateur'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function initializeAuth() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        await getCurrentUser()
      } catch (err) {
        console.error('Token invalide, déconnexion automatique')
        apiService.removeToken()
      }
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    getCurrentUser,
    initializeAuth,
    clearError
  }
})