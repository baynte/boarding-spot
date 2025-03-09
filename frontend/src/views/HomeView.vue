<template class="bg-grey-lighten-5">
  <v-container class="text-center py-16 hero-container">
    <v-hover v-slot="{ isHovering, props }">
      <v-card
        class="pa-16 rounded-xl hero-card transition-swing"
        dark
        v-bind="props"
        :elevation="isHovering ? 16 : 4"
        :class="{ 'on-hover': isHovering }"
      >
        <div class="hero-content">
          <v-scale-transition>
            <h1 class="text-h1 font-weight-black text-white mb-6">Welcome to BoardingSpot</h1>
          </v-scale-transition>
          <p class="text-h5 mb-8 font-weight-light text-white hero-subtitle">
            Find your perfect boarding room with our smart matching system
          </p>
        </div>
      </v-card>
    </v-hover>

    <!-- Sections for Tenants & Landlords with hover effects -->
    <v-row class="mt-16 user-sections">
      <v-col cols="12" md="6">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 12 : 2"
            :class="{ 'on-hover': isHovering }"
            class="pa-12 rounded-xl transition-swing user-card"
          >
            <v-icon size="64" color="primary" class="mb-6">mdi-account-circle</v-icon>
            <h2 class="text-h3 font-weight-bold mb-6">For Tenants</h2>
            <p class="text-h6 mb-8 description">
              Search for rooms that match your preferences and get personalized recommendations.
            </p>
            <v-btn
              v-if="!auth.isAuthenticated"
              to="/register"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="8"
              class="px-8 py-4"
            >
              Register as Tenant
            </v-btn>
            <v-btn
              v-else-if="auth.isTenant"
              to="/search"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="8"
              class="px-8 py-4"
            >
              Search Rooms
            </v-btn>
          </v-card>
        </v-hover>
      </v-col>

      <v-col cols="12" md="6">
        <!-- Similar updates for landlord card -->
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            v-bind="props"
            :elevation="isHovering ? 12 : 2"
            :class="{ 'on-hover': isHovering }"
            class="pa-12 rounded-xl transition-swing user-card"
          >
            <v-icon size="64" color="primary" class="mb-6">mdi-home</v-icon>
            <h2 class="text-h3 font-weight-bold mb-6">For Landlords</h2>
            <p class="text-h6 mb-8 description">
              List your rooms and manage your properties efficiently.
            </p>
            <v-btn
              v-if="!auth.isAuthenticated"
              to="/register"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="8"
              class="px-8 py-4"
            >
              Register as Landlord
            </v-btn>
            <v-btn
              v-else-if="auth.isLandlord"
              to="/landlord"
              color="primary"
              size="x-large"
              rounded="pill"
              elevation="8"
              class="px-8 py-4"
            >
              Manage Rooms
            </v-btn>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>

    <!-- Why Choose Section -->
    <div class="why-choose-section mt-16 pt-8">
      <h2 class="text-h2 font-weight-black mb-12">Why Choose Boarding Spot?</h2>

      <v-row class="mt-8">
        <v-col cols="12" md="4" v-for="(feature, index) in features" :key="index">
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              v-bind="props"
              :elevation="isHovering ? 8 : 1"
              class="pa-8 text-center rounded-xl feature-card"
            >
              <v-icon :color="feature.color" size="72" class="mb-6">{{ feature.icon }}</v-icon>
              <h3 class="text-h4 font-weight-bold mb-4">{{ feature.title }}</h3>
              <p class="text-subtitle-1">{{ feature.description }}</p>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<style scoped>
.hero-card {
  background: rgba(47,72,164,255);
  transition: all 0.4s ease;
  overflow: hidden;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-subtitle {
  opacity: 0.9;
  line-height: 1.6;
}

.user-card {
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  transition: all 0.4s ease;
  height: 100%;
}

.feature-card {
  transition: all 0.4s ease;
  height: 100%;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
}

.feature-card:hover {
  transform: translateY(-8px);
}

.transition-swing {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.on-hover {
  transform: scale(1.03);
}

.description {
  color: #6c757d;
  line-height: 1.6;
}

.why-choose-section {
  background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.02) 100%);
}
</style>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const features = [
  {
    icon: 'mdi-lightbulb-outline',
    title: 'Smart Matching',
    description: 'Our algorithm finds rooms that perfectly match your preferences.',
    color: '#2196F3'
  },
  {
    icon: 'mdi-shield-check',
    title: 'Verified Listings',
    description: 'All rooms are verified to ensure quality and safety.',
    color: '#4CAF50'
  },
  {
    icon: 'mdi-phone',
    title: 'Direct Contact',
    description: 'Connect directly with landlords or tenants.',
    color: '#FF9800'
  }
]
</script>
