<template>
  <div class="preferences-container pa-4">
    <h1 class="text-h4 mb-6 mt-6 text-left primary--text">Rental type Preferences</h1>
    <v-card elevation="3" class="rounded-lg">
      <v-card-text>
        <v-form @submit.prevent="savePreferences" ref="form">
          <v-container>
            <!-- Basic Information Section -->
            <v-row>
              <v-col cols="12">
                <h2 class="text-h6 d-flex align-center primary--text font-weight-medium">
                  <v-icon icon="mdi-information-outline" class="mr-2"></v-icon>
                  Basic Information
                </h2>
                <v-divider class="mt-2 mb-4"></v-divider>
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
                  class="custom-input"
                  bg-color="grey-lighten-4"
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
                  bg-color="grey-lighten-4"
                  prepend-inner-icon="mdi-account-group"
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
                  bg-color="grey-lighten-4"
                  prepend-inner-icon="mdi-map-marker"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="preferences.preferred_distance"
                  label="Maximum Distance from SMCC (km)"
                  type="number"
                  :rules="[rules.positive]"
                  hint="Maximum distance in kilometers from SMCC"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.preferred_distance"
                  variant="outlined"
                  density="comfortable"
                  bg-color="grey-lighten-4"
                  prepend-inner-icon="mdi-map-marker-distance"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="preferences.living_space_type"
                  :items="livingSpaceTypes"
                  label="Rental type"
                  hint="Select your preferred type"
                  persistent-hint
                  clearable
                  :error-messages="errors.living_space_type"
                  variant="outlined"
                  density="comfortable"
                  bg-color="grey-lighten-4"
                  prepend-inner-icon="mdi-home-outline"
                ></v-select>
              </v-col>

              <v-col cols="12">
                <v-combobox
                  v-model="preferences.required_amenities"
                  :items="commonAmenities"
                  label="Required Amenities"
                  multiple
                  chips
                  closable-chips
                  clearable
                  :rules="[rules.required, rules.amenities]"
                  hint="Select important amenities"
                  persistent-hint
                  validate-on="blur"
                  :error-messages="errors.required_amenities"
                  variant="outlined"
                  density="comfortable"
                  bg-color="grey-lighten-4"
                  prepend-inner-icon="mdi-star-outline"
                ></v-combobox>
              </v-col>
            </v-row>

            <!-- Importance Weights Section -->
            <v-row class="mt-8">
              <v-col cols="12">
                <div class="d-flex align-center mb-4">
                  <h2 class="text-h5 font-weight-bold primary--text">
                    <v-icon icon="mdi-scale-balance" class="mr-2" color="primary"></v-icon>
                    Importance Weights
                  </h2>
                  <v-tooltip location="right">
                    <template v-slot:activator="{ props }">
                      <v-icon
                        v-bind="props"
                        icon="mdi-help-circle-outline"
                        class="ml-3"
                        color="grey-darken-1"
                      ></v-icon>
                    </template>
                    <div class="pa-2">
                      <span>Adjust these values to prioritize your preferences.</span>
                      <br />
                      <span class="font-weight-medium">Values will be normalized to 100%</span>
                    </div>
                  </v-tooltip>
                </div>
                <v-divider class="mb-6"></v-divider>
              </v-col>

              <v-col cols="12">
                <v-card flat class="pa-8 rounded-xl bg-grey-lighten-5 border">
                  <!-- Weight Controls -->
                  <v-row>
                    <v-col cols="12" md="6">
                      <!-- Safety -->
                      <div class="weight-control mb-8">
                        <div class="d-flex align-center mb-2">
                          <v-icon icon="mdi-shield-check" color="success" size="large"></v-icon>
                          <span class="text-h6 font-weight-medium ml-3">Safety</span>
                          <v-spacer></v-spacer>
                          <v-text-field
                            v-model="weights.safety"
                            type="number"
                            style="max-width: 90px"
                            density="comfortable"
                            hide-details
                            variant="outlined"
                            @update:model-value="normalizeWeights('safety')"
                          ></v-text-field>
                        </div>
                        <v-slider
                          v-model="weights.safety"
                          :min="0"
                          :max="100"
                          :step="1"
                          @update:model-value="normalizeWeights('safety')"
                          color="success"
                          track-color="success-lighten-4"
                          thumb-label="always"
                        ></v-slider>
                      </div>

                      <!-- Cleanliness -->
                      <div class="weight-control mb-8">
                        <div class="d-flex align-center mb-2">
                          <v-icon icon="mdi-broom" color="info" size="large"></v-icon>
                          <span class="text-h6 font-weight-medium ml-3">Cleanliness</span>
                          <v-spacer></v-spacer>
                          <v-text-field
                            v-model="weights.cleanliness"
                            type="number"
                            style="max-width: 90px"
                            density="comfortable"
                            hide-details
                            variant="outlined"
                            @update:model-value="normalizeWeights('cleanliness')"
                          ></v-text-field>
                        </div>
                        <v-slider
                          v-model="weights.cleanliness"
                          :min="0"
                          :max="100"
                          :step="1"
                          @update:model-value="normalizeWeights('cleanliness')"
                          color="info"
                          track-color="info-lighten-4"
                        ></v-slider>
                      </div>
                    </v-col>

                    <v-col cols="12" md="6">
                      <!-- Accessibility -->
                      <div class="weight-control mb-8">
                        <div class="d-flex align-center mb-2">
                          <v-icon icon="mdi-map-marker-path" color="warning" size="large"></v-icon>
                          <span class="text-h6 font-weight-medium ml-3">Accessibility</span>
                          <v-spacer></v-spacer>
                          <v-text-field
                            v-model="weights.accessibility"
                            type="number"
                            style="max-width: 90px"
                            density="comfortable"
                            hide-details
                            variant="outlined"
                            @update:model-value="normalizeWeights('accessibility')"
                          ></v-text-field>
                        </div>
                        <v-slider
                          v-model="weights.accessibility"
                          :min="0"
                          :max="100"
                          :step="1"
                          @update:model-value="normalizeWeights('accessibility')"
                          color="warning"
                          track-color="warning-lighten-4"
                        ></v-slider>
                      </div>

                      <!-- Noise Level -->
                      <div class="weight-control mb-8">
                        <div class="d-flex align-center mb-2">
                          <v-icon icon="mdi-volume-medium" color="error" size="large"></v-icon>
                          <span class="text-h6 font-weight-medium ml-3">Noise Level</span>
                          <v-spacer></v-spacer>
                          <v-text-field
                            v-model="weights.noise"
                            type="number"
                            style="max-width: 90px"
                            density="comfortable"
                            hide-details
                            variant="outlined"
                            @update:model-value="normalizeWeights('noise')"
                          ></v-text-field>
                        </div>
                        <v-slider
                          v-model="weights.noise"
                          :min="0"
                          :max="100"
                          :step="1"
                          @update:model-value="normalizeWeights('noise')"
                          color="error"
                          track-color="error-lighten-4"
                        ></v-slider>
                      </div>
                    </v-col>
                  </v-row>

                  <!-- Total Weight Summary -->
                  <v-card
                    :color="totalWeight === 0 ? 'error' : 'primary'"
                    class="mt-4"
                    variant="outlined"
                  >
                    <v-card-text>
                      <div class="d-flex align-center">
                        <div>
                          <div class="text-h6 font-weight-bold">
                            Total Weight: {{ totalWeight }}%
                          </div>
                          <div class="text-body-2 mt-1">
                            Values will be automatically normalized when saved
                          </div>
                        </div>
                        <v-spacer></v-spacer>
                        <v-btn
                          :color="totalWeight === 0 ? 'white' : 'primary'"
                          variant="tonal"
                          @click="resetWeights"
                          prepend-icon="mdi-refresh"
                        >
                          Reset to Equal
                        </v-btn>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-card>
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
  living_space_type: null,
  preferred_distance: null,
})

