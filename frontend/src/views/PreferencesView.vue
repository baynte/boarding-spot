<template>
  <div>
    <h1 class="text-h4 mb-4">Room Preferences</h1>

    <v-card>
      <v-card-text>
        <v-form @submit.prevent="savePreferences" ref="form">
          <v-container>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="preferences.max_price"
                  label="Maximum Price"
                  type="number"
                  prefix="₱"
                  :rules="[rules.required, rules.positive]"
                  hint="Your maximum budget for rent"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.max_price"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="preferences.min_capacity"
                  label="Minimum Capacity"
                  type="number"
                  :rules="[rules.required, rules.positive, rules.integer]"
                  hint="Minimum number of occupants the room should accommodate"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.min_capacity"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="preferences.preferred_location"
                  label="Preferred Location"
                  :rules="[rules.required]"
                  hint="Your preferred area or neighborhood"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.preferred_location"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-combobox
                  v-model="preferences.required_amenities"
                  :items="commonAmenities"
                  label="Required Amenities"
                  multiple
                  chips
                  :rules="[rules.required, rules.amenities]"
                  hint="Select amenities that are important to you"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.required_amenities"
                ></v-combobox>
              </v-col>

              <v-col cols="12">
                <div class="text-h6 mb-2">Importance Weights</div>
                <p class="text-caption mb-4">
                  Adjust these sliders to indicate how important each factor is in your decision.
                  The total of all weights will automatically adjust to equal 100%.
                </p>
                <div v-if="errors.weights" class="text-error mb-2">{{ errors.weights }}</div>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.safety"
                  label="Safety Importance"
                  thumb-label
                  :min="1"
                  :max="10"
                  :step="1"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.safety"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      :min="1"
                      :max="10"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.cleanliness"
                  label="Cleanliness Importance"
                  thumb-label
                  :min="1"
                  :max="10"
                  :step="1"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.cleanliness"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      :min="1"
                      :max="10"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.accessibility"
                  label="Accessibility Importance"
                  thumb-label
                  :min="1"
                  :max="10"
                  :step="1"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.accessibility"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      :min="1"
                      :max="10"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.noise"
                  label="Noise Level Importance"
                  thumb-label
                  :min="1"
                  :max="10"
                  :step="1"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.noise"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      :min="1"
                      :max="10"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12">
                <div class="d-flex align-center">
                  <div class="text-subtitle-1">Importance Scale:</div>
                  <div class="ml-2">1 (Least Important) to 10 (Most Important)</div>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="savePreferences"
          :loading="loading"
          :disabled="loading || !isFormValid"
        >
          Save Preferences
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form = ref(null)
const loading = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const preferences = ref({
  max_price: null,
  min_capacity: null,
  preferred_location: '',
  required_amenities: []
})

const weights = ref({
  safety: 5,
  cleanliness: 5,
  accessibility: 5,
  noise: 5
})

const errors = ref({
  max_price: '',
  min_capacity: '',
  preferred_location: '',
  required_amenities: '',
  weights: ''
})

const totalWeight = computed(() => {
  return Object.values(weights.value).reduce((sum, weight) => sum + Number(weight), 0)
})

const isFormValid = computed(() => {
  return totalWeight.value === 10 &&
         Number(preferences.value.max_price) > 0 &&
         Number(preferences.value.min_capacity) > 0 &&
         Number.isInteger(Number(preferences.value.min_capacity)) &&
         !isNaN(preferences.value.max_price) &&
         !isNaN(preferences.value.min_capacity) &&
         preferences.value.preferred_location.trim() !== '' &&
         preferences.value.required_amenities.length > 0
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
  'Closet'
]

const rules = {
  required: v => !!v || 'This field is required',
  positive: v => (Number(v) > 0) || 'Must be greater than 0',
  integer: v => (Number.isInteger(Number(v)) && !isNaN(v)) || 'Must be a whole number',
  amenities: v => v.length > 0 || 'At least one amenity is required'
}

onMounted(async () => {
  await fetchPreferences()
})

const fetchPreferences = async () => {
  try {
    console.log('Fetching preferences...')
    const response = await axios.get('/tenant/preferences')
    console.log('Received preferences:', response.data)
    
    if (response.data) {
      // Backend returned preferences
      preferences.value = {
        max_price: response.data.max_price || null,
        min_capacity: response.data.min_capacity || null,
        preferred_location: response.data.preferred_location || '',
        required_amenities: response.data.required_amenities || []
      }
      weights.value = {
        safety: Math.round((response.data.safety_weight || 0.25) * 10),
        cleanliness: Math.round((response.data.cleanliness_weight || 0.25) * 10),
        accessibility: Math.round((response.data.accessibility_weight || 0.25) * 10),
        noise: Math.round((response.data.noise_level_weight || 0.25) * 10)
      }
      console.log('Set preferences to:', preferences.value)
      console.log('Set weights to:', weights.value)
    } else {
      // No preferences found, set defaults
      preferences.value = {
        max_price: null,
        min_capacity: null,
        preferred_location: '',
        required_amenities: []
      }
      weights.value = {
        safety: 5,
        cleanliness: 5,
        accessibility: 5,
        noise: 5
      }
      console.log('No preferences found, using defaults')
    }
  } catch (error) {
    console.error('Error fetching preferences:', error)
    snackbarText.value = error.response?.data?.error || 'Error fetching preferences'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const savePreferences = async () => {
  try {
    loading.value = true
    errors.value = {
      max_price: '',
      min_capacity: '',
      preferred_location: '',
      required_amenities: '',
      weights: ''
    }

    // Validate numbers
    if (isNaN(preferences.value.max_price) || Number(preferences.value.max_price) <= 0) {
      errors.value.max_price = 'Please enter a valid price'
      return
    }

    if (isNaN(preferences.value.min_capacity) || !Number.isInteger(Number(preferences.value.min_capacity)) || Number(preferences.value.min_capacity) <= 0) {
      errors.value.min_capacity = 'Please enter a valid number of occupants'
      return
    }

    const data = {
      max_price: Number(preferences.value.max_price),
      min_capacity: Number(preferences.value.min_capacity),
      preferred_location: preferences.value.preferred_location.trim(),
      required_amenities: preferences.value.required_amenities,
      safety_weight: weights.value.safety / 10,
      cleanliness_weight: weights.value.cleanliness / 10,
      accessibility_weight: weights.value.accessibility / 10,
      noise_level_weight: weights.value.noise / 10
    }

    await axios.post('/tenant/preferences', data)
    snackbarColor.value = 'success'
    snackbarText.value = 'Preferences saved successfully!'
    snackbar.value = true
  } catch (error) {
    console.error('Error saving preferences:', error)
    snackbarColor.value = 'error'
    snackbarText.value = error.response?.data?.error || 'Error saving preferences'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}
</script> 