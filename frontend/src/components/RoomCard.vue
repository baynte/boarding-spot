<template>
  <v-card class="d-flex flex-column w-100">
    <div class="position-relative">
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
      <v-chip
        class="match-chip"
        :color="getMatchColor(room.match_percentage)"
        size="large"
        label
        variant="elevated"
      >
        <v-icon start :icon="getMatchIcon(room.match_percentage)"></v-icon>
        {{ room.match_percentage }}% Match
      </v-chip>
      <v-chip
        class="rank-chip"
        color="grey-darken-3"
        size="small"
        label
      >
        Rank #{{ room.rank }}
      </v-chip>
    </div>

    <v-card-title class="text-truncate">
      {{ room.title }}
    </v-card-title>

    <v-card-text class="flex-grow-1">
      <div class="d-flex align-center mb-2">
        <div class="text-h6 primary--text">{{ formatPrice(room.price) }}</div>
        <div class="text-subtitle-2 ms-1">/month</div>
      </div>

      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="me-1">mdi-map-marker</v-icon>
        <span class="text-body-2">{{ room.location }}</span>
      </div>

      <div class="d-flex align-center mb-2">
        <v-icon size="small" class="me-1">mdi-ruler-square</v-icon>
        <span class="text-body-2">{{ formatSize(room.size) }}</span>
      </div>

      <div class="text-body-2 text-truncate-2 mb-3">{{ room.description }}</div>

      <v-chip-group class="mb-3">
        <v-chip
          v-for="amenity in room.amenities.slice(0, 3)"
          :key="amenity"
          size="small"
          variant="outlined"
          class="text-caption"
        >
          {{ amenity }}
        </v-chip>
        <v-chip
          v-if="room.amenities.length > 3"
          size="small"
          variant="outlined"
          class="text-caption"
        >
          +{{ room.amenities.length - 3 }} more
        </v-chip>
      </v-chip-group>

      <v-divider class="mb-3"></v-divider>

      <v-row dense>
        <v-col cols="6">
          <div class="d-flex align-center mb-1">
            <v-icon size="small" color="amber-darken-2" class="me-1">mdi-shield-home</v-icon>
            <span class="text-caption">Safety</span>
            <v-tooltip activator="parent" location="top">
              Weight: {{ (room.match_details.safety.weight * 100).toFixed(0) }}%
            </v-tooltip>
            <span class="text-caption ms-auto">{{ room.safety_score }}/10</span>
          </div>
          <v-progress-linear
            :model-value="room.safety_score * 10"
            color="amber-darken-2"
            height="4"
            rounded
          ></v-progress-linear>
        </v-col>
        <v-col cols="6">
          <div class="d-flex align-center mb-1">
            <v-icon size="small" color="light-blue" class="me-1">mdi-broom</v-icon>
            <span class="text-caption">Cleanliness</span>
            <v-tooltip activator="parent" location="top">
              Weight: {{ (room.match_details.cleanliness.weight * 100).toFixed(0) }}%
            </v-tooltip>
            <span class="text-caption ms-auto">{{ room.cleanliness_score }}/10</span>
          </div>
          <v-progress-linear
            :model-value="room.cleanliness_score * 10"
            color="light-blue"
            height="4"
            rounded
          ></v-progress-linear>
        </v-col>
        <v-col cols="6">
          <div class="d-flex align-center mb-1">
            <v-icon size="small" color="green" class="me-1">mdi-wheelchair-accessibility</v-icon>
            <span class="text-caption">Accessibility</span>
            <v-tooltip activator="parent" location="top">
              Weight: {{ (room.match_details.accessibility.weight * 100).toFixed(0) }}%
            </v-tooltip>
            <span class="text-caption ms-auto">{{ room.accessibility_score }}/10</span>
          </div>
          <v-progress-linear
            :model-value="room.accessibility_score * 10"
            color="green"
            height="4"
            rounded
          ></v-progress-linear>
        </v-col>
        <v-col cols="6">
          <div class="d-flex align-center mb-1">
            <v-icon size="small" color="deep-purple" class="me-1">mdi-volume-medium</v-icon>
            <span class="text-caption">Noise</span>
            <v-tooltip activator="parent" location="top">
              Weight: {{ (room.match_details.noise.weight * 100).toFixed(0) }}%
            </v-tooltip>
            <span class="text-caption ms-auto">{{ room.noise_level }}/10</span>
          </div>
          <v-progress-linear
            :model-value="(10 - room.noise_level) * 10"
            color="deep-purple"
            height="4"
            rounded
          ></v-progress-linear>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions class="pa-4 pt-0">
      <v-btn
        block
        color="primary"
        variant="elevated"
        @click="contactLandlord"
      >
        Contact Landlord
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  room: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(price)
}

const formatSize = (size) => {
  return `${size} sq ft`
}

const getMatchColor = (percentage) => {
  if (!percentage) return 'error'
  if (percentage >= 80) return 'success'
  if (percentage >= 60) return 'info'
  return 'warning'
}

const getMatchIcon = (percentage) => {
  if (!percentage) return 'mdi-alert'
  if (percentage >= 80) return 'mdi-star'
  if (percentage >= 60) return 'mdi-thumb-up'
  return 'mdi-thumb-down'
}

const contactLandlord = () => {
  // TODO: Implement contact functionality
  console.log('Contact landlord for room:', props.room.id)
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
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7) !important;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-4px);
}
</style> 