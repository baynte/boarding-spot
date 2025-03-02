<template>
  <v-dialog v-model="dialog" max-width="600px" transition="fade-transition">
    <template v-slot:activator="{ props }">
      <v-btn
        color="primary"
        v-bind="props"
        :disabled="!canRate"
        :title="!canRate ? 'Only tenants can rate Rental types' : ''"
        @click.stop
        variant="elevated"
        prepend-icon="mdi-star"
        class="px-4 py-2"
        elevation="10"
      >
        {{ hasRated ? 'Update Rating' : 'Rate Rental type' }}
      </v-btn>
    </template>

    <v-card elevation="8" class="rounded-lg">
      <v-card-title class="py-4 px-6 bg-primary text-white">
        <span class="text-h5 font-weight-medium">{{ hasRated ? 'Update Rating' : 'Rate Rental type' }}</span>
      </v-card-title>

      <v-card-text class="pt-5">
        <v-container>
          <v-row>
            <v-col cols="12" class="pb-0">
              <h3 class="text-subtitle-1 font-weight-bold mb-5">How would you rate your experience?</h3>
            </v-col>


      
            <v-col cols="12" class="py-1">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-1 font-weight-medium">Safety</span>
                <v-chip size="small" :color="getScoreColor(rating.safety_rating)" class="font-weight-bold">
                  {{ rating.safety_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.safety_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(rating.safety_rating)"
                track-color="grey-lighten-2"
                show-ticks="always"
                :tick-size="4"
                thumb-label="always"
                class="mt-1"
              ></v-slider>
            </v-col>

            <v-col cols="12" class="py-1">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-1 font-weight-medium">Cleanliness</span>
                <v-chip size="small" :color="getScoreColor(rating.cleanliness_rating)" class="font-weight-bold">
                  {{ rating.cleanliness_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.cleanliness_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(rating.cleanliness_rating)"
                track-color="grey-lighten-2"
                show-ticks="always"
                :tick-size="4"
                thumb-label="always"
                class="mt-1"
              ></v-slider>
            </v-col>

            <v-col cols="12" class="py-1">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-1 font-weight-medium">Accessibility</span>
                <v-chip size="small" :color="getScoreColor(rating.accessibility_rating)" class="font-weight-bold">
                  {{ rating.accessibility_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.accessibility_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(rating.accessibility_rating)"
                track-color="grey-lighten-2"
                show-ticks="always"
                :tick-size="4"
                thumb-label="always"
                class="mt-1"
              ></v-slider>
            </v-col>

            <v-col cols="12" class="py-1">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-1 font-weight-medium">Noise Level</span>
                <v-chip size="small" :color="getScoreColor(10 - rating.noise_level_rating)" class="font-weight-bold">
                  {{ rating.noise_level_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.noise_level_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(10 - rating.noise_level_rating)"
                track-color="grey-lighten-2"
                show-ticks="always"
                :tick-size="4"
                thumb-label="always"
                class="mt-1"
              ></v-slider>
            </v-col>

            <v-col cols="12" class="pt-3">
              <v-textarea
                v-model="rating.comment"
                label="Share your experience (optional)"
                rows="3"
                variant="outlined"
                counter
                maxlength="500"
                auto-grow
                class="mt-2"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn 
          color="error" 
          variant="text" 
          @click="dialog = false"
          class="px-4"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="submitRating"
          :loading="loading"
          :disabled="loading"
          class="px-6"
        >
          Submit Rating
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from '@/plugins/axios'

const props = defineProps({
  roomId: {
    type: Number,
    required: true
  },
  userType: {
    type: String,
    required: true
  },
  existingRating: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['rating-updated'])

const dialog = ref(false)
const loading = ref(false)

const rating = ref({
  safety_rating: props.existingRating?.safety_rating || 5,
  cleanliness_rating: props.existingRating?.cleanliness_rating || 5,
  accessibility_rating: props.existingRating?.accessibility_rating || 5,
  noise_level_rating: props.existingRating?.noise_level_rating || 5,
  comment: props.existingRating?.comment || ''
})

const canRate = computed(() => props.userType === 'tenant')
const hasRated = computed(() => !!props.existingRating)

const getScoreColor = (score) => {
  if (score >= 8) return 'success'
  if (score >= 6) return 'info'
  if (score >= 4) return 'warning'
  return 'error'
}

const submitRating = async () => {
  loading.value = true
  try {
    const response = await axios.post(`/rating/submit/${props.roomId}`, rating.value)
    emit('rating-updated', response.data.rating)
    dialog.value = false
  } catch (error) {
    console.error('Error submitting rating:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.v-slider {
  margin-bottom: 24px;
}
</style> 