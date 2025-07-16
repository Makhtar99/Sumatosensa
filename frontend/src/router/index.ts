import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeExampleView from '@/views/HomeExampleView.vue'
import LoginExampleView from '@/views/LoginExampleView.vue'
import AdminExampleView from '@/views/AdminExampleView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeExampleView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginExampleView,
      meta: { requiresGuest: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminExampleView,
      meta: { requiresAuth: true, requiresAdmin: true },
    },
  ],
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth if not done yet
  if (!authStore.isAuthenticated && localStorage.getItem('access_token')) {
    try {
      await authStore.initializeAuth()
    } catch (error) {
      console.error('Auth initialization failed:', error)
    }
  }
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      next('/login')
      return
    }
    
    // Check if route requires admin
    if (to.matched.some(record => record.meta.requiresAdmin)) {
      if (!authStore.isAdmin) {
        next('/')
        return
      }
    }
  }
  
  // Redirect authenticated users away from login
  if (to.matched.some(record => record.meta.requiresGuest)) {
    if (authStore.isAuthenticated) {
      next('/')
      return
    }
  }
  
  next()
})

export default router
