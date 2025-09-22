import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserPrefStore } from '@/stores/userpref'

import AppLayout from '../layout/AppLayout.vue'
import LoginForm from '../views/Auth/LoginForm.vue'
import RegisterForm from '../views/Auth/RegisterForm.vue'

import Dashboard from '../views/ViewDashboard.vue'
import Settings from '../views/ViewSettings.vue'
import Management from '../views/ViewManagement.vue'
import Devices from '../views/ViewSensor.vue'
import Notifications from '../views/ViewNotifications.vue'
import OnboardingPreferences from '@/views/OnboardingPreferences.vue'

import AdminExampleView from '@/views/ViewAdminListUser.vue'
import UserRoleManager from '../views/UserRoleManager.vue'

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
        meta: { requiresAuth: true, hasDoneOnboarding: true },
      },
      {
        path: 'management',
        name: 'Management',
        component: Management,
        meta: { requiresAuth: true },
      },
      {
        path: 'sensors',
        name: 'Devices',
        component: Devices,
        meta: { requiresAuth: true },
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications,
        meta: { requiresAuth: true },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: '/onboarding',
    name: 'OnboardingPreferences',
    component: () => OnboardingPreferences,
    meta: { requiresAuth: true },
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
  {
    path: '/admin/users',
    name: 'UserRoleManager',
    component: UserRoleManager,
    meta: { requiresAuth: true, isAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


let appInitialized = false

export function setupRouterGuards() {
  appInitialized = true
}

router.beforeEach(async (to, from, next) => {
  if (!appInitialized) {
    return next()
  }

  const requiresAuth = to.matched.some((r) => r.meta.requiresAuth)

  if (requiresAuth && !localStorage.getItem('access_token')) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  next()
})

export default router
