<template>
  <div class="pt-10">
    <!-- <h1 class="text-h4 mb-4 mt-10">Rental type Search</h1> -->

    <!-- Warning if preferences not set -->
    <v-alert v-if="!hasPreferences" type="warning" class="mb-4">
      Please set your preferences to get personalized room recommendations.
      <v-btn color="warning" variant="text" to="/preferences" class="ms-2"> Set Preferences </v-btn>
    </v-alert>

    <v-row>
      <!-- Left Sidebar with Filters -->
      <v-col cols="12" md="3" lg="3" class="pr-md-4">
        <v-card class="mb-6 sticky-sidebar" elevation="10" variant="elevated">
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

          <v-card-text class="pa-4">
            <!-- Basic Filters Section -->
            <section class="mb-4">
              <div class="d-flex align-center mb-3">
                <v-icon icon="mdi-tune" class="me-2" color="primary" />
                <span class="text-subtitle-1 font-weight-medium">Basic Filters</span>
              </div>
              
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
                class="rounded-lg mb-3"
              ></v-text-field>

              <v-text-field
                v-model.number="filters.maxDistance"
                label="Max Distance from SMCC (km)"
                type="number"
                min="0"
                clearable
                :loading="loading"
                :disabled="loading"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                prepend-inner-icon="mdi-map-marker-distance"
                class="rounded-lg mb-3"
                :class="{'active-filter': filters.maxDistance !== null}"
              ></v-text-field>

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
                class="rounded-lg mb-3"
              ></v-text-field>

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
                class="rounded-lg mb-3"
              ></v-text-field>

              <v-select
                v-model="filters.livingSpaceType"
                :items="livingSpaceTypes"
                label="Rental type"
                density="comfortable"
                variant="outlined"
                hide-details="auto"
                clearable
                prepend-inner-icon="mdi-home"
                class="rounded-lg mb-3"
              ></v-select>
            </section>

            <!-- Additional Options Section -->
            <section class="mb-4">  
              <div class="d-flex align-center mb-3">
                <v-icon icon="mdi-star" class="me-2" color="primary"/>
                <span class="text-subtitle-1 font-weight-medium">Amenities</span>
              </div>

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
                class="rounded-lg mb-3"
              ></v-combobox>
            </section>

            <!-- Score Filters Section -->
            <section class="mb-4">
              <div class="d-flex align-center mb-3">
                <v-icon icon="mdi-chart-bar" class="me-2" color="primary" />
                <span class="text-subtitle-1 font-weight-medium">Score Filters</span>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-body-2 font-weight-medium">Min Safety Score</span>
                  <v-chip size="x-small" :color="getScoreColor(filters.minSafetyScore)" variant="elevated"
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
                  :loading="loading"
                  :disabled="loading"
                  hide-details
                ></v-slider>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-body-2 font-weight-medium">Min Cleanliness</span>
                  <v-chip size="x-small" :color="getScoreColor(filters.minCleanlinessScore)" variant="elevated"
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
                  track-color="grey-lighten-5"
                  :loading="loading"
                  :disabled="loading"
                  hide-details
                ></v-slider>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-body-2 font-weight-medium">Min Accessibility</span>
                  <v-chip size="x-small" :color="getScoreColor(filters.minAccessibilityScore)" variant="elevated"
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
                  track-color="grey-lighten-5"
                  :loading="loading"
                  :disabled="loading"
                  hide-details
                ></v-slider>
              </div>
              
              <div class="mb-3">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-body-2 font-weight-medium">Max Noise Level</span>
                  <v-chip size="x-small" :color="getScoreColor(10 - filters.maxNoiseLevel)" variant="elevated"
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
                  track-color="grey-lighten-5"
                  :loading="loading"
                  :disabled="loading"
                  hide-details
                ></v-slider>
              </div>
            </section>

            <!-- Action Buttons -->
            <v-divider class="my-4"></v-divider>
            <div class="d-flex justify-space-between">
              <v-btn
                color="error"
                variant="outlined"
                @click="clearFilters"
                :disabled="loading"
                prepend-icon="mdi-refresh"
                size="small"
              >
                Clear
              </v-btn>
              <v-btn
                color="primary"
                @click="searchRooms"
                :loading="loading"
                :disabled="loading"
                prepend-icon="mdi-magnify"
                size="small"
              >
                Search
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Right Content Area with Results -->
      <v-col cols="12" md="9" lg="9">
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
                    
                    <v-chip
                      v-if="searchResults.summary.rooms_with_additional_amenities_count"
                      color="deep-purple"
                      variant="elevated"
                      size="large"
                      label
                      class="font-weight-medium"
                    >
                      <v-icon start size="small">mdi-star-plus</v-icon>
                      Additional Amenities ({{ searchResults.summary.rooms_with_additional_amenities_count }})
                    </v-chip>
                  </v-chip-group>
                </v-col>
              </v-row>

              <v-row v-if="Object.keys(activeFilters).length > 0" class="mt-2">
                <v-col cols="12">
                  <div class="text-subtitle-1 font-weight-medium mb-2">Applied Filters</div>
                  <v-chip-group>
                    <v-chip
                      v-for="(value, key) in activeFilters"
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

          <!-- Map View (Optional) -->
          <v-card class="mb-6" elevation="10" variant="elevated" v-if="selectedLocation">
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
              </div>
            </v-card-text>
          </v-card>

          <!-- Results Grid -->
          <v-row>
            <template v-if="searchResults.all_rooms && searchResults.all_rooms.length > 0">
              <v-col v-for="room, index in searchResults.all_rooms.slice().reverse()" :key="room.id" cols="12" sm="6" md="6" lg="4">
                <RoomCard 
                  :room="room" 
                  :user-type="userType" 
                  :index="index"
                  @show-on-map="selectRoomOnMap(room)"
                />
              </v-col>
            </template>
            <v-col v-else cols="12" class="text-center">
              <v-alert
                type="info"
                text="No rooms found matching your criteria. Try adjusting your filters."
              ></v-alert>
            </v-col>
          </v-row>
          
          <!-- Additional Amenities Section -->
          <div v-if="searchResults.suggestions?.rooms_with_additional_amenities?.length > 0" class="mt-8">
            <v-card class="mb-6" elevation="10" variant="elevated">
              <v-card-title class="d-flex align-center py-4 px-6 bg-deep-purple text-white">
                <v-icon icon="mdi-star-plus" class="me-2" />
                Rooms with Additional Valuable Amenities
                <v-tooltip location="right">
                  <template v-slot:activator="{ props }">
                    <v-icon
                      v-bind="props"
                      icon="mdi-information-outline"
                      class="ml-2"
                      size="small"
                      color="white"
                    ></v-icon>
                  </template>
                  <span>These rooms have valuable amenities you didn't request in your search</span>
                </v-tooltip>
              </v-card-title>
              
              <v-card-text class="pa-4">
                <p class="text-body-1 mb-4">
                  We found some rooms that match your criteria and also include additional valuable amenities 
                  you didn't specifically request. These extra amenities might enhance your living experience!
                </p>
                
                <v-row>
                  <v-col v-for="room in searchResults.suggestions.rooms_with_additional_amenities" 
                    :key="room.id" cols="12" sm="6" md="6" lg="4">
                    <RoomCard 
                      :room="room" 
                      :user-type="userType"
                      :highlight-amenities="room.highlighted_amenities"
                      @show-on-map="selectRoomOnMap(room)"
                    />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>
        </template>
        
        <!-- Loading State -->
        <div v-else-if="loading" class="d-flex justify-center align-center" style="min-height: 400px">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </div>
        
        <!-- Initial State -->
        <v-card v-else class="pa-6 text-center" elevation="10">
          <v-icon icon="mdi-home-search" size="64" color="primary" class="mb-4"></v-icon>
          <h2 class="text-h5 mb-2">Find Your Perfect Rental type</h2>
          <p class="text-body-1 mb-6">Use the filters on the left to search for rooms that match your preferences.</p>
          <v-btn color="primary" @click="searchRooms" prepend-icon="mdi-magnify">
            Start Searching
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '@/plugins/axios'
import RoomCard from '@/components/RoomCard.vue'
import LeafletMap from '@/components/LeafletMap.vue'