const weights = ref({
  safety: 25,
  cleanliness: 25,
  accessibility: 25,
  noise: 25,
})

const errors = ref({
  max_price: '',
  min_capacity: '',
  preferred_location: '',
  required_amenities: '',
  weights: '',
  living_space_type: '',
  preferred_distance: '',
})

const totalWeight = computed(() => {
  return Object.values(weights.value).reduce((sum, weight) => sum + Number(weight), 0)
})

const remainingWeight = computed(() => {
  return 100 - totalWeight.value
})

const isFormValid = computed(() => {
  // Check if at least one weight is greater than 0
  const hasPositiveWeight = Object.values(weights.value).some((weight) => Number(weight) > 0)

  // Check other form fields
  const hasValidPrice = preferences.value.max_price > 0
  const hasValidCapacity = preferences.value.min_capacity > 0
  const hasValidLocation = preferences.value.preferred_location.trim() !== ''
  const hasValidAmenities = preferences.value.required_amenities.length > 0
  const hasValidType = preferences.value.living_space_type !== null
  const hasValidDistance = preferences.value.preferred_distance > 0

  // Log validation status for debugging
  console.log('Form validation status:', {
    hasPositiveWeight,
    hasValidPrice,
    hasValidCapacity,
    hasValidLocation,
    hasValidAmenities,
    hasValidType,
    hasValidDistance,
    weights: weights.value,
    preferences: preferences.value,
  })

  // Return true to enable the button regardless of validation
  // This is temporary to help debug the issue
  return true
})

