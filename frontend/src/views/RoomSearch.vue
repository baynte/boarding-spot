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
            <div class="text-h6">{{ searchSummary.total_rooms || 0 }}</div>
            <div class="text-subtitle-2">Available Rooms</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card>
          <v-card-text class="text-center">
            <div class="text-h6">{{ searchSummary.best_matches_count || 0 }}</div>
            <div class="text-subtitle-2">Best Matches (80%+)</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card>
          <v-card-text class="text-center">
            <div class="text-h6">{{ searchSummary.good_matches_count || 0 }}</div>
            <div class="text-subtitle-2">Good Matches (60-79%)</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Search Filters -->
    <v-card class="mb-4">
      <v-card-title class="d-flex align-center">
        Filters
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="text"
          @click="clearFilters"
          :disabled="loading"
        >
          Clear Filters
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="filters.maxPrice"
              label="Max Price"
              type="number"
              prefix="$"
              clearable
              :loading="loading"
              :disabled="loading"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="filters.minSize"
              label="Min Size (sq ft)"
              type="number"
              clearable
              :loading="loading"
              :disabled="loading"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="filters.location"
              label="Location"
              clearable
              :loading="loading"
              :disabled="loading"
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
              :loading="loading"
              :disabled="loading"
            ></v-combobox>
          </v-col>
        </v-row>

        <!-- Score Filters -->
        <v-row>
          <v-col cols="12">
            <div class="text-subtitle-1 mb-2">Score Filters</div>
          </v-col>
          <v-col cols="12" sm="6">
            <div class="text-body-2 mb-1">Minimum Safety Score</div>
            <v-slider
              v-model="filters.minSafetyScore"
              :min="1"
              :max="10"
              :step="0.5"
              thumb-label="always"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
          <v-col cols="12" sm="6">
            <div class="text-body-2 mb-1">Maximum Noise Level</div>
            <v-slider
              v-model="filters.maxNoiseLevel"
              :min="1"
              :max="10"
              :step="0.5"
              thumb-label="always"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
          <v-col cols="12" sm="6">
            <div class="text-body-2 mb-1">Minimum Accessibility Score</div>
            <v-slider
              v-model="filters.minAccessibilityScore"
              :min="1"
              :max="10"
              :step="0.5"
              thumb-label="always"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
          <v-col cols="12" sm="6">
            <div class="text-body-2 mb-1">Minimum Cleanliness Score</div>
            <v-slider
              v-model="filters.minCleanlinessScore"
              :min="1"
              :max="10"
              :step="0.5"
              thumb-label="always"
              :loading="loading"
              :disabled="loading"
            ></v-slider>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 200px;">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <!-- No Results Message -->
    <v-alert
      v-else-if="!hasRooms"
      type="info"
      class="mb-4"
    >
      No rooms found matching your criteria. Try adjusting your filters.
    </v-alert>

    <!-- Results by Category -->
    <template v-else>
      <!-- Best Matches Section -->
      <div v-if="suggestions.best_matches.length > 0" class="mb-6">
        <div class="d-flex align-center mb-3">
          <h2 class="text-h5">Best Matches</h2>
          <v-chip
            color="success"
            class="ms-2"
          >
            80%+ Match
          </v-chip>
        </div>
        <v-row>
          <v-col
            v-for="room in suggestions.best_matches"
            :key="room.id"
            cols="12"
            sm="6"
            lg="4"
            class="d-flex"
          >
            <RoomCard :room="room" />
          </v-col>
        </v-row>
      </div>

      <!-- Good Matches Section -->
      <div v-if="suggestions.good_matches.length > 0" class="mb-6">
        <div class="d-flex align-center mb-3">
          <h2 class="text-h5">Good Matches</h2>
          <v-chip
            color="info"
            class="ms-2"
          >
            60-79% Match
          </v-chip>
        </div>
        <v-row>
          <v-col
            v-for="room in suggestions.good_matches"
            :key="room.id"
            cols="12"
            sm="6"
            lg="4"
            class="d-flex"
          >
            <RoomCard :room="room" />
          </v-col>
        </v-row>
      </div>

      <!-- Other Matches Section -->
      <div v-if="suggestions.other_matches.length > 0" class="mb-6">
        <div class="d-flex align-center mb-3">
          <h2 class="text-h5">Other Matches</h2>
          <v-chip
            color="warning"
            class="ms-2"
          >
            Below 60% Match
          </v-chip>
        </div>
        <v-row>
          <v-col
            v-for="room in suggestions.other_matches"
            :key="room.id"
            cols="12"
            sm="6"
            lg="4"
            class="d-flex"
          >
            <RoomCard :room="room" />
          </v-col>
        </v-row>
      </div>
    </template>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash'
import RoomCard from '@/components/RoomCard.vue'

const router = useRouter()
const hasPreferences = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')
const loading = ref(false)

// New data structure for search results
const searchSummary = ref({
  total_rooms: 0,
  best_matches_count: 0,
  good_matches_count: 0,
  other_matches_count: 0,
  categories: {
    best_match: '80% or higher',
    good_match: '60-79%',
    other_match: 'Below 60%'
  }
})

const suggestions = ref({
  best_matches: [],
  good_matches: [],
  other_matches: []
})

const allRooms = ref([])

// Computed property to check if we have any rooms
const hasRooms = computed(() => {
  return suggestions.value.best_matches.length > 0 ||
         suggestions.value.good_matches.length > 0 ||
         suggestions.value.other_matches.length > 0
})

