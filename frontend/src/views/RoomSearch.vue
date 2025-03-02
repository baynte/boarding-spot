<template>
  <div>
    <h1 class="text-h4 mb-4 mt-10">Living Space Search</h1>

    <!-- Warning if preferences not set -->
    <v-alert v-if="!hasPreferences" type="warning" class="mb-4">
      Please set your preferences to get personalized room recommendations.
      <v-btn color="warning" variant="text" to="/preferences" class="ms-2"> Set Preferences </v-btn>
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
    <v-card class="mb-6" elevation="10" variant="elevated">
      <!-- Header with better visual separation -->
      <v-card-title class="d-flex align-center py-4 px-6 bg-primary text-white">
        <v-icon icon="mdi-filter-variant" class="me-2" />
        Search Filters
        <v-spacer></v-spacer>
        <v-chip
          v-if="activeFiltersCount > 0"
          color="white"
          text-color="primary"
          variant="outlined"
          size="small"
          class="font-weight-bold"
        >
          {{ activeFiltersCount }} filters active
        </v-chip>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- Basic Filters Section -->
        <section class="mb-6">
          <div class="d-flex align-center mb-4">
            <v-icon icon="mdi-tune" class="me-2" color="primary" />
            <span class="text-h6">Basic Filters</span>
          </div>
          <v-row dense>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model.number="filters.maxPrice"
                label="Maximum Price"
                type="number"
                clearable
                :loading="loading"
                :disabled="loading"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                prepend-inner-icon="mdi-currency-php"
                class="rounded-lg"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model.number="filters.minCapacity"
                label="Minimum Capacity"
                type="number"
                min="1"
                clearable
                :loading="loading"
                :disabled="loading"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                prepend-inner-icon="mdi-account-group"
                class="rounded-lg"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="filters.location"
                label="Location"
                clearable
                :loading="loading"
                :disabled="loading"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                prepend-inner-icon="mdi-map-marker"
                class="rounded-lg"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="filters.livingSpaceType"
                :items="livingSpaceTypes"
                label="Rental type"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                clearable
                prepend-inner-icon="mdi-home"
                class="rounded-lg"
              ></v-select>
            </v-col>
          </v-row>
        </section>

        <!-- Additional Options Section -->
        <section class="mb-6">  
          <div class="d-flex align-center mb-4">
            <v-icon icon="mdi-cog" class="me-2" color="primary"/>
            <span class="text-h6">Additional Options</span>
          </div>

          <v-row dense>
            <v-col cols="12" md="3">
              <v-select
                v-model="sortBy"
                :items="sortOptions"
                label="Sort Results By"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                prepend-inner-icon="mdi-sort"
                class="rounded-lg"
              ></v-select>
            </v-col>

            <v-col cols="12" md="9">
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
                hide-details="auto"
                prepend-inner-icon="mdi-star"
                class="rounded-lg"
              ></v-combobox>
            </v-col>
          </v-row>
        </section>

        <!-- Score Filters Section -->
        <v-row class="mt-4">
          <v-col cols="12">
            <div class="d-flex align-center mb-1">
              <v-icon icon="mdi-chart-bar" class="me-2" color="primary" />
              <span class="text-h6">Score Filters</span>
            </div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card variant="outlined" class="pa-3 rounded-lg">
              <div class="d-flex align-center justify-space-between mb-1">
                <v-icon size="22" color="primary">mdi-shield-check</v-icon>
                <span class="text-body-2 font-weight-bold">Min Safety Score</span>
                <v-chip size="x-small" :color="getScoreColor(filters.minSafetyScore)"
                  >{{ filters.minSafetyScore }}/10</v-chip
                >
              </div>
              <v-slider
                v-model="filters.minSafetyScore"
                :min="1"
                :max="10"
                :step="0.5"
                thumb-label
                :color="getScoreColor(filters.minSafetyScore)"
                track-color="grey-lighten-5"
                show-ticks="always"
                :tick-size="3"
                :loading="loading"
                :disabled="loading"
              ></v-slider>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card variant="outlined" class="pa-3 rounded-lg">
              <div class="d-flex align-center justify-space-between mb-1">
                <v-icon size="20" color="primary">mdi-broom</v-icon>
                <span class="text-body-2 font-weight-bold">Cleanliness</span>
                <v-chip size="x-small" :color="getScoreColor(filters.minCleanlinessScore)"
                  >{{ filters.minCleanlinessScore }}/10</v-chip
                >
              </div>
              <v-slider
                v-model="filters.minCleanlinessScore"
                :min="1"
                :max="10"
                :step="0.5"
                thumb-label
                :color="getScoreColor(filters.minCleanlinessScore)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
                :loading="loading"
                :disabled="loading"
              ></v-slider>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card variant="outlined" class="pa-3 rounded-lg">
              <div class="d-flex align-center justify-space-between mb-1">
                <v-icon size="22" color="primary">mdi-account-box</v-icon>
                <span class="text-body-2 font-weight-bold">Min Accessibility</span>
                <v-chip size="x-small" :color="getScoreColor(filters.minAccessibilityScore)"
                  >{{ filters.minAccessibilityScore }}/10</v-chip
                >
              </div>
              <v-slider
                v-model="filters.minAccessibilityScore"
                :min="1"
                :max="10"
                :step="0.5"
                thumb-label
                :color="getScoreColor(filters.minAccessibilityScore)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
                :loading="loading"
                :disabled="loading"
              ></v-slider>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card variant="outlined" class="pa-3 rounded-lg">
              <div class="d-flex align-center justify-space-between mb-1">
                <v-icon size="22" color="primary">mdi-volume-high</v-icon>
                <span class="text-body-2 font-weight-bold">Max Noise Level</span>
                <v-chip size="x-small" :color="getScoreColor(10 - filters.maxNoiseLevel)"
                  >{{ filters.maxNoiseLevel }}/10</v-chip
                >
              </div>
              <v-slider
                v-model="filters.maxNoiseLevel"
                :min="1"
                :max="10"
                :step="0.5"
                thumb-label
                :color="getScoreColor(10 - filters.maxNoiseLevel)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
                :loading="loading"
                :disabled="loading"
              ></v-slider>
            </v-card>
          </v-col>
        </v-row>

        <!-- Action Buttons -->
        <v-divider class="my-4"></v-divider>
        <div class="d-flex justify-end gap-3">
          <v-btn
            color="error"
            variant="outlined"
            @click="clearFilters"
            :disabled="loading"
            prepend-icon="mdi-refresh"
            class="mr-4"
            elevation="7"
          >
            Clear All
          </v-btn>
          <v-btn
            color="primary"
            @click="searchRooms"
            :loading="loading"
            :disabled="loading"
            prepend-icon="mdi-magnify"
            elevation="8"
          >
            Search
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!-- Map View -->
    <v-card class="mb-6" elevation="10" variant="elevated">
      <v-card-title class="d-flex align-center py-4 px-6 bg-primary text-white">
        <v-icon icon="mdi-map" class="me-2" />
        Map View
      </v-card-title>
      <v-card-text class="pa-0">
        <div class="map-container" style="height: 400px; position: relative">
          <leaflet-map
            :marker-lat-lng="selectedLocation"
            :popup-content="selectedLocationName"
            @marker-click="handleMarkerClick"
            class="rounded-b-lg"
          />
          <div class="map-overlay pa-3" v-if="!selectedLocation">
            <v-chip color="info" variant="flat" prepend-icon="mdi-information">
              Click on the map to select a location
            </v-chip>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <template v-if="!loading && searchPerformed">
      <!-- Summary Section -->
      <v-card
        class="mb-6 search-summary-card"
        elevation="10"
        variant="elevated"
        v-if="searchResults.summary"
        rounded="lg"
      >
        <v-card-item>
          <template v-slot:prepend>
            <v-icon icon="mdi-magnify" size="large" color="primary" class="mr-3"></v-icon>
          </template>
          <v-card-title class="text-h5 font-weight-bold pb-1">Search Results</v-card-title>
          <v-card-subtitle
            >Found {{ searchResults.summary.total_rooms }} rooms matching your
            criteria</v-card-subtitle
          >
        </v-card-item>

        <v-divider></v-divider>

        <v-card-text>
          <v-row align-items="center">
            <v-col cols="12" sm="5" md="4">
              <div class="d-flex align-center">
                <v-avatar color="primary" size="56" class="mr-4">
                  <span class="text-h5 font-weight-bold text-white">{{
                    searchResults.summary.total_rooms
                  }}</span>
                </v-avatar>
                <div>
                  <div class="text-subtitle-1 font-weight-medium">Total Rooms</div>
                  <div class="text-caption text-medium-emphasis">Available for booking</div>
                </div>
              </div>
            </v-col>

            <v-col cols="12" sm="7" md="8">
              <div class="text-subtitle-1 font-weight-medium mb-2">Match Quality</div>
              <v-chip-group class="match-quality-chips">
                <v-chip
                  v-if="searchResults.summary.perfect_matches_count"
                  color="success"
                  variant="elevated"
                  size="large"
                  label
                  class="font-weight-medium"
                >
                  <v-icon start size="small">mdi-check-circle</v-icon>
                  Perfect ({{ searchResults.summary.perfect_matches_count }})
                </v-chip>

                <v-chip
                  v-if="searchResults.summary.excellent_matches_count"
                  color="info"
                  variant="elevated"
                  size="large"
                  label
                  class="font-weight-medium"
                >
                  <v-icon start size="small">mdi-thumb-up</v-icon>
                  Excellent ({{ searchResults.summary.excellent_matches_count }})
                </v-chip>

                <v-chip
                  v-if="searchResults.summary.good_matches_count"
                  color="primary"
                  variant="elevated"
                  size="large"
                  label
                  class="font-weight-medium"
                >
                  <v-icon start size="small">mdi-star</v-icon>
                  Good ({{ searchResults.summary.good_matches_count }})
                </v-chip>

                <v-chip
                  v-if="searchResults.summary.fair_matches_count"
                  color="warning"
                  variant="elevated"
                  size="large"
                  label
                  class="font-weight-medium"
                >
                  <v-icon start size="small">mdi-alert</v-icon>
                  Fair ({{ searchResults.summary.fair_matches_count }})
                </v-chip>

                <v-chip
                  v-if="searchResults.summary.other_matches_count"
                  color="grey"
                  variant="elevated"
                  size="large"
                  label
                  class="font-weight-medium"
                >
                  <v-icon start size="small">mdi-dots-horizontal</v-icon>
                  Other ({{ searchResults.summary.other_matches_count }})
                </v-chip>
              </v-chip-group>
            </v-col>
          </v-row>

          <v-row v-if="searchResults.filters" class="mt-2">
            <v-col cols="12">
              <div class="text-subtitle-1 font-weight-medium mb-2">Applied Filters</div>
              <v-chip-group>
                <v-chip
                  v-for="(value, key) in searchResults.filters"
                  :key="key"
                  size="small"
                  closable
                  variant="outlined"
                  color="grey-darken-1"
                  @click:close="removeFilter(key)"
                >
                  {{ formatFilterName(key) }}: {{ value }}
                </v-chip>
              </v-chip-group>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Results Grid -->
      <v-row>
        <template v-if="searchResults.all_rooms && searchResults.all_rooms.length > 0">
          <v-col v-for="room in searchResults.all_rooms" :key="room.id" cols="12" sm="6" md="4">
            <RoomCard :room="room" :user-type="userType" />
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
import LeafletMap from '@/components/LeafletMap.vue'

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
      other_match: 'Below 60%',
    },
  },
  suggestions: {
    perfect_matches: [],
    excellent_matches: [],
    good_matches: [],
    fair_matches: [],
    other_matches: [],
  },
  all_rooms: [],
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
  sortBy: 'match_desc',
  livingSpaceType: null,
})

