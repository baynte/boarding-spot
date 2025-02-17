<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ props }">
      <v-btn
        color="primary"
        v-bind="props"
        :disabled="!canRate"
        :title="!canRate ? 'Only tenants can rate living spaces' : ''"
        @click.stop
      >
        {{ hasRated ? 'Update Rating' : 'Rate Living Space' }}

      </v-btn>
    </template>


    <v-card>
      <v-card-title>
        <span class="text-h5">{{ hasRated ? 'Update Rating' : 'Rate Living Space' }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-2">Safety Rating</span>
                <v-chip size="x-small" :color="getScoreColor(rating.safety_rating)">
                  {{ rating.safety_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.safety_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(rating.safety_rating)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
              ></v-slider>
            </v-col>

            <v-col cols="12">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-2">Cleanliness Rating</span>
                <v-chip size="x-small" :color="getScoreColor(rating.cleanliness_rating)">
                  {{ rating.cleanliness_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.cleanliness_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(rating.cleanliness_rating)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
              ></v-slider>
            </v-col>

            <v-col cols="12">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-2">Accessibility Rating</span>
                <v-chip size="x-small" :color="getScoreColor(rating.accessibility_rating)">
                  {{ rating.accessibility_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.accessibility_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(rating.accessibility_rating)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
              ></v-slider>
            </v-col>

            <v-col cols="12">
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="text-body-2">Noise Level Rating</span>
                <v-chip size="x-small" :color="getScoreColor(10 - rating.noise_level_rating)">
                  {{ rating.noise_level_rating }}/10
                </v-chip>
              </div>
              <v-slider
                v-model="rating.noise_level_rating"
                :min="1"
                :max="10"
                :step="0.5"
                :color="getScoreColor(10 - rating.noise_level_rating)"
                track-color="grey-lighten-1"
                show-ticks="always"
                :tick-size="4"
              ></v-slider>
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="rating.comment"
                label="Additional Comments"
                rows="3"
                hide-details
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" variant="text" @click="dialog = false">Cancel</v-btn>
        <v-btn
          color="primary"
          @click="submitRating"
          :loading="loading"
          :disabled="loading"
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