import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '@/services/AuthService'

import AppLayout from '@/layout/AppLayout.vue'

import LoginForm from '@/views/LoginForm.vue'
import RegisterForm from '@/views/RegisterForm.vue'

import Dashboard from '@/views/Dashboard.vue'
import Settings from '@/views/Settings.vue'
import ExportView from '@/views/ExportView.vue'
import Management from '@/views/Management.vue'
import History from '@/views/History.vue'
import devices from '@/views/Devices.vue'
import Alertes from '@/views/Alertes.vue'
import Notifications from '@/views/Notifications.vue'
import Energy from '@/views/Energy.vue'

import AdminExampleView from '@/views/TestBack/AdminExampleView.vue'

// Routes de l'application
const routes = [
  {
    path: '/',
    redirect: '/dashboard',
    component: AppLayout,
    children: [
      {
        path: '/',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: false },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { requiresAuth: true },
      },
      {
        path: 'export',
        name: 'Export',
        component: ExportView,
        meta: { requiresAuth: true },
      },
      {
        path: 'management',
        name: 'Management',
        component: Management,
        meta: { requiresAuth: true },
      },
      {
        path: 'history',
        name: 'History',
        component: History,
        meta: { requiresAuth: true },
      },
      {
        path: 'devices',
        name: 'Devices',
        component: devices,
        meta: { requiresAuth: true },
      },
      {
        path: 'alerts',
        name: 'Alertes',
        component: Alertes,
        meta: { requiresAuth: true },
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications,
        meta: { requiresAuth: true },
      },
      {
        path: 'energy',
        name: 'Energy',
        component: Energy,
        meta: { requiresAuth: true },
      }
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
    meta: { requiresAuth: false },
  },


]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  console.log("Authentifié ?", isAuthenticated())
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

export default router
