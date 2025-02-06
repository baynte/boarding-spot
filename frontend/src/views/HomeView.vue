<template>
  <v-container class="text-center py-12">
    <!-- Hero Section -->
    <v-card
      class="pa-8 rounded-xl elevation-3"
      color="primary"
      dark
      elevation="10"
    >
      <h1 class="text-h3 font-weight-bold mb-3">Welcome to Boarding Spot</h1>
      <p class="text-subtitle-1 mb-5">
        Find your perfect boarding room with our smart matching system
      </p>
    </v-card>

    <!-- Sections for Tenants & Landlords -->
    <v-row class="mt-12">
      <v-col cols="12" md="6">
        <v-card class="pa-6 rounded-lg elevation-3">
          <h2 class="text-h5 font-weight-bold mb-3">For Tenants</h2>
          <p class="mb-4">Search for rooms that match your preferences and get personalized recommendations.</p>
          <v-btn
            v-if="!auth.isAuthenticated"
            to="/register"
            color="primary"
            rounded
            elevation="2"
          >
            Register as Tenant
          </v-btn>
          <v-btn
            v-else-if="auth.isTenant"
            to="/search"
            color="primary"
            rounded
            elevation="2"
          >
            Search Rooms
          </v-btn>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-6 rounded-lg elevation-3">
          <h2 class="text-h5 font-weight-bold mb-3">For Landlords</h2>
          <p class="mb-4">List your rooms and manage your properties efficiently.</p>
          <v-btn
            v-if="!auth.isAuthenticated"
            to="/register"
            color="primary"
            rounded
            elevation="2"
          >
            Register as Landlord
          </v-btn>
          <v-btn
            v-else-if="auth.isLandlord"
            to="/landlord"
            color="primary"
            rounded
            elevation="2"
          >
            Manage Rooms
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <!-- Why Choose Boarding Spot Section -->
    <h2 class="text-h4 font-weight-bold mt-12">Why Choose Boarding Spot?</h2>
    
    <v-row class="mt-6">
      <v-col cols="12" md="4">
        <v-card class="pa-5 text-center elevation-3 rounded-lg">
          <v-icon color="primary" size="48">mdi-lightbulb-outline</v-icon>
          <h3 class="text-h6 font-weight-bold mt-3">Smart Matching</h3>
          <p class="text-body-2">Our algorithm finds rooms that perfectly match your preferences.</p>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-5 text-center elevation-3 rounded-lg">
          <v-icon color="primary" size="48">mdi-shield-check</v-icon>
          <h3 class="text-h6 font-weight-bold mt-3">Verified Listings</h3>
          <p class="text-body-2">All rooms are verified to ensure quality and safety.</p>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-5 text-center elevation-3 rounded-lg">
          <v-icon color="primary" size="48">mdi-phone</v-icon>
          <h3 class="text-h6 font-weight-bold mt-3">Direct Contact</h3>
          <p class="text-body-2">Connect directly with landlords or tenants.</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


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