const router = useRouter()
const route = useRoute()
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
    rooms_with_additional_amenities_count: 0,
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
  maxDistance: null,
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
  if (filters.value.maxDistance) count++
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

const activeFilters = computed(() => {
  const result = {};
  
  if (filters.value.maxPrice) result.maxPrice = `₱${filters.value.maxPrice}`;
  if (filters.value.maxDistance) result.maxDistance = `${filters.value.maxDistance} km`;
  if (filters.value.minCapacity) result.minCapacity = filters.value.minCapacity;
  if (filters.value.location) result.location = filters.value.location;
  if (filters.value.amenities.length > 0) result.amenities = `${filters.value.amenities.length} selected`;
  if (filters.value.livingSpaceType) result.livingSpaceType = filters.value.livingSpaceType;
  
  return result;
})

const commonAmenities = [
  'Air Conditioning',
  'Appliances',
  'Backyard or garden',
  'CCTV',
  'Closet',
  'Common CR',
  'Convenience Store',
  'Curfew policy',
  'Double-Deck Bed',
  'Electricity Included',
  'Elevator',
  'Fan',
  'Fire Exits',
  'Fire Extinguisher',
  'Furnished',
  'Function room',
  'Gated property',
  'Gas/Induction Stove',
  'Gym/Fitness Gym',
  'Heating',
  'Kitchen',
  'Laundry',
  'Living room area',
  'Microwave',
  'Outdoor space',
  'Parking',
  'Pet-friendly',
  'Phone',
  'Private Bathroom',
  'Private garage',
  'Receiving Area',
  'Refrigerator',
  'Rice cooker',
  'Security Fingerprint',
  'Security Guard',
  'Security Keycard',
  'Single bed',
  'Storage room',
  'Study Desk',
  'Swimming Pool',
  'TV',
  'Unfurnished',
  'Washing Machine',
  'Water included',
  'WiFi',
]

