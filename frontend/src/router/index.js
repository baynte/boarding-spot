import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LandlordDashboard from '@/views/LandlordDashboard.vue'
import LandlordProfile from '@/views/LandlordProfile.vue'
import TenantDashboard from '@/views/TenantDashboard.vue'
import RoomSearch from '@/views/RoomSearch.vue'
import PreferencesView from '@/views/PreferencesView.vue'
import AdminLoginView from '@/views/AdminLoginView.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/landlord',
      name: 'landlord',
      component: LandlordDashboard,
      meta: { requiresAuth: true, requiresLandlord: true }
    },
    {
      path: '/landlord/profile',
      name: 'landlordProfile',
      component: LandlordProfile,
      meta: { requiresAuth: true, requiresLandlord: true }
    },
    {
      path: '/tenant',
      name: 'tenant',
      component: TenantDashboard,
      meta: { requiresAuth: true, requiresTenant: true }
    },
    {
      path: '/search',
      name: 'search',
      component: RoomSearch,
      meta: { requiresAuth: true, requiresTenant: true }
    },
    {
      path: '/preferences',
      name: 'preferences',
      component: PreferencesView,
      meta: { requiresAuth: true, requiresTenant: true }
    },
    {
      path: '/admin/login',
      name: 'adminLogin',
      component: AdminLoginView
    },
    {
      path: '/admin/dashboard',
      name: 'adminDashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresLandlord && !auth.isLandlord) {
    next('/')
  } else if (to.meta.requiresTenant && !auth.isTenant) {
    next('/')
  } else if (to.meta.requiresAdmin && !auth.isAdminUser) {
    next('/admin/login')
  } else {
    next()
  }
})

export default router 