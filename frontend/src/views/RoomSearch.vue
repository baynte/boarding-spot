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
    <!-- <v-row class="mb-4">
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
    </v-row> -->

    <!-- Search Filters -->
    <v-card class="mb-6">
      <v-card-title>Search Filters</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.maxPrice"
              label="Maximum Price"
              type="number"
              prefix="₱"
              clearable
              :loading="loading"
              :disabled="loading"
              density="compact"
              variant="outlined"
              hide-details
              class="mb-3"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model.number="filters.minCapacity"
              label="Minimum Capacity"
              type="number"
              min="1"
              hint="Minimum number of tenants"
              persistent-hint
              clearable
              :loading="loading"
              :disabled="loading"
              density="compact"
              variant="outlined"
              hide-details
              class="mb-3"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filters.location"
              label="Location"
              clearable
              :loading="loading"
              :disabled="loading"
              density="compact"
              variant="outlined"
              hide-details
              prepend-inner-icon="mdi-map-marker"
              class="mb-3"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              label="Sort By"
              density="compact"
              variant="outlined"
              hide-details
              class="mb-3"
            ></v-select>
          </v-col>

          <v-col cols="12">
            <v-combobox
              v-model="filters.amenities"
              :items="commonAmenities"
              label="Required Amenities"
              multiple
              chips
              closable-chips
              clearable
              :loading="loading"
              :disabled="loading"
              density="comfortable"
              variant="outlined"
              hide-details
            ></v-combobox>
          </v-col>
        </v-row>

        <!-- Score Filters -->
        <v-row class="mt-4">
          <v-col cols="12">
            <div class="text-subtitle-1 mb-2">Score Filters</div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="d-flex align-center justify-space-between mb-1">
              <span class="text-body-2">Min Safety Score</span>
              <v-chip size="x-small" :color="getScoreColor(filters.minSafetyScore)">{{ filters.minSafetyScore }}/10</v-chip>
            </div>
            <v-slider
              v-model="filters.minSafetyScore"
              :min="1"
              :max="10"
              :step="0.5"
              :color="getScoreColor(filters.minSafetyScore)"
              track-color="grey-lighten-1"
              show-ticks="always"
              :tick-size="4"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="d-flex align-center justify-space-between mb-1">
              <span class="text-body-2">Max Noise Level</span>
              <v-chip size="x-small" :color="getScoreColor(10 - filters.maxNoiseLevel)">{{ filters.maxNoiseLevel }}/10</v-chip>
            </div>
            <v-slider
              v-model="filters.maxNoiseLevel"
              :min="1"
              :max="10"
              :step="0.5"
              :color="getScoreColor(10 - filters.maxNoiseLevel)"
              track-color="grey-lighten-1"
              show-ticks="always"
              :tick-size="4"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="d-flex align-center justify-space-between mb-1">
              <span class="text-body-2">Min Accessibility</span>
              <v-chip size="x-small" :color="getScoreColor(filters.minAccessibilityScore)">{{ filters.minAccessibilityScore }}/10</v-chip>
            </div>
            <v-slider
              v-model="filters.minAccessibilityScore"
              :min="1"
              :max="10"
              :step="0.5"
              :color="getScoreColor(filters.minAccessibilityScore)"
              track-color="grey-lighten-1"
              show-ticks="always"
              :tick-size="4"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="d-flex align-center justify-space-between mb-1">
              <span class="text-body-2">Min Cleanliness</span>
              <v-chip size="x-small" :color="getScoreColor(filters.minCleanlinessScore)">{{ filters.minCleanlinessScore }}/10</v-chip>
            </div>
            <v-slider
              v-model="filters.minCleanlinessScore"
              :min="1"
              :max="10"
              :step="0.5"
              :color="getScoreColor(filters.minCleanlinessScore)"
              track-color="grey-lighten-1"
              show-ticks="always"
              :tick-size="4"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col cols="12" class="d-flex justify-end">
            <v-btn
              color="error"
              variant="text"
              @click="clearFilters"
              :disabled="loading"
              class="me-2"
            >
              Clear All
            </v-btn>
            <v-btn
              color="primary"
              @click="searchRooms"
              :loading="loading"
              :disabled="loading"
            >
              Search
              <v-chip
                v-if="activeFiltersCount > 0"
                size="x-small"
                class="ml-2"
              >
                {{ activeFiltersCount }} active
              </v-chip>
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
            <RoomCard :room="room" />
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
  maxPrice: null,
  minCapacity: null,
  location: '',
  amenities: [],
  minSafetyScore: 1,
  maxNoiseLevel: 10,
  minAccessibilityScore: 1,
  minCleanlinessScore: 1,
  sortBy: 'match_desc'
})