const sortOptions = [
  { title: 'Best Match', value: 'match_desc' },
  { title: 'Price (Low to High)', value: 'price_asc' },
  { title: 'Price (High to Low)', value: 'price_desc' },
  { title: 'Capacity (Largest First)', value: 'capacity_desc' },
  { title: 'Capacity (Smallest First)', value: 'capacity_asc' },
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
  if (filters.value.livingSpaceType) count++
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
  'Furnished',
  'Single bed',
  'Double-Deck Bed',
  'Refrigerator',
  'Washing Machine',
  'Microwave',
  'Fan',
  'Gas/Induction Stove',
  'Rice cooker',
  'Pet-friendly',
  'Security Keycard',
  'Security Fingerprint',
  'Security Guard',
  'Elevator',
  'Convenient Store',
  'Phone',
  'Electricity Included',
  'Water included',
  'Gym/Fitness Gym',
  'Swimming Pool',
]

const livingSpaceTypes = ['Boarding House', 'Apartment', 'House', 'Dormitory', 'Condo Unit']

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
    sortBy: 'match_desc',
    livingSpaceType: null,
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
      amenities: JSON.stringify(filters.value.amenities),
      min_safety_score: filters.value.minSafetyScore,
      max_noise_level: filters.value.maxNoiseLevel,
      min_accessibility_score: filters.value.minAccessibilityScore,
      min_cleanliness_score: filters.value.minCleanlinessScore,
      living_space_type: filters.value.livingSpaceType,
      sort_by: sortBy.value,
    }

    const response = await axios.get('/tenant/search', {
      params,
      paramsSerializer: {
        encode: (param) => encodeURIComponent(param),
        serialize: (params) => {
          const searchParams = new URLSearchParams()
          for (const key in params) {
            if (params[key] != null) {
              searchParams.append(key, params[key])
            }
          }
          return searchParams.toString()
        },
      },
    })
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
        other_matches_count: 0,
      },
      all_rooms: [],
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
        Pragma: 'no-cache',
      },
    })
    console.log('Raw preferences response:', response)
    console.log('Preferences data:', response.data)
    hasPreferences.value = !!response.data
    if (response.data) {
      console.log('Setting filters with preferences...')
      // Initialize filters with preferences
      const newFilters = {
        maxPrice: response.data.max_price || null,
        minCapacity: response.data.min_capacity || null,
        location: response.data.preferred_location || '',
        amenities: response.data.required_amenities || [], // Backend already sends parsed JSON
        minSafetyScore: Math.max(1, Math.round(response.data.safety_weight * 10)),
        maxNoiseLevel: Math.min(10, Math.round((1 - response.data.noise_level_weight) * 10)),
        minAccessibilityScore: Math.max(1, Math.round(response.data.accessibility_weight * 10)),
        minCleanlinessScore: Math.max(1, Math.round(response.data.cleanliness_weight * 10)),
        livingSpaceType: response.data.living_space_type || null,
      }
      console.log('New filters:', newFilters)
      filters.value = newFilters

      // After setting filters, trigger a search to show results based on preferences
      console.log('Triggering initial search with preferences...')
      await searchRooms()
    }
  } catch (error) {
    console.error('Error checking preferences:', error)
    if (error.response) {
      console.error('Error response:', error.response.data)
      console.error('Error status:', error.response.status)
    }
    hasPreferences.value = false
  }
}

const selectedLocation = ref(null)
const selectedLocationName = ref('')

const handleMarkerClick = () => {
  console.log('Marker clicked')
}

// Add user type state
const userType = ref('tenant') // Default to tenant

// Get user type on mount
const getUserType = async () => {
  try {
    const token = localStorage.getItem('token')
    if (token) {
      const response = await axios.get('/auth/user-type')
      userType.value = response.data.user_type
    }
  } catch (error) {
    console.error('Error getting user type:', error)
  }
}

// Initialize on component mount
onMounted(async () => {
  await getUserType()
  await checkPreferences()
  await searchRooms()
})
</script>

<style scoped>
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.room-card {
  transition:
    transform 0.2s,
    box-shadow 0.2s;
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

.search-summary-card {
  border-left: 4px solid var(--v-primary-base);
  transition: all 0.3s ease;
}

.search-summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.match-quality-chips .v-chip {
  margin: 4px;
  transition: all 0.2s ease;
}

.match-quality-chips .v-chip:hover {
  transform: scale(1.05);
}
</style>
