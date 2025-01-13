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
                  prefix="$"
                  :rules="[rules.required, rules.positive]"
                  hint="Your maximum budget for rent"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.max_price"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="preferences.min_size"
                  label="Minimum Size (sq ft)"
                  type="number"
                  :rules="[rules.required, rules.positive]"
                  hint="Minimum room size you're comfortable with"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.min_size"
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
                  :min="0"
                  :max="100"
                  :step="5"
                  @update:model-value="normalizeWeights('safety')"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.safety"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      @update:model-value="normalizeWeights('safety')"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.cleanliness"
                  label="Cleanliness Importance"
                  thumb-label
                  :min="0"
                  :max="100"
                  :step="5"
                  @update:model-value="normalizeWeights('cleanliness')"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.cleanliness"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      @update:model-value="normalizeWeights('cleanliness')"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.accessibility"
                  label="Accessibility Importance"
                  thumb-label
                  :min="0"
                  :max="100"
                  :step="5"
                  @update:model-value="normalizeWeights('accessibility')"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.accessibility"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      @update:model-value="normalizeWeights('accessibility')"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12" sm="6">
                <v-slider
                  v-model="weights.noise"
                  label="Noise Level Importance"
                  thumb-label
                  :min="0"
                  :max="100"
                  :step="5"
                  @update:model-value="normalizeWeights('noise')"
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="weights.noise"
                      type="number"
                      style="width: 70px"
                      density="compact"
                      hide-details
                      @update:model-value="normalizeWeights('noise')"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>

              <v-col cols="12">
                <div class="d-flex align-center">
                  <div class="text-subtitle-1">Total Weight:</div>
                  <div :class="{'text-error': totalWeight !== 100, 'text-success': totalWeight === 100}" class="ml-2">
                    {{ totalWeight }}%
                  </div>
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
  min_size: null,
  preferred_location: '',
  required_amenities: []
})

const weights = ref({
  safety: 25,
  cleanliness: 25,
  accessibility: 25,
  noise: 25
})

const errors = ref({
  max_price: '',
  min_size: '',
  preferred_location: '',
  required_amenities: '',
  weights: ''
})

const totalWeight = computed(() => {
  return Object.values(weights.value).reduce((sum, weight) => sum + Number(weight), 0)
})

const isFormValid = computed(() => {
  return totalWeight.value === 100 &&
         preferences.value.max_price > 0 &&
         preferences.value.min_size > 0 &&
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
  required: v => !!v || 'Field is required',
  positive: v => v > 0 || 'Must be greater than 0',
  amenities: v => v && v.length > 0 || 'At least one amenity is required'
}

onMounted(async () => {
  await fetchPreferences()
})

const fetchPreferences = async () => {
  try {
    const response = await axios.get('http://localhost:5000/tenant/preferences')
    if (response.data) {
      preferences.value = {
        max_price: response.data.max_price,
        min_size: response.data.min_size,
        preferred_location: response.data.preferred_location,
        required_amenities: response.data.required_amenities
      }
      weights.value = {
        safety: response.data.safety_weight * 100,
        cleanliness: response.data.cleanliness_weight * 100,
        accessibility: response.data.accessibility_weight * 100,
        noise: response.data.noise_level_weight * 100
      }
    }
  } catch (error) {
    snackbarText.value = 'Error fetching preferences'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const normalizeWeights = (changedWeight) => {
  // Convert all weights to numbers first
  Object.keys(weights.value).forEach(key => {
    weights.value[key] = Number(weights.value[key]) || 0
  })

  const total = Object.values(weights.value).reduce((sum, weight) => sum + weight, 0)
  if (total === 0) {
    // Reset to default equal weights if total is 0
    Object.keys(weights.value).forEach(key => {
      weights.value[key] = 25
    })
    return
  }

  const factor = 100 / total
  Object.keys(weights.value).forEach(key => {
    if (key !== changedWeight) {
      weights.value[key] = Math.round(weights.value[key] * factor)
    }
  })

  // Ensure the changed weight is also a number
  weights.value[changedWeight] = Number(weights.value[changedWeight]) || 0

  // Adjust for rounding errors by putting the remainder in the changed weight
  const newTotal = Object.values(weights.value).reduce((sum, weight) => sum + weight, 0)
  if (newTotal !== 100) {
    const diff = 100 - newTotal
    weights.value[changedWeight] += diff
  }
}

const savePreferences = async () => {
  const { valid } = await form.value.validate()
  if (!valid) {
    snackbarText.value = 'Please fill in all required fields correctly'
    snackbarColor.value = 'error'
    snackbar.value = true
    return
  }

  // Validate weights total
  const totalWeight = Object.values(weights.value).reduce((sum, weight) => sum + weight, 0)
  if (Math.abs(totalWeight - 100) > 0.01) {
    snackbarText.value = 'Importance weights must sum to 100%'
    snackbarColor.value = 'error'
    snackbar.value = true
    return
  }

  loading.value = true

  try {
    const response = await axios.post('http://localhost:5000/tenant/preferences', {
      max_price: Number(preferences.value.max_price),
      min_size: Number(preferences.value.min_size),
      preferred_location: preferences.value.preferred_location.trim(),
      required_amenities: preferences.value.required_amenities,
      safety_weight: weights.value.safety / 100,
      cleanliness_weight: weights.value.cleanliness / 100,
      accessibility_weight: weights.value.accessibility / 100,
      noise_level_weight: weights.value.noise / 100
    })

    snackbarText.value = 'Preferences saved successfully'
    snackbarColor.value = 'success'
    snackbar.value = true
    router.push('/search')
  } catch (error) {
    console.error('Error saving preferences:', error)
    snackbarText.value = error.response?.data?.error || 'Error saving preferences'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}
</script> 