const sortOptions = [
  { title: 'Best Match', value: 'match_desc' },
  { title: 'Price (Low to High)', value: 'price_asc' },
  { title: 'Price (High to Low)', value: 'price_desc' },
  { title: 'Capacity (Largest First)', value: 'capacity_desc' },
  { title: 'Capacity (Smallest First)', value: 'capacity_asc' }
]
const sortBy = ref('match_desc')

// Computed properties
const activeFiltersCount = computed(() => {
  let count = 0
  if (filters.value.maxPrice) count++
  if (filters.value.minCapacity) count++
  if (filters.value.location) count++
  if (filters.value.amenities.length > 0) count++
  if (filters.value.minSafetyScore > 1) count++
  if (filters.value.maxNoiseLevel < 10) count++
  if (filters.value.minAccessibilityScore > 1) count++
  if (filters.value.minCleanlinessScore > 1) count++
  if (sortBy.value !== 'match_desc') count++
  return count
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
  'Closet',
  'CCTV',
  'Fire Exits',
  'Common CR',
  'Appliances',
  'Receiving Area',
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
    maxPrice: null,
    minCapacity: null,
    location: '',
    amenities: [],
    minSafetyScore: 1,
    maxNoiseLevel: 10,
    minAccessibilityScore: 1,
    minCleanlinessScore: 1,
    sortBy: 'match_desc'
  }
  searchRooms()
}

const searchRooms = async () => {
  loading.value = true
  searchPerformed.value = true
  try {
    const params = {
      max_price: filters.value.maxPrice,
      min_capacity: filters.value.minCapacity,
      location: filters.value.location,
      amenities: filters.value.amenities,
      min_safety_score: filters.value.minSafetyScore,
      max_noise_level: filters.value.maxNoiseLevel,
      min_accessibility_score: filters.value.minAccessibilityScore,
      min_cleanliness_score: filters.value.minCleanlinessScore,
      sort_by: sortBy.value
    }
    
    const response = await axios.get('/tenant/search', { params })
    searchResults.value = response.data
    if (!response.data.all_rooms) {
      searchResults.value.all_rooms = []
    }

  } catch (error) {
    console.error('Error searching rooms:', error)
    snackbarText.value = error.response?.data?.error || 'Error searching rooms'
    snackbarColor.value = 'error'
    snackbar.value = true
    searchResults.value = { 
      summary: {
        total_rooms: 0,
        perfect_matches_count: 0,
        excellent_matches_count: 0,
        good_matches_count: 0,
        fair_matches_count: 0,
        other_matches_count: 0
      }, 
      all_rooms: [] 
    }
  } finally {
    loading.value = false
  }
}

const viewRoom = (room) => {
  router.push(`/rooms/₱{room.id}`)
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
        maxPrice: response.data.max_price,
        minCapacity: response.data.min_capacity,
        location: response.data.preferred_location,
        amenities: response.data.required_amenities || [],
        minSafetyScore: Math.max(1, Math.round(response.data.safety_weight * 10)),
        maxNoiseLevel: Math.min(10, Math.round((1 - response.data.noise_level_weight) * 10)),
        minAccessibilityScore: Math.max(1, Math.round(response.data.accessibility_weight * 10)),
        minCleanlinessScore: Math.max(1, Math.round(response.data.cleanliness_weight * 10)),
        sortBy: 'match_desc'
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

/* Mobile Responsive Styles */
@media (max-width: 600px) {
  .v-card-title {
    font-size: 1.25rem !important;
  }

  .text-h4 {
    font-size: 1.5rem !important;
  }

  .v-chip-group {
    flex-wrap: wrap;
  }

  .v-chip {
    margin-bottom: 4px;
  }

  .v-slider {
    margin-bottom: 24px;
  }
}
</style> 