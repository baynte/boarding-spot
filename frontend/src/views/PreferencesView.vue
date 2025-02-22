<template>
  <div class="preferences-container pa-4">
    <h1 class="text-h4 mb-6 mt-6 text-left primary--text">Living Space Preferences</h1>

    <v-card elevation="3" class="rounded-lg">
      <v-card-text>
        <v-form @submit.prevent="savePreferences" ref="form">
          <v-container>
            <!-- Basic Information Section -->
            <v-row>
              <v-col cols="12">
                <div class="text-h6 mb-4 primary--text">
                  <v-icon icon="mdi-information" class="mr-2"></v-icon>
                  Basic Information
                </div>
              </v-col>

              <v-col cols="12" md="6">
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
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="preferences.min_capacity"
                  label="Minimum Capacity"
                  type="number"
                  :rules="[rules.required, rules.positive]"
                  hint="Minimum number of people"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.min_capacity"
                  variant="outlined"
                  density="comfortable"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="preferences.preferred_location"
                  label="Preferred Location"
                  :rules="[rules.required]"
                  hint="Your preferred area or neighborhood"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.preferred_location"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-map-marker"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="preferences.living_space_type"
                  :items="livingSpaceTypes"
                  label="Living Space Type"
                  hint="Select your preferred type"
                  persistent-hint
                  clearable
                  :error-messages="errors.living_space_type"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-home"
                ></v-select>
              </v-col>

              <v-col cols="12">
                <v-combobox
                  v-model="preferences.required_amenities"
                  :items="commonAmenities"
                  label="Required Amenities"
                  multiple
                  chips
                  :rules="[rules.required, rules.amenities]"
                  hint="Select important amenities"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.required_amenities"
                  variant="outlined"
                  density="comfortable"
                ></v-combobox>
              </v-col>
            </v-row>

            <!-- Importance Weights Section -->
            <v-row class="mt-6">
              <v-col cols="12">
                <div class="text-h6 primary--text d-flex align-center">
                  <v-icon icon="mdi-scale-balance" class="mr-2"></v-icon>
                  Importance Weights
                  <v-tooltip location="right">
                    <template v-slot:activator="{ props }">
                      <v-icon v-bind="props" icon="mdi-help-circle" class="ml-2" size="small"></v-icon>
                    </template>
                    <span>Adjust these values to prioritize your preferences. Total must equal 100%.</span>
                  </v-tooltip>
                </div>
                <div class="text-caption mb-4">All weights must sum to 100%</div>
              </v-col>

              <v-col cols="12" sm="6" v-for="(value, key) in weights" :key="key">
                <v-card flat class="pa-2">
                  <v-slider
                    v-model="weights[key]"
                    :label="key.charAt(0).toUpperCase() + key.slice(1)"
                    thumb-label="always"
                    :min="0"
                    :max="100"
                    :step="5"
                    @update:model-value="normalizeWeights(key)"
                    class="ml-2"
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="weights[key]"
                        type="number"
                        style="width: 70px"
                        density="compact"
                        hide-details
                        variant="outlined"
                        @update:model-value="normalizeWeights(key)"
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-card>
              </v-col>

              <v-col cols="12">
                <v-alert
                  :type="totalWeight === 100 ? 'success' : 'warning'"
                  variant="tonal"
                  class="mt-2"
                >
                  Total Weight: {{ totalWeight }}%
                </v-alert>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="elevated"
          @click="savePreferences"
          :loading="loading"
          :disabled="loading || !isFormValid"
          size="large"
          prepend-icon="mdi-content-save"
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
import axios from '@/plugins/axios'

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
  required_amenities: [],
  living_space_type: null
})

const weights = ref({
  safety: 25,
  cleanliness: 25,
  accessibility: 25,
  noise: 25
})

const errors = ref({
  max_price: '',
  min_capacity: '',
  preferred_location: '',
  required_amenities: '',
  weights: '',
  living_space_type: ''
})

const totalWeight = computed(() => {
  return Object.values(weights.value).reduce((sum, weight) => sum + Number(weight), 0)
})

const isFormValid = computed(() => {
  return totalWeight.value === 100 &&
         preferences.value.max_price > 0 &&
         preferences.value.min_capacity > 0 &&
         preferences.value.preferred_location.trim() !== '' &&
         preferences.value.required_amenities.length > 0 &&
         preferences.value.living_space_type !== null
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

const livingSpaceTypes = [
  'Boarding House',
  'Apartment',
  'House',
  'Dormitory',
  'Condo Unit'
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
    const response = await axios.get('/tenant/preferences')
    if (response.data) {
      preferences.value = {
        max_price: response.data.max_price,
        min_capacity: response.data.min_capacity,
        preferred_location: response.data.preferred_location,
        required_amenities: response.data.required_amenities,
        living_space_type: response.data.living_space_type
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
    const response = await axios.post('/tenant/preferences', {
      max_price: Number(preferences.value.max_price),
      min_capacity: Number(preferences.value.min_capacity),
      preferred_location: preferences.value.preferred_location.trim(),
      required_amenities: preferences.value.required_amenities,
      living_space_type: preferences.value.living_space_type,
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