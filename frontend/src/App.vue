<template>
  <v-app>
    <v-main>
      <div class="container">
        <div class="d-flex align-center justify-space-between py-4">
          <router-link to="/" class="text-decoration-none">
            <span class="text-primary font-weight-medium">Boarding Spot</span>
          </router-link>
          <div class="d-flex gap-4">
            <template v-if="!auth.isAuthenticated">
              <router-link to="/login" class="text-decoration-none text-black">Login</router-link>
            </template>
            <template v-else>
              <router-link 
                v-if="auth.isTenant" 
                to="/tenant" 
                class="text-decoration-none text-black"
              >Dashboard</router-link>
              <router-link 
                v-if="auth.isLandlord" 
                to="/landlord" 
                class="text-decoration-none text-black"
              >Dashboard</router-link>
              <a 
                href="#" 
                @click.prevent="logout" 
                class="text-decoration-none text-black"
              >Logout</a>
            </template>
          </div>
        </div>

        <router-view></router-view>

        <div class="text-center py-4 text-caption">
          © {{ new Date().getFullYear() }} - Boarding Spot
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = async () => {
  auth.logout()
  router.push('/login')
}
</script>

<style>
.gap-4 {
  gap: 1rem;
}
</style>
