import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layout/AppLayout.vue'
import LoginForm from '@/views/LoginForm.vue'
import RegisterForm from '@/views/RegisterForm.vue'
import Dashboard from '@/views/Dashboard.vue'

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
