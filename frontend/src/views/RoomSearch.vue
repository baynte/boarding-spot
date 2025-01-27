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
    <v-expansion-panels v-model="showFilters" class="mb-4">
      <v-expansion-panel>
        <v-expansion-panel-title>
          <div class="d-flex align-center">
            <v-icon start>mdi-filter</v-icon>
            Search Filters
            <v-chip
              v-if="activeFiltersCount"
              color="primary"
              size="small"
              class="ms-2"
            >
              {{ activeFiltersCount }} active
            </v-chip>
          </div>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="filters.maxPrice"
                label="Maximum Price"
                type="number"
                prefix="₱"
                clearable
                :loading="loading"
                :disabled="loading"
                density="comfortable"
                variant="outlined"
                hide-details
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="filters.minCapacity"
                label="Minimum Capacity"
                type="number"
                min="1"
                hint="Minimum number of tenants"
                persistent-hint
                clearable
                :loading="loading"
                :disabled="loading"
                density="comfortable"
                variant="outlined"
                hide-details
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
                hide-details
                prepend-inner-icon="mdi-map-marker"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="sortBy"
                :items="sortOptions"
                label="Sort By"
                density="comfortable"
                variant="outlined"
                hide-details
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
                @click="applyFilters"
                :loading="loading"
                :disabled="loading"
              >
                Apply Filters
              </v-btn>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- Search Results -->
    <div v-if="!loading && searchResults?.all_rooms?.length > 0">
      <!-- Perfect Matches -->
      <div v-if="searchResults?.suggestions?.perfect_matches?.length > 0" class="mb-6">
        <h2 class="text-h5 mb-3">
          Perfect Matches
          <v-chip color="success" class="ms-2">{{ searchResults?.summary?.perfect_matches_count || 0 }}</v-chip>
        </h2>
        <v-row>
          <v-col 
            v-for="room in searchResults?.suggestions?.perfect_matches || []"
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <RoomCard 
              :room="room"
              :match-score="room.comprehensive_score"
              :match-details="room.match_details"
              :total_rooms="searchResults?.summary?.total_rooms || 0"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Excellent Matches -->
      <div v-if="searchResults?.suggestions?.excellent_matches?.length > 0" class="mb-6">
        <h2 class="text-h5 mb-3">
          Excellent Matches
          <v-chip color="info" class="ms-2">{{ searchResults?.summary?.excellent_matches_count || 0 }}</v-chip>
        </h2>
        <v-row>
          <v-col 
            v-for="room in searchResults?.suggestions?.excellent_matches || []"
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <RoomCard 
              :room="room"
              :match-score="room.comprehensive_score"
              :match-details="room.match_details"
              :total_rooms="searchResults?.summary?.total_rooms || 0"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Good Matches -->
      <div v-if="searchResults?.suggestions?.good_matches?.length > 0" class="mb-6">
        <h2 class="text-h5 mb-3">
          Good Matches
          <v-chip color="success-darken-1" class="ms-2">{{ searchResults?.summary?.good_matches_count || 0 }}</v-chip>
        </h2>
        <v-row>
          <v-col 
            v-for="room in searchResults?.suggestions?.good_matches || []"
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <RoomCard 
              :room="room"
              :match-score="room.comprehensive_score"
              :match-details="room.match_details"
              :total_rooms="searchResults?.summary?.total_rooms || 0"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Fair Matches -->
      <div v-if="searchResults?.suggestions?.fair_matches?.length > 0" class="mb-6">
        <h2 class="text-h5 mb-3">
          Fair Matches
          <v-chip color="warning" class="ms-2">{{ searchResults?.summary?.fair_matches_count || 0 }}</v-chip>
        </h2>
        <v-row>
          <v-col 
            v-for="room in searchResults?.suggestions?.fair_matches || []"
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <RoomCard 
              :room="room"
              :match-score="room.comprehensive_score"
              :match-details="room.match_details"
              :total_rooms="searchResults?.summary?.total_rooms || 0"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Other Matches -->
      <div v-if="searchResults?.suggestions?.other_matches?.length > 0" class="mb-6">
        <h2 class="text-h5 mb-3">
          Other Matches
          <v-chip color="grey" class="ms-2">{{ searchResults?.summary?.other_matches_count || 0 }}</v-chip>
        </h2>
        <v-row>
          <v-col 
            v-for="room in searchResults?.suggestions?.other_matches || []"
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <RoomCard 
              :room="room"
              :match-score="room.comprehensive_score"
              :match-details="room.match_details"
              :total_rooms="searchResults?.summary?.total_rooms || 0"
            />
          </v-col>
        </v-row>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-center align-center py-12">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>

    <!-- No Results Message -->
    <v-alert
      v-if="!loading && (!searchResults?.all_rooms || searchResults.all_rooms.length === 0)"
      type="info"
      class="mt-4"
    >
      No rooms found matching your criteria. Try adjusting your filters.
    </v-alert>
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
  applyFilters()
}

const applyFilters = async () => {
  loading.value = true
  try {
    const params = {
      max_price: filters.value.maxPrice,
      min_capacity: filters.value.minCapacity,
      location: filters.value.location,
      amenities: filters.value.amenities,
      min_safety_score: filters.value.minSafetyScore,
      max_noise_level: filters.value.maxNoiseLevel,
      min_accessibility_score: filters.value.minAccessibilityScore,
      min_cleanliness_score: filters.value.minCleanlinessScore
    }
    
    const response = await axios.get('/tenant/search', { params })
    searchResults.value = response.data
  } catch (error) {
    console.error('Error fetching search results:', error)
  } finally {
    loading.value = false
  }
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
    await applyFilters()
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
</style> 