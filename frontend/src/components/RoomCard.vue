<template>
  <v-card class="d-flex flex-column h-100">
    <div class="position-relative">
      <v-img
        :src="room.image_url || '/placeholder-room.jpg'"
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
      <v-chip
        class="match-chip"
        :color="getMatchColor(match_score)"
        size="large"
        label
        variant="elevated"
      >
        <v-icon start :icon="getMatchIcon(match_score)"></v-icon>
        {{ Math.round(match_score) }}%
      </v-chip>
      <v-chip
        class="rank-chip"
        :color="getMatchColor(match_score)"
        size="small"
        label
      >
        #{{ room.rank }} of {{ total_rooms }}
      </v-chip>
    </div>

    <v-card-title class="text-truncate">
      {{ room.title }}
    </v-card-title>

    <v-card-text class="flex-grow-1">
      <div class="d-flex align-center mb-2">
        <div class="text-h6 primary--text">₱{{ formatPrice(room.price) }}</div>
        <div class="text-subtitle-2 ms-1">/month</div>
      </div>

      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="me-1">mdi-map-marker</v-icon>
        <span class="text-body-2">{{ room.location }}</span>
      </div>

      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="me-1">mdi-ruler-square</v-icon>
        <span class="text-body-2">{{ room.size }} sq ft</span>
      </div>

      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="me-1">mdi-account</v-icon>
        <span class="text-body-2">Contact: {{ room.landlord?.contact_number || 'Not available' }}</span>
      </div>

      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="me-1">mdi-email</v-icon>
        <span class="text-body-2">{{ room.landlord?.email || 'Email not available' }}</span>
      </div>

      <div class="text-body-2 text-truncate-2 mb-3">{{ room.description }}</div>

      <!-- Amenities -->
      <v-chip-group class="mb-3">
        <template v-if="match_details?.amenities?.matched?.length">
          <v-chip
            v-for="amenity in match_details.amenities.matched"
            :key="amenity"
            size="small"
            color="success"
            variant="outlined"
            class="text-caption"
          >
            <v-icon start size="x-small">mdi-check</v-icon>
            {{ amenity }}
          </v-chip>
        </template>
        <template v-if="match_details?.amenities?.missing?.length">
          <v-chip
            v-for="amenity in match_details.amenities.missing"
            :key="amenity"
            size="small"
            color="error"
            variant="outlined"
            class="text-caption"
          >
            <v-icon start size="x-small">mdi-close</v-icon>
            {{ amenity }}
          </v-chip>
        </template>
      </v-chip-group>

      <v-divider class="mb-3"></v-divider>

      <!-- Match Score Details -->
      <div class="match-details mb-4">
        <div class="d-flex align-center justify-space-between mb-2">
          <div class="text-h6">Match Details</div>
          <v-chip
            :color="getMatchColor(match_score)"
            size="small"
            label
          >
            {{ Math.round(match_score) }}% Overall
          </v-chip>
        </div>
        
        <v-row dense>
          <!-- Safety Score -->
          <v-col cols="12" class="mb-2">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(safetyScore)" class="me-1">mdi-shield-home</v-icon>
              <span class="text-body-2">Safety</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(safetyScore)"
                label
              >
                {{ safetyScore }}/10
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="safetyScore * 10"
              :color="getScoreColor(safetyScore)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col>

          <!-- Cleanliness Score -->
          <v-col cols="12" class="mb-2">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(cleanlinessScore)" class="me-1">mdi-broom</v-icon>
              <span class="text-body-2">Cleanliness</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(cleanlinessScore)"
                label
              >
                {{ cleanlinessScore }}/10
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="cleanlinessScore * 10"
              :color="getScoreColor(cleanlinessScore)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col>

          <!-- Accessibility Score -->
          <v-col cols="12" class="mb-2">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(accessibilityScore)" class="me-1">mdi-wheelchair-accessibility</v-icon>
              <span class="text-body-2">Accessibility</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(accessibilityScore)"
                label
              >
                {{ accessibilityScore }}/10
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="accessibilityScore * 10"
              :color="getScoreColor(accessibilityScore)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col>

          <!-- Noise Level -->
          <v-col cols="12" class="mb-2">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(10 - noiseScore)" class="me-1">mdi-volume-medium</v-icon>
              <span class="text-body-2">Noise Level</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(10 - noiseScore)"
                label
              >
                {{ noiseScore }}/10
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="(10 - noiseScore) * 10"
              :color="getScoreColor(10 - noiseScore)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col>

          <!-- Amenity Match -->
          <v-col cols="12" class="mb-2">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(amenityScore / 10)" class="me-1">mdi-check-circle</v-icon>
              <span class="text-body-2">Amenity Match</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(amenityScore / 10)"
                label
              >
                {{ Math.round(amenityScore) }}%
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="amenityScore"
              :color="getScoreColor(amenityScore / 10)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col>

          <!-- Location Match -->
          <!-- <v-col cols="12" class="mb-2">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(locationScore / 10)" class="me-1">mdi-map-marker-check</v-icon>
              <span class="text-body-2">Location Match</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(locationScore / 10)"
                label
              >
                {{ Math.round(locationScore) }}%
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="locationScore"
              :color="getScoreColor(locationScore / 10)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col> -->

          <!-- Price Value -->
          <v-col cols="12">
            <div class="d-flex align-center mb-1">
              <v-icon size="small" :color="getScoreColor(priceValueScore / 10)" class="me-1">mdi-currency-usd</v-icon>
              <span class="text-body-2">Price Value</span>
              <v-spacer></v-spacer>
              <v-chip
                size="x-small"
                :color="getScoreColor(priceValueScore / 10)"
                label
              >
                {{ Math.round(priceValueScore) }}%
              </v-chip>
            </div>
            <v-progress-linear
              :model-value="priceValueScore"
              :color="getScoreColor(priceValueScore / 10)"
              height="8"
              rounded
            ></v-progress-linear>
          </v-col>
        </v-row>
      </div>
    </v-card-text>

    <!-- <v-card-actions>
      <v-btn
        block
        color="primary"
        variant="elevated"
        @click="viewDetails"
      >
        View Details
      </v-btn>
    </v-card-actions> -->
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  room: {
    type: Object,
    required: true,
    validator: (obj) => {
      return (
        obj.id !== undefined &&
        obj.title !== undefined &&
        obj.description !== undefined &&
        obj.price !== undefined &&
        obj.size !== undefined &&
        obj.location !== undefined &&
        obj.amenities !== undefined &&
        obj.availability !== undefined &&
        obj.image_url !== undefined &&
        obj.safety_score !== undefined &&
        obj.cleanliness_score !== undefined &&
        obj.accessibility_score !== undefined &&
        obj.noise_level !== undefined &&
        obj.landlord !== undefined &&
        obj.comprehensive_score !== undefined &&
        obj.rank !== undefined &&
        obj.percentile !== undefined &&
        obj.match_details !== undefined
      )
    }
  },
  match_score: {
    type: Number,
    required: true,
    default: (props) => props?.room?.comprehensive_score || 0
  },
  match_details: {
    type: Object,
    required: true,
    default: (props) => props?.room?.match_details || {
      safety: { score: 0, weight: 0, weighted_score: 0 },
      cleanliness: { score: 0, weight: 0, weighted_score: 0 },
      accessibility: { score: 0, weight: 0, weighted_score: 0 },
      noise: { score: 0, weight: 0, weighted_score: 0 },
      amenities: { score: 0, weight: 0, weighted_score: 0, matched: [], missing: [] },
      location: { score: 0, preferred_location: '', actual_location: '' },
      price_value: { score: 0, preferred_max: 0, actual_price: 0 }
    }
  },
  total_rooms: {
    type: Number,
    required: true
  }
})

