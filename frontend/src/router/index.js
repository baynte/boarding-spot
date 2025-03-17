import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LandlordDashboard from '@/views/LandlordDashboard.vue'
import LandlordProfile from '@/views/LandlordProfile.vue'
import TenantDashboard from '@/views/TenantDashboard.vue'
import TenantProfile from '@/views/TenantProfile.vue'
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
      component: LoginView,
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guest: true }
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
      path: '/tenant/profile',
      name: 'tenantProfile',
      component: TenantProfile,
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
  
  // If route requires authentication and user is not authenticated
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } 
  // If route requires landlord role and user is not a landlord
  else if (to.meta.requiresLandlord && !auth.isLandlord) {
    next('/')
  } 
  // If route requires tenant role and user is not a tenant
  else if (to.meta.requiresTenant && !auth.isTenant) {
    next('/')
  } 
  // If route requires admin role and user is not an admin
  else if (to.meta.requiresAdmin && !auth.isAdminUser) {
    next('/admin/login')
  } 
  // If route is for guests (login/register) and user is already authenticated
  else if (to.meta.guest && auth.isAuthenticated) {
    // Redirect to appropriate dashboard based on user type
    if (auth.isLandlord) {
      next('/landlord')
    } else if (auth.isTenant) {
      next('/tenant')
    } else if (auth.isAdminUser) {
      next('/admin/dashboard')
    } else {
      next('/')
    }
  } 
  // Otherwise, proceed to the requested route
  else {
    next()
  }
})

export default router 