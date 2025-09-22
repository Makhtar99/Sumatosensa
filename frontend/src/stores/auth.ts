import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {
  apiService,
  type LoginRequest,
  type User,
  type RegisterRequest,
} from '@/services/api'

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
      localStorage.setItem('user_role', response.user.role)
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
      localStorage.removeItem('user_role')
      isLoading.value = false
    }
  }

  async function getCurrentUser() {
    isLoading.value = true
    error.value = null
    try {
      const currentUser = await apiService.getCurrentUser()
      user.value = currentUser
      localStorage.setItem('user_role', currentUser.role)
      return currentUser
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur de récupération utilisateur'
      apiService.removeToken()
      localStorage.removeItem('user_role')
      user.value = null
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function initializeAuth(): Promise<void> {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        await getCurrentUser()
      } catch (err) {
        console.error('Token invalide, déconnexion automatique')
        console.error(err)
        apiService.removeToken()
        localStorage.removeItem('user_role')
      }
    }
  }

  function clearError() {
    error.value = null
  }

  async function registerAndLogin(payload: RegisterRequest) {
    isLoading.value = true
    error.value = null
    try {
      await apiService.register(payload)
      const loginResponse = await apiService.login({ username: payload.username, password: payload.password })
      user.value = loginResponse.user
      localStorage.setItem('user_role', loginResponse.user.role)
      return loginResponse
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Erreur d'inscription"
      throw err
    } finally {
      isLoading.value = false
    }
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
    clearError,
    registerAndLogin,
  }
})