const livingSpaceTypes = ['Boarding House', 'Apartment', 'House', 'Condo', 'Lodge', 'Hotel', 'Resort',]

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
    maxDistance: null,
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
  
  // Update URL with current filters
  updateUrlWithFilters();
  
  try {
    const params = {
      max_price: filters.value.maxPrice,
      max_distance: filters.value.maxDistance,
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
        rooms_with_additional_amenities_count: 0,
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

const formatFilterName = (key) => {
  const filterNames = {
    maxPrice: 'Max Price',
    maxDistance: 'Max Distance from SMCC',
    minCapacity: 'Min Capacity',
    location: 'Location',
    amenities: 'Amenities',
    minSafetyScore: 'Min Safety Score',
    maxNoiseLevel: 'Max Noise Level',
    minAccessibilityScore: 'Min Accessibility Score',
    minCleanlinessScore: 'Min Cleanliness Score',
    livingSpaceType: 'Rental Type'
  };
  
  return filterNames[key] || key;
}

const removeFilter = (key) => {
  if (key === 'maxDistance') {
    filters.value.maxDistance = null;
    updateUrlWithFilters();
  } else if (key === 'maxPrice') {
    filters.value.maxPrice = null;
  } else if (key === 'minCapacity') {
    filters.value.minCapacity = null;
  } else if (key === 'location') {
    filters.value.location = '';
  } else if (key === 'amenities') {
    filters.value.amenities = [];
  } else if (key === 'livingSpaceType') {
    filters.value.livingSpaceType = null;
  }
  
  // Re-search with updated filters
  searchRooms();
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
        maxDistance: route.query.maxDistance ? Number(route.query.maxDistance) : (response.data.preferred_distance || null),
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

const selectRoomOnMap = (room) => {
  if (room.latitude && room.longitude) {
    selectedLocation.value = [room.latitude, room.longitude]
    selectedLocationName.value = `${room.title} - ${formatDistance(room.distance_from_smcc)} km from SMCC`
  }
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
  
  // Check if we have query parameters to apply
  if (route.query.maxDistance) {
    filters.value.maxDistance = Number(route.query.maxDistance);
  }
  
  await checkPreferences()
  await searchRooms()
})

// Add the formatDistance function to the methods
const formatDistance = (distance) => {
  if (distance === null || distance === undefined) return 'Unknown';
  return distance.toFixed(1);
};

// Function to update URL with current filters
const updateUrlWithFilters = () => {
  const query = { ...route.query };
  
  // Only add non-null filters to the URL
  if (filters.value.maxDistance) {
    query.maxDistance = filters.value.maxDistance;
  } else {
    delete query.maxDistance;
  }
  
  // Update the URL without triggering a navigation
  router.replace({ query });
}

// Watch for changes to maxDistance filter
watch(() => filters.value.maxDistance, (newValue) => {
  if (newValue !== null && newValue !== undefined) {
    updateUrlWithFilters();
  }
});
</script>

<style scoped>
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.active-filter {
  border: 2px solid var(--v-primary-base) !important;
  background-color: rgba(var(--v-theme-primary), 0.05) !important;
}

.sticky-sidebar {
  position: sticky;
  top: 20px;
  max-height: calc(100vh - 70px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--v-theme-primary), 0.5) transparent;
}

.sticky-sidebar::-webkit-scrollbar {
  width: 6px;
}

.sticky-sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.sticky-sidebar::-webkit-scrollbar-thumb {
  background-color: rgba(var(--v-theme-primary), 0.5);
  border-radius: 6px;
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
@media (max-width: 960px) {
  .sticky-sidebar {
    position: relative;
    top: 0;
    max-height: none;
    margin-bottom: 20px;
  }
  
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
