<template>
  <div>
    <h1 class="text-h4 mb-4">Room Search</h1>

    <!-- Warning if preferences not set -->
    <v-alert
      v-if="!hasPreferences"
      type="warning"
      class="mb-4"
    >
      Please set your preferences to get personalized room recommendations.
      <v-btn
        color="warning"
        variant="text"
        to="/preferences"
        class="ms-2"
      >
        Set Preferences
      </v-btn>
    </v-alert>

    <!-- Search Filters -->
    <v-card class="mb-4">
      <v-card-title>Filters</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="filters.maxPrice"
              label="Max Price"
              type="number"
              prefix="$"
              clearable
              @update:model-value="searchRooms"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="filters.minSize"
              label="Min Size (sq ft)"
              type="number"
              clearable
              @update:model-value="searchRooms"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="filters.location"
              label="Location"
              clearable
              @update:model-value="searchRooms"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-combobox
              v-model="filters.amenities"
              :items="commonAmenities"
              label="Required Amenities"
              multiple
              chips
              clearable
              @update:model-value="searchRooms"
            ></v-combobox>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Results -->
    <v-row>
      <v-col
        v-for="room in rooms"
        :key="room.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card>
          <v-img
            :src="room.image_url"
            height="200"
            cover
            class="bg-grey-lighten-2"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
              </v-row>
            </template>
          </v-img>

          <v-card-title>{{ room.title }}</v-card-title>

          <v-card-text>
            <div class="text-h6 mb-2">${{ room.price }}/month</div>
            <div class="mb-2">{{ room.location }}</div>
            <div class="mb-2">{{ room.size }} sq ft</div>
            <div class="mb-2">{{ room.description }}</div>

            <v-chip-group>
              <v-chip
                v-for="amenity in room.amenities"
                :key="amenity"
                size="small"
              >
                {{ amenity }}
              </v-chip>
            </v-chip-group>

            <v-divider class="my-3"></v-divider>

            <v-row>
              <v-col cols="6">
                <div class="text-caption">Safety</div>
                <v-rating
                  :model-value="room.safety_score / 2"
                  color="amber"
                  density="compact"
                  half-increments
                  readonly
                  size="small"
                ></v-rating>
              </v-col>
              <v-col cols="6">
                <div class="text-caption">Cleanliness</div>
                <v-rating
                  :model-value="room.cleanliness_score / 2"
                  color="amber"
                  density="compact"
                  half-increments
                  readonly
                  size="small"
                ></v-rating>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <div class="text-caption">Accessibility</div>
                <v-rating
                  :model-value="room.accessibility_score / 2"
                  color="amber"
                  density="compact"
                  half-increments
                  readonly
                  size="small"
                ></v-rating>
              </v-col>
              <v-col cols="6">
                <div class="text-caption">Noise Level</div>
                <v-rating
                  :model-value="(10 - room.noise_level) / 2"
                  color="amber"
                  density="compact"
                  half-increments
                  readonly
                  size="small"
                ></v-rating>
              </v-col>
            </v-row>

            <div v-if="room.topsis_score" class="mt-2">
              <div class="text-caption">Match Score</div>
              <v-progress-linear
                :model-value="room.topsis_score * 100"
                color="primary"
                height="8"
              >
                <template v-slot:default="{ value }">
                  <strong>{{ Math.round(value) }}%</strong>
                </template>
              </v-progress-linear>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="text"
              @click="contactLandlord(room)"
            >
              Contact Landlord
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const rooms = ref([])
const hasPreferences = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const filters = ref({
  maxPrice: null,
  minSize: null,
  location: '',
  amenities: []
})

const commonAmenities = [
  'WiFi',
  'Air Conditioning',
  'Heating',
  'Kitchen',
  'Laundry',
  'Parking',
  'TV',
  'Private Bathroom',
  'Study Desk',
  'Closet'
]

onMounted(async () => {
  await checkPreferences()
  await searchRooms()
})

const checkPreferences = async () => {
  try {
    const response = await axios.get('http://localhost:5000/tenant/preferences')
    hasPreferences.value = !!response.data
  } catch (error) {
    hasPreferences.value = false
  }
}

const searchRooms = async () => {
  try {
    const response = await axios.get('http://localhost:5000/tenant/search', {
      params: {
        max_price: filters.value.maxPrice,
        min_size: filters.value.minSize,
        location: filters.value.location,
        amenities: filters.value.amenities?.length ? JSON.stringify(filters.value.amenities) : undefined
      }
    })
    rooms.value = response.data
  } catch (error) {
    snackbarText.value = 'Error fetching rooms'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const contactLandlord = (room) => {
  // This would typically open a chat or messaging interface
  snackbarText.value = 'Contact feature coming soon!'
  snackbarColor.value = 'info'
  snackbar.value = true
}
</script> 