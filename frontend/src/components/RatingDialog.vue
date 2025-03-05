<template>
  <v-dialog v-model="dialog" max-width="700px" transition="fade-transition">
    <template v-slot:activator="{ props }">
      <v-btn
        color="primary"
        v-bind="props"
        :disabled="!canRate"
        :title="!canRate ? 'Only tenants can rate Rental types' : ''"
        @click.stop
        variant="elevated"
        prepend-icon="mdi-star"
        class="px-6 py-2 text-capitalize font-weight-medium"
        elevation="3"
        rounded
      >
        {{ hasRated ? 'Update Rating' : 'Rate Rental type' }}
      </v-btn>
    </template>

    <v-card elevation="4" class="rounded-lg">
      <v-card-title class="py-6 px-8 bg-primary text-white d-flex align-center">
        <v-icon size="28" class="mr-3">mdi-star-circle</v-icon>
        <span class="text-h5 font-weight-bold">{{ hasRated ? 'Update Rating' : 'Rate Rental type' }}</span>
      </v-card-title>

      <v-card-text class="pt-6 px-8">
        <v-container>
          <v-row>
            <v-col cols="12" class="pb-2">
              <h3 class="text-h6 font-weight-bold mb-6">How would you rate your experience?</h3>
            </v-col>

            <template v-for="(item, index) in [
              { label: 'Safety', model: 'safety_rating', icon: 'mdi-shield-check' },
              { label: 'Cleanliness', model: 'cleanliness_rating', icon: 'mdi-broom' },
              { label: 'Accessibility', model: 'accessibility_rating', icon: 'mdi-door' },
              { label: 'Noise Level', model: 'noise_level_rating', icon: 'mdi-volume-high' }
            ]" :key="index">
              <v-col cols="12" class="py-2">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="d-flex align-center">
                    <v-icon :icon="item.icon" class="mr-2" size="20"></v-icon>
                    <span class="text-subtitle-1 font-weight-medium">{{ item.label }}</span>
                  </div>
                  <v-chip
                    size="small"
                    :color="getScoreColor(item.model === 'noise_level_rating' ? 10 - rating[item.model] : rating[item.model])"
                    class="font-weight-bold px-2"
                    variant="elevated"
                  >
                    {{ rating[item.model] }}/10
                  </v-chip>
                </div>
                <v-slider
                  v-model="rating[item.model]"
                  :min="1"
                  :max="10"
                  :step="0.5"
                  :color="getScoreColor(item.model === 'noise_level_rating' ? 10 - rating[item.model] : rating[item.model])"
                  track-color="grey-lighten-3"
                  show-ticks="always"
                  :tick-size="3"
                  thumb-label="always"
                  class="mt-1"
                ></v-slider>
              </v-col>
            </template>

            <v-col cols="12" class="pt-4">
              <v-textarea
                v-model="rating.comment"
                label="Share your experience (optional)"
                rows="3"
                variant="outlined"
                counter
                maxlength="500"
                auto-grow
                class="mt-2"
                density="comfortable"
                bg-color="grey-lighten-4"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-6">
        <v-spacer></v-spacer>
        <v-btn 
          color="grey-darken-1" 
          variant="text" 
          @click="dialog = false"
          class="px-6 text-capitalize"
          :disabled="loading"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="submitRating"
          :loading="loading"
          :disabled="loading"
          class="px-8 text-capitalize ml-4"
          elevation="2"
        >
          <v-icon left class="mr-2">mdi-check</v-icon>
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