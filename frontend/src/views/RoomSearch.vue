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

    <!-- Search Stats -->
    <v-row class="mb-4">
      <v-col cols="12" sm="4">
        <v-card>
          <v-card-text class="text-center">
            <div class="text-h5 mb-1">{{ searchResults?.summary?.total_rooms || 0 }}</div>
            <div class="text-subtitle-1">Total Rooms</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card 
          :color="searchResults?.summary?.perfect_matches_count ? 'success' : undefined"
          :variant="searchResults?.summary?.perfect_matches_count ? 'flat' : 'outlined'"
        >
          <v-card-text class="text-center">
            <div class="text-h5 mb-1">{{ searchResults?.summary?.perfect_matches_count || 0 }}</div>
            <div class="text-subtitle-1">Perfect Matches</div>
            <div class="text-caption">{{ searchResults?.summary?.categories?.perfect_match }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card 
          :color="searchResults?.summary?.excellent_matches_count ? 'info' : undefined"
          :variant="searchResults?.summary?.excellent_matches_count ? 'flat' : 'outlined'"
        >
          <v-card-text class="text-center">
            <div class="text-h5 mb-1">{{ searchResults?.summary?.excellent_matches_count || 0 }}</div>
            <div class="text-subtitle-1">Excellent Matches</div>
            <div class="text-caption">{{ searchResults?.summary?.categories?.excellent_match }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Search Filters -->
    <v-card class="mb-6">
      <v-card-title>Search Filters</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.max_price"
              label="Maximum Price"
              type="number"
              prefix="₱"
              clearable
              hint="Leave empty to use preference"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.min_capacity"
              label="Minimum Capacity"
              type="number"
              clearable
              hint="Leave empty to use preference"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filters.location"
              label="Location"
              clearable
              hint="Leave empty to use preference"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-combobox
              v-model="filters.amenities"
              :items="commonAmenities"
              label="Required Amenities"
              multiple
              chips
              clearable
              hint="Leave empty to use preference"
              persistent-hint
            ></v-combobox>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.min_safety_score"
              label="Minimum Safety Score"
              type="number"
              :min="1"
              :max="10"
              :step="1"
              clearable
              hint="1-10 scale"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.min_cleanliness_score"
              label="Minimum Cleanliness Score"
              type="number"
              :min="1"
              :max="10"
              :step="1"
              clearable
              hint="1-10 scale"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.min_accessibility_score"
              label="Minimum Accessibility Score"
              type="number"
              :min="1"
              :max="10"
              :step="1"
              clearable
              hint="1-10 scale"
              persistent-hint
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.max_noise_level"
              label="Maximum Noise Level"
              type="number"
              :min="1"
              :max="10"
              :step="1"
              clearable
              hint="1-10 scale (lower is better)"
              persistent-hint
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row class="mt-4">
          <v-col cols="12" class="text-center">
            <v-btn
              color="primary"
              :loading="loading"
              @click="searchRooms"
              class="mr-2"
            >
              Search Rooms
            </v-btn>
            <v-btn
              variant="outlined"
              @click="resetFilters"
              :disabled="loading"
            >
              Reset Filters
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Search Results -->
    <template v-if="!loading && searchPerformed">
      <!-- Summary Section -->
      <v-card class="mb-6" v-if="searchResults.summary">
        <v-card-title>Search Results Summary</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <div class="text-subtitle-1">Total Rooms Found</div>
              <div class="text-h5">{{ searchResults.summary.total_rooms }}</div>
            </v-col>
            <v-col cols="12" sm="6" md="8">
              <div class="text-subtitle-1">Match Categories</div>
              <v-chip-group>
                <v-chip color="success" v-if="searchResults.summary.perfect_matches_count">
                  Perfect ({{ searchResults.summary.perfect_matches_count }})
                </v-chip>
                <v-chip color="info" v-if="searchResults.summary.excellent_matches_count">
                  Excellent ({{ searchResults.summary.excellent_matches_count }})
                </v-chip>
                <v-chip color="primary" v-if="searchResults.summary.good_matches_count">
                  Good ({{ searchResults.summary.good_matches_count }})
                </v-chip>
                <v-chip color="warning" v-if="searchResults.summary.fair_matches_count">
                  Fair ({{ searchResults.summary.fair_matches_count }})
                </v-chip>
                <v-chip v-if="searchResults.summary.other_matches_count">
                  Other ({{ searchResults.summary.other_matches_count }})
                </v-chip>
              </v-chip-group>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Results Grid -->
      <v-row>
        <template v-if="searchResults.all_rooms && searchResults.all_rooms.length > 0">
          <v-col 
            v-for="room in searchResults.all_rooms" 
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              @click="viewRoom(room)"
              class="room-card"
              :class="getMatchClass(room.comprehensive_score)"
            >
              <v-img
                :src="room.image_urls?.[0] || '/placeholder-room.jpg'"
                height="200"
                cover
              >
                <template v-slot:placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-progress-circular
                      indeterminate
                      color="primary"
                    ></v-progress-circular>
                  </div>
                </template>
              </v-img>

              <v-card-title>
                {{ room.title }}
                <v-chip
                  :color="getMatchColor(room.comprehensive_score)"
                  size="small"
                  class="ml-2"
                >
                  {{ Math.round(room.comprehensive_score) }}% Match
                </v-chip>
              </v-card-title>

              <v-card-text>
                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-1">mdi-currency-php</v-icon>
                  <span class="text-h6">{{ room.price }}</span>
                  <v-spacer></v-spacer>
                  <v-icon size="small" class="mr-1">mdi-account-group</v-icon>
                  <span>{{ room.capacity }} person(s)</span>
                </div>

                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
                  <span class="text-truncate">{{ room.location }}</span>
                </div>

                <v-divider class="my-2"></v-divider>

                <div class="scores-grid">
                  <div class="score-item">
                    <v-icon size="small" color="success">mdi-shield-check</v-icon>
                    <span>{{ room.safety_score }}/10</span>
                  </div>
                  <div class="score-item">
                    <v-icon size="small" color="info">mdi-broom</v-icon>
                    <span>{{ room.cleanliness_score }}/10</span>
                  </div>
                  <div class="score-item">
                    <v-icon size="small" color="primary">mdi-transit-connection</v-icon>
                    <span>{{ room.accessibility_score }}/10</span>
                  </div>
                  <div class="score-item">
                    <v-icon size="small" color="warning">mdi-volume-medium</v-icon>
                    <span>{{ room.noise_level }}/10</span>
                  </div>
                </div>

                <v-chip-group class="mt-2">
                  <v-chip
                    v-for="amenity in room.amenities.slice(0, 3)"
                    :key="amenity"
                    size="x-small"
                    variant="outlined"
                  >
                    {{ amenity }}
                  </v-chip>
                  <v-chip
                    v-if="room.amenities.length > 3"
                    size="x-small"
                    variant="outlined"
                  >
                    +{{ room.amenities.length - 3 }} more
                  </v-chip>
                </v-chip-group>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  variant="text"
                  color="primary"
                  @click.stop="viewRoom(room)"
                >
                  View Details
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </template>
        <v-col v-else cols="12" class="text-center">
          <v-alert
            type="info"
            text="No rooms found matching your criteria. Try adjusting your filters."
          ></v-alert>
        </v-col>
      </v-row>
    </template>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/plugins/axios'
import RoomCard from '@/components/RoomCard.vue'

const router = useRouter()
const loading = ref(false)
const showFilters = ref(null)
const hasPreferences = ref(true)
const searchPerformed = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

// Search results data
const searchResults = ref({
  summary: {
    total_rooms: 0,
    perfect_matches_count: 0,
    excellent_matches_count: 0,
    good_matches_count: 0,
    fair_matches_count: 0,
    other_matches_count: 0,
    categories: {
      perfect_match: '90% or higher with all amenities and within budget',
      excellent_match: '85-89%',
      good_match: '75-84%',
      fair_match: '60-74%',
      other_match: 'Below 60%'
    }
  },
  suggestions: {
    perfect_matches: [],
    excellent_matches: [],
    good_matches: [],
    fair_matches: [],
    other_matches: []
  },
  all_rooms: []
})

// Filters
const filters = ref({
  max_price: null,
  min_capacity: null,
  location: '',
  amenities: [],
  min_safety_score: null,
  min_cleanliness_score: null,
  min_accessibility_score: null,
  max_noise_level: null
})

const sortOptions = [
  { title: 'Match Score (High to Low)', value: 'score' },
  { title: 'Price (Low to High)', value: 'price_asc' },
  { title: 'Price (High to Low)', value: 'price_desc' },
  { title: 'Size (Largest First)', value: 'size_desc' },
  { title: 'Size (Smallest First)', value: 'size_asc' }
]
const sortBy = ref('score')

// Computed properties
const activeFiltersCount = computed(() => {
  let count = 0
  if (filters.value.max_price) count++
  if (filters.value.min_capacity) count++
  if (filters.value.location) count++
  if (filters.value.amenities.length > 0) count++
  if (filters.value.min_safety_score) count++
  if (filters.value.max_noise_level) count++
  if (filters.value.min_accessibility_score) count++
  if (filters.value.min_cleanliness_score) count++
  return count
})

const commonAmenities = [
  'WiFi',
  'Air Conditioning',
  'Private Bathroom',
  'Kitchen Access',
  'Laundry',
  'Study Area',
  'Parking',
  'Security System',
  'Water Heater',
  'Furnished'
]

// Methods
const getScoreColor = (score) => {
  if (score >= 8) return 'success'
  if (score >= 6) return 'info'
  if (score >= 4) return 'warning'
  return 'error'
}

const clearFilters = () => {
  filters.value = {
    max_price: null,
    min_capacity: null,
    location: '',
    amenities: [],
    min_safety_score: null,
    min_cleanliness_score: null,
    min_accessibility_score: null,
    max_noise_level: null
  }
  searchRooms()
}

const searchRooms = async () => {
  try {
    loading.value = true
    searchPerformed.value = true

    // Build query parameters
    const params = new URLSearchParams()
    if (filters.value.max_price) params.append('max_price', filters.value.max_price)
    if (filters.value.min_capacity) params.append('min_capacity', filters.value.min_capacity)
    if (filters.value.location) params.append('location', filters.value.location)
    if (filters.value.amenities?.length) params.append('amenities', JSON.stringify(filters.value.amenities))
    if (filters.value.min_safety_score) params.append('min_safety_score', filters.value.min_safety_score)
    if (filters.value.min_cleanliness_score) params.append('min_cleanliness_score', filters.value.min_cleanliness_score)
    if (filters.value.min_accessibility_score) params.append('min_accessibility_score', filters.value.min_accessibility_score)
    if (filters.value.max_noise_level) params.append('max_noise_level', filters.value.max_noise_level)

    const response = await axios.get(`${import.meta.env.VITE_API_URL}/tenant/search?${params.toString()}`)
    searchResults.value = response.data

  } catch (error) {
    console.error('Error searching rooms:', error)
    snackbarText.value = error.response?.data?.error || 'Error searching rooms'
    snackbarColor.value = 'error'
    snackbar.value = true
    searchResults.value = { summary: null, all_rooms: [] }
  } finally {
    loading.value = false
  }
}

const viewRoom = (room) => {
  router.push(`/rooms/${room.id}`)
}

const getMatchClass = (score) => {
  if (score >= 90) return 'perfect-match'
  if (score >= 85) return 'excellent-match'
  if (score >= 75) return 'good-match'
  if (score >= 60) return 'fair-match'
  return 'other-match'
}

const getMatchColor = (score) => {
  if (score >= 90) return 'success'
  if (score >= 85) return 'info'
  if (score >= 75) return 'primary'
  if (score >= 60) return 'warning'
  return 'grey'
}

const checkPreferences = async () => {
  try {
    console.log('Checking preferences...')
    const response = await axios.get('/tenant/preferences', {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    })
    console.log('Preferences response:', response.data)
    hasPreferences.value = !!response.data
    if (response.data) {
      // Initialize filters with preferences
      filters.value = {
        max_price: response.data.max_price,
        min_capacity: response.data.min_capacity,
        location: response.data.preferred_location,
        amenities: response.data.required_amenities || [],
        min_safety_score: Math.max(1, Math.round(response.data.safety_weight * 10)),
        max_noise_level: Math.min(10, Math.round((1 - response.data.noise_level_weight) * 10)),
        min_accessibility_score: Math.max(1, Math.round(response.data.accessibility_weight * 10)),
        min_cleanliness_score: Math.max(1, Math.round(response.data.cleanliness_weight * 10))
      }
    }
  } catch (error) {
    console.error('Error checking preferences:', error)
    hasPreferences.value = false
  }
}

// Initialize on component mount
onMounted(async () => {
  loading.value = true
  try {
    await checkPreferences()
    await searchRooms()
  } catch (error) {
    console.error('Error loading initial data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.room-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.room-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

.scores-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.perfect-match {
  border: 2px solid rgb(var(--v-theme-success)) !important;
}

.excellent-match {
  border: 2px solid rgb(var(--v-theme-info)) !important;
}

.good-match {
  border: 2px solid rgb(var(--v-theme-primary)) !important;
}

.fair-match {
  border: 2px solid rgb(var(--v-theme-warning)) !important;
}

.other-match {
  border: 2px solid rgb(var(--v-theme-grey)) !important;
}
</style> 