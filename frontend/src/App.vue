<template>
  <v-app>
    <v-main>
      <div class="container">
        <v-app-bar
          elevation="1"
          variant="elevated"
          class="my-3 px-5"
        >
            <router-link to="/" class="text-decoration-none d-flex align-center">
              <div class="d-flex align-center brand-container">
              <v-img
                src="@/assets/logo.png"
                max-height="48"
                max-width="48"
                contain
                class="mr-2"
                :style="{ filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.5))' }"
              ></v-img>
              <div class="brand-text">
                <v-card-title class="text-primary font-weight-bold pa-0 text-h5">
                Boarding<span class="text-secondary">Spot</span>
                </v-card-title>
                <div class="text-caption text-medium-emphasis">Find your perfect stay</div>
              </div>
              </div>
            </router-link>
            <v-spacer></v-spacer>
          <div class="d-flex align-center">
            <template v-if="!auth.isAuthenticated">
              <v-btn
                to="/login"
                color="primary"
                variant="text"
                prepend-icon="mdi-login"
                size="x-large"
              >
              </v-btn>
            </template>
            <template v-else>
              <v-btn
                v-if="auth.isTenant"
                to="/tenant"
                color="primary"
                variant="text"
                prepend-icon="mdi-view-dashboard"
              >
                Dashboard
              </v-btn>
              <v-btn
                v-if="auth.isLandlord"
                to="/landlord"
                color="primary"
                variant="text"
                prepend-icon="mdi-view-dashboard"
              >
                Dashboard
              </v-btn>
              <v-btn
                @click="logout"
                color="error"
                variant="text"
                prepend-icon="mdi-logout"
              >
                Logout
              </v-btn>
            </template>
          </div>
        </v-app-bar>

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
