<template>
  <v-app>
    <v-main>
      <div class="container">
        <v-app-bar
          elevation="5"
          variant="elevated"
          class="px-6"
          style="height: 70px;"
        >
            <router-link to="/" class="text-decoration-none d-flex align-center">
              <div class="d-flex align-center brand-container">
              <div class="brand-text">
                <v-card-title class="text-primary ml-6 font-weight-bold pa-0 text-h5">
                Boarding<span class="text-secondary">Spot</span>
                </v-card-title>
                <div class="text-caption ml-6 text-medium-emphasis">Find your perfect stay</div>
              </div>
              </div>
            </router-link>
            <v-spacer></v-spacer>
          <div class="d-flex align-center">
            <template v-if="!auth.isAuthenticated">
              <v-btn
                to="/login"
                color="primary"
                variant="elevated"
                prepend-icon="mdi-login"
              >
              </v-btn>
            </template>
            <template v-else>
              <v-btn
                v-if="auth.isTenant"
                to="/tenant"
                color="primary"
                variant="elevated"
                prepend-icon="mdi-view-dashboard"
                class="mr-4"
              >
                Dashboard
              </v-btn>
              <v-btn
                v-if="auth.isLandlord"
                to="/landlord"
                color="primary"
                variant="elevated"
                prepend-icon="mdi-view-dashboard"
                class="mr-4"
              >
                Dashboard
              </v-btn>
              <v-btn
                @click="logout"
                color="error"
                variant="elevated"
                prepend-icon="mdi-logout"
              >
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
