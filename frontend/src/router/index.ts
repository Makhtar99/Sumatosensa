import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import AppLayout from '../layout/AppLayout.vue'

import LoginForm from '../views/LoginForm.vue'
import RegisterForm from '../views/RegisterForm.vue'

import Dashboard from '../views/ViewDashboard.vue'
import Settings from '../views/ViewSettings.vue'
import Management from '../views/ViewManagement.vue'
import Devices from '../views/ViewSensor.vue'
import Notifications from '../views/ViewNotifications.vue'

import AdminExampleView from '@/views/ViewAdminListUser.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
    component: AppLayout,
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: false },
      },
      {
        path: 'management',
        name: 'Management',
        component: Management,
        meta: { requiresAuth: false },
      },
      {
        path: 'sensors',
        name: 'Devices',
        component: Devices,
        meta: { requiresAuth: false },
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications,
        meta: { requiresAuth: false },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { requiresAuth: false },
      },
    ],
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm,
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterForm,
    meta: { requiresAuth: false },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminExampleView,
    meta: { requiresAuth: true, isAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (!auth.user && localStorage.getItem('access_token')) {
    try {
      await auth.getCurrentUser()
    } catch {
    }
  }

  const requiresAuth = to.matched.some((r) => r.meta.requiresAuth)
  const requiresAdmin = to.matched.some((r) => r.meta.isAdmin)

  if (requiresAuth && !auth.isAuthenticated) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  if (requiresAdmin && !auth.isAdmin) {
    return { name: 'Dashboard' }
  }

  if ((to.name === 'Login' || to.name === 'Register') && auth.isAuthenticated) {
    return { name: 'Dashboard' }
  }

  if (to.name === undefined) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
