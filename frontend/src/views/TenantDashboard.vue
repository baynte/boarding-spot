<template>
  <div>
    <h1 class="text-h4 mb-4">Tenant Dashboard</h1>

    <!-- Current Preferences Card -->
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center">
        My Preferences
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="text"
          to="/preferences"
        >
          Edit Preferences
        </v-btn>
      </v-card-title>

      <v-card-text v-if="preferences">
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <div class="text-subtitle-1">Maximum Price</div>
            <div class="text-h6">${{ preferences.max_price }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-subtitle-1">Minimum Size</div>
            <div class="text-h6">{{ preferences.min_size }} sq ft</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-subtitle-1">Preferred Location</div>
            <div class="text-h6">{{ preferences.preferred_location }}</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-subtitle-1">Required Amenities</div>
            <v-chip-group>
              <v-chip
                v-for="amenity in preferences.required_amenities"
                :key="amenity"
                size="small"
              >
                {{ amenity }}
              </v-chip>
            </v-chip-group>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <div class="text-subtitle-1 mb-2">Importance Weights</div>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <div class="text-caption">Safety</div>
            <v-progress-linear
              :model-value="preferences.safety_weight * 100"
              color="primary"
              height="8"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}%</strong>
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
                <strong>{{ Math.round(value) }}%</strong>
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
                <strong>{{ Math.round(value) }}%</strong>
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
                <strong>{{ Math.round(value) }}%</strong>
              </template>
            </v-progress-linear>
          </v-col>
        </v-row>
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
        <v-card>
          <v-card-text class="text-center">
            <v-icon
              color="primary"
              size="48"
              class="mb-2"
            >
              mdi-home-search
            </v-icon>
            <h3 class="text-h6 mb-2">Search Rooms</h3>
            <p class="mb-4">Find your perfect room based on your preferences</p>
            <v-btn
              color="primary"
              to="/search"
            >
              Search Now
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text class="text-center">
            <v-icon
              color="primary"
              size="48"
              class="mb-2"
            >
              mdi-tune
            </v-icon>
            <h3 class="text-h6 mb-2">Update Preferences</h3>
            <p class="mb-4">Modify your preferences to get better matches</p>
            <v-btn
              color="primary"
              to="/preferences"
            >
              Update Now
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-text class="text-center">
            <v-icon
              color="primary"
              size="48"
              class="mb-2"
            >
              mdi-history
            </v-icon>
            <h3 class="text-h6 mb-2">Recent Views</h3>
            <p class="mb-4">Check your recently viewed rooms</p>
            <v-btn
              color="primary"
              @click="showRecentlyViewed"
            >
              View History
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recently Viewed Rooms -->
    <v-dialog v-model="recentlyViewedDialog" max-width="800">
      <v-card>
        <v-card-title>Recently Viewed Rooms</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item
              v-for="room in recentlyViewed"
              :key="room.id"
              :title="room.title"
              :subtitle="`$${room.price} - ${room.location}`"
              @click="viewRoom(room)"
            >
              <template v-slot:prepend>
                <v-avatar size="48">
                  <v-img :src="room.image_url" cover></v-img>
                </v-avatar>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            @click="recentlyViewedDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
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
    const response = await axios.get('/tenant/preferences')
    if (response.data) {
      preferences.value = {
        ...response.data,
        required_amenities: response.data.required_amenities
      }
    }
  } catch (error) {
    console.error('Error fetching preferences:', error)
  }
}

const fetchRecentlyViewed = async () => {
  try {
    const response = await axios.get('/tenant/recently-viewed')
    recentlyViewed.value = response.data
  } catch (error) {
    console.error('Error fetching recently viewed rooms:', error)
  }
}

const showRecentlyViewed = () => {
  if (recentlyViewed.value.length === 0) {
    snackbarText.value = 'No recently viewed rooms'
    snackbarColor.value = 'info'
    snackbar.value = true
    return
  }
  recentlyViewedDialog.value = true
}

const viewRoom = (room) => {
  recentlyViewedDialog.value = false
  router.push(`/search?room=${room.id}`)
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