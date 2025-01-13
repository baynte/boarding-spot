<template>
  <div>
    <h1 class="text-h4 font-weight-bold mb-4">Welcome to Boarding Spot</h1>
    <p class="text-subtitle-1 mb-8">Find your perfect boarding room with our smart matching system</p>

    <div class="mb-16">
      <h2 class="text-h5 font-weight-bold mb-4">For Tenants</h2>
      <p class="mb-4">Search for rooms that match your preferences and get personalized recommendations</p>
      <div class="d-flex align-center gap-4">
        <v-btn
          v-if="!auth.isAuthenticated"
          to="/register"
          color="primary"
          variant="flat"
        >
          Register as Tenant
        </v-btn>
        <v-btn
          v-else-if="auth.isTenant"
          to="/search"
          color="primary"
          variant="flat"
        >
          Search Rooms
        </v-btn>
      </div>
    </div>

    <div class="mb-16">
      <h2 class="text-h5 font-weight-bold mb-4">For Landlords</h2>
      <p class="mb-4">List your rooms and manage your properties efficiently</p>
      <div class="d-flex align-center gap-4">
        <v-btn
          v-if="!auth.isAuthenticated"
          to="/register"
          color="primary"
          variant="flat"
        >
          Register as Landlord
        </v-btn>
        <v-btn
          v-else-if="auth.isLandlord"
          to="/landlord"
          color="primary"
          variant="flat"
        >
          Manage Rooms
        </v-btn>
      </div>
    </div>

    <div>
      <h2 class="text-h5 font-weight-bold mb-8">Why Choose Boarding Spot?</h2>
      <div class="d-flex flex-column gap-8">
        <div>
          <h3 class="text-h6 font-weight-bold mb-2">Smart Matching</h3>
          <p>Our algorithm finds rooms that perfectly match your preferences</p>
        </div>
        <div>
          <h3 class="text-h6 font-weight-bold mb-2">Verified Listings</h3>
          <p>All rooms are verified to ensure quality and safety</p>
        </div>
        <div>
          <h3 class="text-h6 font-weight-bold mb-2">Direct Contact</h3>
          <p>Connect directly with landlords or tenants</p>
        </div>
      </div>
    </div>
  </div>
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