// Computed properties for safer data access
const safetyScore = computed(() => props.match_details?.safety?.score || props.room?.safety_score || 0)
const cleanlinessScore = computed(() => props.match_details?.cleanliness?.score || props.room?.cleanliness_score || 0)
const accessibilityScore = computed(() => props.match_details?.accessibility?.score || props.room?.accessibility_score || 0)
const noiseScore = computed(() => props.match_details?.noise?.score || props.room?.noise_level || 0)
const amenityScore = computed(() => props.match_details?.amenities?.score || 0)
const locationScore = computed(() => props.match_details?.location?.score || 0)
const priceValueScore = computed(() => props.match_details?.price_value?.score || 0)
const matchedAmenities = computed(() => props.match_details?.amenities?.matched || [])
const missingAmenities = computed(() => props.match_details?.amenities?.missing || [])

const router = useRouter()

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-PH').format(price)
}

const getMatchColor = (score) => {
  if (score >= 90) return 'success'
  if (score >= 85) return 'info'
  if (score >= 75) return 'green-darken-1'
  if (score >= 60) return 'warning'
  return 'grey'
}

const getMatchIcon = (score) => {
  if (score >= 90) return 'mdi-star'
  if (score >= 85) return 'mdi-star-half-full'
  if (score >= 75) return 'mdi-star-outline'
  if (score >= 60) return 'mdi-star-outline'
  return 'mdi-star-off'
}

const getScoreColor = (score) => {
  if (score >= 8) return 'success'
  if (score >= 6) return 'info'
  if (score >= 4) return 'warning'
  return 'error'
}

const viewDetails = () => {
  router.push(`/rooms/${props.room.id}`)
}
</script>

<style scoped>
.match-chip {
  position: absolute;
  top: 8px;
  right: 8px;
}

.rank-chip {
  position: absolute;
  top: 8px;
  left: 8px;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-card {
  transition: transform 0.2s ease-in-out;
}

.v-card:hover {
  transform: translateY(-4px);
}
</style> 