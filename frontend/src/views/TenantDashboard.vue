<template>
  <div>
    <h1 class="text-h4 mb-4 mt-10">Tenant Dashboard</h1>

    <!-- Current Preferences Card -->
    <v-card class="mb-6" elevation="10" rounded="lg">
      <v-card-title class="d-flex align-center pa-6 bg-primary-lighten-5">
      <v-icon icon="mdi-tune" size="24" class="mr-2" color="primary"/>
      <span class="text-h5 font-weight-medium">My Preferences</span>
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        prepend-icon="mdi-pencil"
        to="/preferences"
        rounded
        elevation="7"
      >
        Edit Preferences
      </v-btn>
      </v-card-title>

      <v-card-text v-if="preferences" class="pa-6">
      <v-row>
        <v-col cols="12" sm="6" md="3">
        <v-card variant="flat" class="pa-4 bg-grey-lighten-4" rounded="lg" elevation="5">
          <div class="text-subtitle-2 text-grey-darken-5 font-weight-bold mb-2">Maximum Price</div>
          <div class="text-h5 font-weight-bold text-primary">₱{{ preferences.max_price.toLocaleString() }}</div>
        </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
        <v-card variant="flat" class="pa-4 bg-grey-lighten-4" rounded="lg" elevation="5">
          <div class="text-subtitle-2 text-grey-darken-5 font-weight-bold mb-2">Minimum Capacity</div> 
          <div class="text-h5 font-weight-bold text-primary">{{ preferences.min_capacity }} Person(s)</div>
        </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
        <v-card variant="flat" class="pa-4 bg-grey-lighten-4" rounded="lg" elevation="5">
          <div class="text-subtitle-2 text-grey-darken-5 font-weight-bold mb-2">Preferred Location</div>
          <div class="text-h5 font-weight-bold text-primary">{{ preferences.preferred_location }}</div>
        </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
        <v-card variant="flat" class="pa-4 bg-grey-lighten-4" rounded="lg" elevation="5">
          <div class="text-subtitle-2 text-grey-darken-5 font-weight-bold mb-2">Required Amenities</div>
          <v-chip-group>
          <v-chip
            v-for="amenity in preferences.required_amenities"
            :key="amenity"
            color="primary"
            variant="outlined"
            size="small"
            class="font-weight-medium"
          >
            {{ amenity }}
          </v-chip>
          </v-chip-group>
        </v-card>
        </v-col>
      </v-row>

        <!-- <v-divider class="my-4"></v-divider> -->

        <!-- <div class="text-subtitle-1 mb-2">Importance Weights</div> -->
        <!-- <v-row>
          <v-col cols="12" sm="6" md="3">
            <div class="text-caption">Safety</div>
            <v-progress-linear
              :model-value="preferences.safety_weight * 100"
              color="primary"
              height="8"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}</strong>
              </template>
            </v-progress-linear>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-caption">Cleanliness</div>
            <v-progress-linear
              :model-value="preferences.cleanliness_weight * 100"
              color="primary"
              height="8"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}</strong>
              </template>
            </v-progress-linear>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-caption">Accessibility</div>
            <v-progress-linear
              :model-value="preferences.accessibility_weight * 100"
              color="primary"
              height="8"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}</strong>
              </template>
            </v-progress-linear>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-caption">Noise Level</div>
            <v-progress-linear
              :model-value="preferences.noise_level_weight * 100"
              color="primary"
              height="8"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}</strong>
              </template>
            </v-progress-linear>
          </v-col>
        </v-row> -->
      </v-card-text>

      <v-card-text v-else>
        <v-alert
          type="info"
          text="You haven't set your preferences yet. Setting preferences will help us find the perfect room for you."
        >
          <template v-slot:append>
            <v-btn
              color="info"
              variant="text"
              to="/preferences"
            >
              Set Preferences
            </v-btn>
          </template>
        </v-alert>
      </v-card-text>
    </v-card>

    <!-- Quick Actions -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="4">
      <v-card elevation="12" rounded="lg" class="action-card">
        <v-card-text class="text-center pa-6">
        <v-icon
          color="primary"
          size="56"
          class="mb-4"
          icon="mdi-home-search"
        ></v-icon>
        <h3 class="text-h6 font-weight-bold mb-3">Search Living Spaces</h3>
        <p class="text-body-1 text-grey-darken-1 mb-6">Find your perfect living space based on your preferences</p>
        <v-btn
          color="primary"
          size="large"
          block
          rounded="lg"
          elevation="7"
          to="/search"
          class="text-none"
        >
          Search Now
        </v-btn>
        </v-card-text>
      </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
      <v-card elevation="12" rounded="lg" class="action-card">
        <v-card-text class="text-center pa-6">
        <v-icon
          color="primary"
          size="56"
          class="mb-4"
          icon="mdi-tune"
        ></v-icon>
        <h3 class="text-h6 font-weight-bold mb-3">Update Preferences</h3>
        <p class="text-body-1 text-grey-darken-1 mb-6">Modify your preferences to get better matches</p>
        <v-btn
          color="primary"
          size="large"
          block
          rounded="lg"
          elevation="7"
          to="/preferences"
          class="text-none"
        >
          Update Now
        </v-btn>
        </v-card-text>
      </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
      <v-card elevation="2" rounded="lg" class="action-card">
        <v-card-text class="text-center pa-6">
        <v-icon
          color="primary"
          size="56"
          class="mb-4"
          icon="mdi-history"
        ></v-icon>
        <h3 class="text-h6 font-weight-bold mb-3">Recent Views</h3>
        <p class="text-body-1 text-grey-darken-1 mb-6">Check your recently viewed rooms</p>
        <v-btn
          color="primary"
          size="large"
          block
          rounded="lg"
          elevation="7"
          @click="showRecentlyViewed"
          class="text-none"
        >
          View History
        </v-btn>
        </v-card-text>
      </v-card>
      </v-col>
    </v-row>

    <!-- Recently Viewed Rooms Dialog -->
    <v-dialog v-model="recentlyViewedDialog" max-width="600" scrollable>
      <v-card rounded="lg">
      <v-toolbar color="primary" class="text-white">
        <v-toolbar-title class="text-h6">Recently Viewed Rooms</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="recentlyViewedDialog = false">
        <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      
      <v-card-text class="pa-4">
        <v-list v-if="recentlyViewed.length" class="pa-0">
        <v-list-item
          v-for="room in recentlyViewed"
          :key="room.id"
          :title="room.title"
          :subtitle="`₱${room.price.toLocaleString()} - ${room.location}`"
          @click="viewRoom(room)"
          rounded="lg"
          class="mb-2"
        >
          <template v-slot:prepend>
          <v-avatar size="56" rounded="lg">
            <v-img :src="room.image_urls?.[0]" cover></v-img>
          </v-avatar>
          </template>
          <template v-slot:append>
          <v-icon color="primary">mdi-chevron-right</v-icon>
          </template>
        </v-list-item>
        </v-list>
        
        <v-alert
        v-else
        type="info"
        variant="tonal"
        class="mt-4"
        text="No recently viewed rooms found"
        ></v-alert>
      </v-card-text>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const preferences = ref(null)