const filters = ref({
  maxPrice: null,
  minSize: null,
  location: '',
  amenities: [],
  minSafetyScore: 1,
  maxNoiseLevel: 10,
  minAccessibilityScore: 1,
  minCleanlinessScore: 1
})

// Create a debounced version of searchRooms
const debouncedSearch = debounce(async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:5000/tenant/search', {
      params: {
        max_price: filters.value.maxPrice,
        min_size: filters.value.minSize,
        location: filters.value.location,
        amenities: filters.value.amenities?.length ? JSON.stringify(filters.value.amenities) : undefined,
        min_safety_score: filters.value.minSafetyScore,
        max_noise_level: filters.value.maxNoiseLevel,
        min_accessibility_score: filters.value.minAccessibilityScore,
        min_cleanliness_score: filters.value.minCleanlinessScore
      }
    })
    
    if (response.data.summary) {
      searchSummary.value = response.data.summary
      suggestions.value = response.data.suggestions
      allRooms.value = response.data.all_rooms
    } else {
      searchSummary.value = {
        total_rooms: 0,
        best_matches_count: 0,
        good_matches_count: 0,
        other_matches_count: 0
      }
      suggestions.value = {
        best_matches: [],
        good_matches: [],
        other_matches: []
      }
      allRooms.value = []
      snackbarText.value = response.data.message || 'No rooms found'
      snackbarColor.value = 'info'
      snackbar.value = true
    }
  } catch (error) {
    console.error('Error searching rooms:', error)
    searchSummary.value = {
      total_rooms: 0,
      best_matches_count: 0,
      good_matches_count: 0,
      other_matches_count: 0
    }
    suggestions.value = {
      best_matches: [],
      good_matches: [],
      other_matches: []
    }
    allRooms.value = []
    snackbarText.value = error.response?.data?.error || 'Error fetching rooms'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}, 500)

// Watch for changes in filters
watch(
  () => ({
    maxPrice: filters.value.maxPrice,
    minSize: filters.value.minSize,
    location: filters.value.location,
    amenities: filters.value.amenities,
    minSafetyScore: filters.value.minSafetyScore,
    maxNoiseLevel: filters.value.maxNoiseLevel,
    minAccessibilityScore: filters.value.minAccessibilityScore,
    minCleanlinessScore: filters.value.minCleanlinessScore
  }),
  () => {
    debouncedSearch()
  },
  { deep: true }
)

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

// Computed properties for stats
const averagePrice = computed(() => {
  if (rooms.value.length === 0) return 0
  const total = rooms.value.reduce((sum, room) => sum + room.price, 0)
  return Math.round(total / rooms.value.length)
})

const averageSize = computed(() => {
  if (rooms.value.length === 0) return 0
  const total = rooms.value.reduce((sum, room) => sum + room.size, 0)
  return Math.round(total / rooms.value.length)
})

const averageMatchScore = computed(() => {
  if (rooms.value.length === 0) return 0
  const total = rooms.value.reduce((sum, room) => sum + room.topsis_score, 0)
  return Math.round((total / rooms.value.length) * 100)
})

onMounted(async () => {
  await checkPreferences()
  debouncedSearch()
})

const checkPreferences = async () => {
  try {
    const response = await axios.get('http://localhost:5000/tenant/preferences')
    console.log('Preferences response:', response.data)
    hasPreferences.value = !!response.data
    if (response.data) {
      // Initialize filters with preferences
      filters.value = {
        maxPrice: response.data.max_price,
        minSize: response.data.min_size,
        location: response.data.preferred_location,
        amenities: response.data.required_amenities || [],
        // Initialize score filters based on weights
        // Higher weight means higher minimum requirement
        minSafetyScore: Math.max(1, Math.round(response.data.safety_weight * 10)),
        maxNoiseLevel: Math.min(10, Math.round((1 - response.data.noise_level_weight) * 10)),
        minAccessibilityScore: Math.max(1, Math.round(response.data.accessibility_weight * 10)),
        minCleanlinessScore: Math.max(1, Math.round(response.data.cleanliness_weight * 10))
      }
      // Trigger a search after setting preferences
      debouncedSearch()
    }
  } catch (error) {
    console.error('Error checking preferences:', error)
    hasPreferences.value = false
  }
}

const contactLandlord = (room) => {
  // This would typically open a chat or messaging interface
  snackbarText.value = 'Contact feature coming soon!'
  snackbarColor.value = 'info'
  snackbar.value = true
}

const clearFilters = () => {
  filters.value = {
    maxPrice: null,
    minSize: null,
    location: '',
    amenities: [],
    minSafetyScore: 1,
    maxNoiseLevel: 10,
    minAccessibilityScore: 1,
    minCleanlinessScore: 1
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price)
}

const formatSize = (size) => {
  return `${size} sq ft`
}

const formatMatchPercentage = (score) => {
  if (score === undefined || score === null) return '0%';
  // Convert TOPSIS score (0-1) to percentage and round to nearest integer
  return `${Math.round(score * 100)}%`;
};

const getMatchColor = (score) => {
  if (score === undefined || score === null) return 'error';
  const percentage = score * 100;
  if (percentage >= 80) return 'success';
  if (percentage >= 60) return 'info';
  if (percentage >= 40) return 'warning';
  return 'error';
};

const getMatchIcon = (score) => {
  if (score >= 0.8) return 'mdi-star-circle'
  if (score >= 0.6) return 'mdi-star-half-full'
  if (score >= 0.4) return 'mdi-star-outline'
  return 'mdi-alert-circle'
}
</script>

<style scoped>
.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.match-chip {
  position: absolute;
  top: 12px;
  right: 12px;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 