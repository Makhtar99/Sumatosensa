import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { isAuthenticated } from '@/services/AuthService'
import AppLayout from '@/layout/AppLayout.vue'
import Dashboard from '@/views/Dashboard.vue'
import LoginForm from '@/views/LoginForm.vue'
import RegisterForm from '@/views/RegisterForm.vue'

import HomeExampleView from '@/views/HomeExampleView.vue'
import LoginExampleView from '@/views/LoginExampleView.vue'
import AdminExampleView from '@/views/AdminExampleView.vue'
import testRegister from '@/views/testRegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
  {
    path: '/',
    component: AppLayout,
    children: [
      {
        path: '',
        name: 'dashboard',
        component: Dashboard,
        meta: { requiresAuth: false }
      },
      // {
      //   path: 'admin',
      //   name: 'admin',
      //   component: AdminPanel,
      //   meta: { requiresAuth: true, requiresAdmin: true }
      // }
    ]
  },
    {
      path: '/login',
      name: 'login',
      component: LoginForm,
      meta: { requiresGuest: true},
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterForm,
      meta: { requiresGuest: true},
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminExampleView,
      meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
      path: '/test',
      name: 'test',
      component: testRegister,
      meta: { requiresAuth: false, requiresAdmin: false },
    },
  ],
})

// Navigation guards
router.beforeEach((to, from, next) => {
  console.log("➡️ Navigation vers :", to.path)
  console.log("🔐 Auth requis ?", to.meta.requiresAuth)
  console.log("🧾 Authentifié ?", isAuthenticated())
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

export default router