const commonAmenities = [
  'Air Conditioning',
  'Appliances',
  'Backyard or garden',
  'CCTV',
  'Closet',
  'Common CR',
  'Convenience Store',
  'Curfew policy',
  'Double-Deck Bed',
  'Electricity Included',
  'Elevator',
  'Fan',
  'Fire Exits',
  'Fire Extinguisher',
  'Furnished',
  'Function room',
  'Gated property',
  'Gas/Induction Stove',
  'Gym/Fitness Gym',
  'Heating',
  'Kitchen',
  'Laundry',
  'Living room area',
  'Microwave',
  'Outdoor space',
  'Parking',
  'Pet-friendly',
  'Phone',
  'Private Bathroom',
  'Private garage',
  'Receiving Area',
  'Refrigerator',
  'Rice cooker',
  'Security Fingerprint',
  'Security Guard',
  'Security Keycard',
  'Single bed',
  'Storage room',
  'Study Desk',
  'Swimming Pool',
  'TV',
  'Unfurnished',
  'Washing Machine',
  'Water included',
  'WiFi',
]

const livingSpaceTypes = [
  'Boarding House',
  'Apartment',
  'House',
  'Condo',
  'Lodge',
  'Hotel',
  'Resort',
]

const rules = {
  required: (v) => !!v || 'Field is required',
  positive: (v) => v > 0 || 'Must be greater than 0',
  amenities: (v) => (v && v.length > 0) || 'At least one amenity is required',
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
        living_space_type: response.data.living_space_type,
        preferred_distance: response.data.preferred_distance,
      }
      weights.value = {
        safety: response.data.safety_weight * 100,
        cleanliness: response.data.cleanliness_weight * 100,
        accessibility: response.data.accessibility_weight * 100,
        noise: response.data.noise_level_weight * 100,
      }
    }
  } catch (error) {
    snackbarText.value = 'Error fetching preferences'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const normalizeWeights = (changedWeight) => {
  // Convert the changed weight to a number
  weights.value[changedWeight] = Number(weights.value[changedWeight]) || 0

  // Ensure the value is not negative
  if (weights.value[changedWeight] < 0) {
    weights.value[changedWeight] = 0
  }

  // Ensure the value is not greater than 100
  if (weights.value[changedWeight] > 100) {
    weights.value[changedWeight] = 100
  }

  // Round to nearest integer
  weights.value[changedWeight] = Math.round(weights.value[changedWeight])
}

// Reset weights to equal distribution (25% each)
const resetWeights = () => {
  Object.keys(weights.value).forEach((key) => {
    weights.value[key] = 25
  })
}

const savePreferences = async () => {
  try {
    // Skip form validation for now
    // const { valid } = await form.value.validate()
    // if (!valid) {
    //   snackbarText.value = 'Please fill in all required fields correctly'
    //   snackbarColor.value = 'error'
    //   snackbar.value = true
    //   return
    // }

    // Check if at least one weight is greater than 0
    const hasPositiveWeight = Object.values(weights.value).some((weight) => Number(weight) > 0)
    if (!hasPositiveWeight) {
      snackbarText.value = 'At least one importance weight must be greater than 0'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    // Validate required fields manually
    if (!preferences.value.max_price || preferences.value.max_price <= 0) {
      snackbarText.value = 'Maximum price must be greater than 0'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    if (!preferences.value.min_capacity || preferences.value.min_capacity <= 0) {
      snackbarText.value = 'Minimum capacity must be greater than 0'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    if (
      !preferences.value.preferred_location ||
      preferences.value.preferred_location.trim() === ''
    ) {
      snackbarText.value = 'Preferred location is required'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    if (
      !preferences.value.required_amenities ||
      preferences.value.required_amenities.length === 0
    ) {
      snackbarText.value = 'At least one required amenity is needed'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    if (!preferences.value.living_space_type) {
      snackbarText.value = 'Living space type is required'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    if (!preferences.value.preferred_distance || preferences.value.preferred_distance <= 0) {
      snackbarText.value = 'Preferred distance must be greater than 0'
      snackbarColor.value = 'error'
      snackbar.value = true
      return
    }

    loading.value = true

    // Create a copy of the weights and normalize them to sum to 1.0 for the backend
    // This doesn't change what the user sees in the UI
    const normalizedWeights = { ...weights.value }
    const totalWeightValue = Object.values(normalizedWeights).reduce(
      (sum, weight) => sum + Number(weight),
      0,
    )
    const factor = 100 / totalWeightValue

    Object.keys(normalizedWeights).forEach((key) => {
      normalizedWeights[key] = normalizedWeights[key] * factor
    })

    const response = await axios.post('/tenant/preferences', {
      max_price: Number(preferences.value.max_price),
      min_capacity: Number(preferences.value.min_capacity),
      preferred_location: preferences.value.preferred_location.trim(),
      required_amenities: preferences.value.required_amenities,
      living_space_type: preferences.value.living_space_type,
      preferred_distance: Number(preferences.value.preferred_distance),
      safety_weight: normalizedWeights.safety / 100,
      cleanliness_weight: normalizedWeights.cleanliness / 100,
      accessibility_weight: normalizedWeights.accessibility / 100,
      noise_level_weight: normalizedWeights.noise / 100,
    })

    snackbarText.value = 'Preferences saved successfully'
    snackbarColor.value = 'success'
    snackbar.value = true

    // Force a refresh of the search page to ensure it loads with the new preferences
    router.push({
      path: '/search',
      query: {
        refresh: Date.now(),
        maxDistance: Number(preferences.value.preferred_distance),
      },
    })
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

<style scoped>
.preferences-container {
  max-width: 1000px;
  margin: 0 auto;
}

.custom-input :deep(.v-field__input) {
  padding-top: 8px;
  padding-bottom: 8px;
}

/* Slider styling */
:deep(.v-slider .v-slider-thumb) {
  width: 20px;
  height: 20px;
}

:deep(.v-slider .v-slider-thumb__label) {
  font-weight: bold;
}

:deep(.v-slider-track__background) {
  height: 8px;
  border-radius: 4px;
}

:deep(.v-slider-track__fill) {
  height: 8px;
  border-radius: 4px;
}

.border {
  border: 1px solid rgba(0, 0, 0, 0.1);
}
</style>
