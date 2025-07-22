import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Simulation from '@/views/Simulation.vue'
import Results from '@/views/Results.vue'
import About from '@/views/About.vue'
import store from '@/store'
import SimulationList from '@/views/SimulationList.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/simulation',
    name: 'Simulation',
    component: Simulation,
    meta: { requiresAuth: true }
  },
  {
    path: '/simulations',
    name: 'SimulationList',
    component: SimulationList,
    meta: { requiresAuth: true }
  },
  {
    path: '/results/:id',
    name: 'Results',
    component: Results,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router