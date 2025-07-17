import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layout/AppLayout.vue'
import LoginForm from '@/views/LoginForm.vue'
import RegisterForm from '@/views/RegisterForm.vue'
import Dashboard from '@/views/Dashboard.vue'
import Settings from '@/views/Settings.vue'
import ExportView from '@/views/ExportView.vue'
import Management from '@/views/Management.vue'
import History from '@/views/History.vue'
import devices from '@/views/Devices.vue'




// Routes de l'application
const routes = [
  {
    path: '/',
    component: AppLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: false },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { requiresAuth: false },
      },
      {
        path: 'export',
        name: 'Export',
        component: ExportView,
        meta: { requiresAuth: false },
      },
      {
        path: 'management',
        name: 'Management',
        component: Management,
        meta: { requiresAuth: false },
      },
      {
        path: 'history',
        name: 'History',
        component: History,
        meta: { requiresAuth: false },
      },
      {
        path: 'devices',
        name: 'Devices',
        component: devices,
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

]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
