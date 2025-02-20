<template>
  <v-container class="text-center py-12">
    <!-- Hero Section with gradient and animation -->
    <v-card
      class="pa-12 rounded-xl elevation-8 hero-card"
      dark
    >
      <v-scale-transition>
        <h1 class="text-h2 font-weight-bold mb-4">Welcome to BoardingSpot</h1>
      </v-scale-transition>
      <p class="text-h6 mb-5 font-weight-light">
        Find your perfect boarding room with our smart matching system
      </p>
    </v-card>

    <!-- Sections for Tenants & Landlords with hover effects -->
    <v-row class="mt-16">
      <v-col cols="12" md="6">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 12 : 3"
            :class="{ 'on-hover': isHovering }"
            class="pa-8 rounded-lg transition-swing"
          >
            <h2 class="text-h4 font-weight-bold mb-4">For Tenants</h2>
            <p class="text-subtitle-1 mb-6">Search for rooms that match your preferences and get personalized recommendations.</p>
            <v-btn
              v-if="!auth.isAuthenticated"
              to="/register"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="4"
            >
              Register as Tenant
            </v-btn>
            <v-btn
              v-else-if="auth.isTenant"
              to="/search"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="4"
            >
              Search Rooms
            </v-btn>
          </v-card>
        </v-hover>
      </v-col>

      <v-col cols="12" md="6">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 12 : 3"
            :class="{ 'on-hover': isHovering }"
            class="pa-8 rounded-lg transition-swing"
          >
            <h2 class="text-h4 font-weight-bold mb-4">For Landlords</h2>
            <p class="text-subtitle-1 mb-6">List your rooms and manage your properties efficiently.</p>
            <v-btn
              v-if="!auth.isAuthenticated"
              to="/register"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="4"
            >
              Register as Landlord
            </v-btn>
            <v-btn
              v-else-if="auth.isLandlord"
              to="/landlord"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="4"
            >
              Manage Rooms
            </v-btn>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>

    <!-- Why Choose Section with improved cards -->
    <h2 class="text-h3 font-weight-bold mt-16 mb-8">Why Choose Boarding Spot?</h2>
    
    <v-row class="mt-6">
      <v-col cols="12" md="4">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            class="pa-6 text-center rounded-xl feature-card"
          >
            <v-icon color="primary" size="64" class="mb-4">mdi-lightbulb-outline</v-icon>
            <h3 class="text-h5 font-weight-bold mb-3">Smart Matching</h3>
            <p class="text-subtitle-1">Our algorithm finds rooms that perfectly match your preferences.</p>
          </v-card>
        </v-hover>
      </v-col>

      <v-col cols="12" md="4">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            class="pa-6 text-center rounded-xl feature-card"
          >
            <v-icon color="primary" size="64" class="mb-4">mdi-shield-check</v-icon>
            <h3 class="text-h5 font-weight-bold mb-3">Verified Listings</h3>
            <p class="text-subtitle-1">All rooms are verified to ensure quality and safety.</p>
          </v-card>
        </v-hover>
      </v-col>

      <v-col cols="12" md="4">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 8 : 2"
            class="pa-6 text-center rounded-xl feature-card"
          >
            <v-icon color="primary" size="64" class="mb-4">mdi-phone</v-icon>
            <h3 class="text-h5 font-weight-bold mb-3">Direct Contact</h3>
            <p class="text-subtitle-1">Connect directly with landlords or tenants.</p>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.hero-card {
  background: linear-gradient(135deg, var(--v-primary-base), var(--v-secondary-base));
  transition: all 0.3s ease;
}

.feature-card {
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.transition-swing {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.on-hover {
  transform: scale(1.02);
}
</style>


<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.gap-4 {
  gap: 1rem;
}
.gap-8 {
  gap: 2rem;
}
</style>
