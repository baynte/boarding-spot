<template>
  <div>
    <v-card class="d-flex flex-column h-100" @click="dialog = true">
      <div class="position-relative">
        <v-img
          :src="parseImageUrls(room.image_urls)?.[0] || '/placeholder-room.jpg'"
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
          <v-icon size="small" class="me-1">mdi-account-group</v-icon>
          <span class="text-body-2">{{ room.capacity }} tenant{{ room.capacity > 1 ? 's' : '' }}</span>
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
    </v-card>

    <!-- Details Modal -->
    <v-dialog v-model="dialog" max-width="1200">
      <v-card>
        <v-card-text class="pa-0">
          <v-row no-gutters>
            <!-- Image Carousel (60%) -->
            <v-col cols="12" md="7">
              <v-carousel
                v-model="currentSlide"
                show-arrows="hover"
                height="600"
                hide-delimiter-background
              >
                <v-carousel-item
                  v-for="(url, index) in parseImageUrls(room.image_urls)"
                  :key="index"
                >
                  <v-img
                    :src="url"
                    height="600"
                    cover
                    class="bg-grey-lighten-2"
                  >
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-carousel-item>
              </v-carousel>
            </v-col>

            <!-- Room Details (40%) -->
            <v-col cols="12" md="5" class="pa-6">
              <div class="d-flex justify-space-between align-center mb-4">
                <h2 class="text-h4">{{ room.title }}</h2>
                <v-btn icon="mdi-close" variant="text" @click="dialog = false"></v-btn>
              </div>

              <div class="d-flex align-center mb-4">
                <div class="text-h5 primary--text">₱{{ formatPrice(room.price) }}</div>
                <div class="text-subtitle-1 ms-1">/month</div>
              </div>

              <v-divider class="mb-4"></v-divider>

              <!-- Location and Capacity -->
              <div class="d-flex flex-column gap-2">
                <div class="d-flex align-center">
                  <v-icon size="20" class="me-2">mdi-map-marker</v-icon>
                  <span class="text-body-1">{{ room.location }}</span>
                </div>
                <div class="d-flex align-center">
                  <v-icon size="20" class="me-2">mdi-account-group</v-icon>
                  <span class="text-body-1">{{ room.capacity }} tenant{{ room.capacity > 1 ? 's' : '' }}</span>
                </div>
              </div>

              <!-- Description -->
              <div class="text-body-1 mb-4">{{ room.description }}</div>

              <!-- Amenities -->
              <h3 class="text-h6 mb-2">Amenities</h3>
              <v-chip-group class="mb-4">
                <v-chip
                  v-for="amenity in parseAmenities(room.amenities)"
                  :key="amenity"
                  size="small"
                  variant="outlined"
                  class="text-body-2"
                >
                  {{ amenity }}
                </v-chip>
              </v-chip-group>

              <!-- Ratings -->
              <h3 class="text-h6 mb-2">Property Ratings</h3>
              <v-row dense>
                <v-col cols="6">
                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" :color="getScoreColor(room.safety_score)" class="me-1">mdi-shield-home</v-icon>
                    <span class="text-body-2">Safety: {{ room.safety_score }}/10</span>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" :color="getScoreColor(room.cleanliness_score)" class="me-1">mdi-broom</v-icon>
                    <span class="text-body-2">Cleanliness: {{ room.cleanliness_score }}/10</span>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" :color="getScoreColor(room.accessibility_score)" class="me-1">mdi-wheelchair-accessibility</v-icon>
                    <span class="text-body-2">Accessibility: {{ room.accessibility_score }}/10</span>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" :color="getScoreColor(10 - room.noise_level)" class="me-1">mdi-volume-medium</v-icon>
                    <span class="text-body-2">Noise Level: {{ room.noise_level }}/10</span>
                  </div>
                </v-col>
              </v-row>

              <!-- Contact Information -->
              <v-divider class="my-4"></v-divider>
              <h3 class="text-h6 mb-2">Contact Information</h3>
              <div class="d-flex align-center mb-2">
                <v-icon size="20" class="me-2">mdi-account</v-icon>
                <span class="text-body-1">{{ room.landlord?.contact_number || 'Not available' }}</span>
              </div>
              <div class="d-flex align-center mb-2">
                <v-icon size="20" class="me-2">mdi-email</v-icon>
                <span class="text-body-1">{{ room.landlord?.email || 'Email not available' }}</span>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  room: {
    type: Object,
    required: true,
    validator: (room) => {
      return [
        'id',
        'title',
        'description',
        'price',
        'capacity',
        'location',
        'amenities',
        'availability',
        'image_urls',
        'safety_score',
        'cleanliness_score',
        'accessibility_score',
        'noise_level',
        'landlord'
      ].every(prop => prop in room)
    }
  },
  match_score: {
    type: Number,
    required: false,
    default: (props) => props?.room?.comprehensive_score || 0
  },
  match_details: {
    type: Object,
    required: false,
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
    required: false,
    default: 1
  }
})

// Update computed properties to use match_details from the room object
const safetyScore = computed(() => props.room.match_details?.safety?.score || props.room.safety_score || 0)
const cleanlinessScore = computed(() => props.room.match_details?.cleanliness?.score || props.room.cleanliness_score || 0)
const accessibilityScore = computed(() => props.room.match_details?.accessibility?.score || props.room.accessibility_score || 0)
const noiseScore = computed(() => props.room.match_details?.noise?.score || props.room.noise_level || 0)
const amenityScore = computed(() => props.room.match_details?.amenities?.score || 0)
const locationScore = computed(() => props.room.match_details?.location?.score || 0)
const priceValueScore = computed(() => props.room.match_details?.price_value?.score || 0)
const matchedAmenities = computed(() => props.room.match_details?.amenities?.matched || [])
const missingAmenities = computed(() => props.room.match_details?.amenities?.missing || [])

const router = useRouter()

const dialog = ref(false)
const currentSlide = ref(0)

const parseImageUrls = (urls) => {
  if (!urls) return [];
  try {
    return typeof urls === 'string' ? JSON.parse(urls) : urls;
  } catch (error) {
    console.error('Error parsing image URLs:', error);
    return [];
  }
}

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

const parseAmenities = (amenities) => {
  if (!amenities) return [];
  if (Array.isArray(amenities)) return amenities;
  try {
    return typeof amenities === 'string' ? JSON.parse(amenities) : [];
  } catch (error) {
    console.error('Error parsing amenities:', error);
    return [];
  }
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

/* Add new styles for the modal */
.v-dialog .v-card {
  overflow: hidden;
}

.v-carousel {
  background-color: #000;
}

.v-carousel .v-img {
  object-fit: contain;
}
</style> 