const recentlyViewed = ref([])
const recentlyViewedDialog = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

onMounted(async () => {
  await fetchPreferences()
  await fetchRecentlyViewed()
})

const fetchPreferences = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/tenant/preferences`)
    if (response.data) {
      preferences.value = {
        max_price: response.data.max_price,
        min_capacity: response.data.min_capacity,
        preferred_location: response.data.preferred_location,
        required_amenities: Array.isArray(response.data.required_amenities) ? 
          response.data.required_amenities : 
          (response.data.required_amenities ? JSON.parse(response.data.required_amenities) : []),
        safety_weight: response.data.safety_weight,
        cleanliness_weight: response.data.cleanliness_weight,
        accessibility_weight: response.data.accessibility_weight,
        noise_level_weight: response.data.noise_level_weight
      }
    }
  } catch (error) {
    console.error('Error fetching preferences:', error)
    snackbarText.value = error.response?.data?.error || 'Error fetching preferences'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const fetchRecentlyViewed = async () => {
  try {
    const response = await axios.get(`/tenant/recently-viewed`)
    recentlyViewed.value = response.data || []
  } catch (error) {
    console.error('Error fetching recently viewed rooms:', error)
  }
}

const showRecentlyViewed = () => {
  recentlyViewedDialog.value = true
}

const viewRoom = (room) => {
  recentlyViewedDialog.value = false
  router.push(`/rooms/${room.id}`)
}
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style> 