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
            <h2 class="text-h6 d-flex align-center primary--text font-weight-medium">
          <v-icon icon="mdi-scale-balance" class="mr-2"></v-icon>
          Importance Weights
          <v-tooltip location="right">
            <template v-slot:activator="{ props }">
              <v-icon
            v-bind="props"
            icon="mdi-help-circle-outline"
            class="ml-2"
            size="small"
            color="grey"
              ></v-icon>
            </template>
            <span>Adjust these values to prioritize your preferences. Total must equal 100%.</span>
          </v-tooltip>
            </h2>
            <v-divider class="mt-2 mb-4"></v-divider>
          </v-col>

          <v-col cols="12" md="6" class="pb-0">
            <v-card flat class="pa-4 rounded-lg bg-grey-lighten-4">
          <div class="d-flex align-center mb-2">
            <v-icon icon="mdi-shield-check" color="success" class="mr-2"></v-icon>
            <span class="text-subtitle-1">Safety</span>
          </div>
          <v-slider
            v-model="weights.safety"
            :min="0"
            :max="100"
            :step="5"
            @update:model-value="normalizeWeights('safety')"
            color="success"
          >
            <template v-slot:append>
              <v-text-field
            v-model="weights.safety"
            type="number"
            style="width: 70px"
            density="compact"
            hide-details
            variant="outlined"
            @update:model-value="normalizeWeights('safety')"
              ></v-text-field>
            </template>
          </v-slider>
            </v-card>
          </v-col>

          <v-col cols="12" md="6" class="pb-0">
            <v-card flat class="pa-4 rounded-lg bg-grey-lighten-4">
          <div class="d-flex align-center mb-2">
            <v-icon icon="mdi-broom" color="info" class="mr-2"></v-icon>
            <span class="text-subtitle-1">Cleanliness</span>
          </div>
          <v-slider
            v-model="weights.cleanliness"
            :min="0"
            :max="100"
            :step="5"
            @update:model-value="normalizeWeights('cleanliness')"
            color="info"
          >
            <template v-slot:append>
              <v-text-field
            v-model="weights.cleanliness"
            type="number"
            style="width: 70px"
            density="compact"
            hide-details
            variant="outlined"
            @update:model-value="normalizeWeights('cleanliness')"
              ></v-text-field>
            </template>
          </v-slider>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card flat class="pa-4 rounded-lg bg-grey-lighten-4">
          <div class="d-flex align-center mb-2">
            <v-icon icon="mdi-map-marker-path" color="warning" class="mr-2"></v-icon>
            <span class="text-subtitle-1">Accessibility</span>
          </div>
          <v-slider
            v-model="weights.accessibility"
            :min="0"
            :max="100"
            :step="5"
            @update:model-value="normalizeWeights('accessibility')"
            color="warning"
          >
            <template v-slot:append>
              <v-text-field
            v-model="weights.accessibility"
            type="number"
            style="width: 70px"
            density="compact"
            hide-details
            variant="outlined"
            @update:model-value="normalizeWeights('accessibility')"
              ></v-text-field>
            </template>
          </v-slider>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card flat class="pa-4 rounded-lg bg-grey-lighten-4">
          <div class="d-flex align-center mb-2">
            <v-icon icon="mdi-volume-medium" color="error" class="mr-2"></v-icon>
            <span class="text-subtitle-1">Noise Level</span>
          </div>
          <v-slider
            v-model="weights.noise"
            :min="0"
            :max="100"
            :step="5"
            @update:model-value="normalizeWeights('noise')"
            color="error"
          >
            <template v-slot:append>
              <v-text-field
            v-model="weights.noise"
            type="number"
            style="width: 70px"
            density="compact"
            hide-details
            variant="outlined"
            @update:model-value="normalizeWeights('noise')"
              ></v-text-field>
            </template>
          </v-slider>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-alert
          :type="totalWeight === 100 ? 'success' : 'warning'"
          variant="tonal"
          :icon="totalWeight === 100 ? 'mdi-check-circle' : 'mdi-alert'"
          class="mt-4"
          density="comfortable"
            >
          <strong>Total Weight: {{ totalWeight }}%</strong>
          <div v-if="totalWeight !== 100" class="text-caption mt-1">
            Please adjust the weights to sum up to 100%
          </div>
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

const isFormValid = computed(() => {
  return (
    totalWeight.value === 100 &&
    preferences.value.max_price > 0 &&
    preferences.value.min_capacity > 0 &&
    preferences.value.preferred_location.trim() !== '' &&
    preferences.value.required_amenities.length > 0 &&
    preferences.value.living_space_type !== null &&
    preferences.value.preferred_distance > 0
  )
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
  // Convert all weights to numbers first
  Object.keys(weights.value).forEach((key) => {
    weights.value[key] = Number(weights.value[key]) || 0
  })

  const total = Object.values(weights.value).reduce((sum, weight) => sum + weight, 0)
  if (total === 0) {
    // Reset to default equal weights if total is 0
    Object.keys(weights.value).forEach((key) => {
      weights.value[key] = 25
    })
    return
  }

  const factor = 100 / total
  Object.keys(weights.value).forEach((key) => {
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
      preferred_distance: Number(preferences.value.preferred_distance),
      safety_weight: weights.value.safety / 100,
      cleanliness_weight: weights.value.cleanliness / 100,
      accessibility_weight: weights.value.accessibility / 100,
      noise_level_weight: weights.value.noise / 100,
    })

    snackbarText.value = 'Preferences saved successfully'
    snackbarColor.value = 'success'
    snackbar.value = true
    
    // Force a refresh of the search page to ensure it loads with the new preferences
    router.push({ 
      path: '/search', 
      query: { 
        refresh: Date.now(),
        maxDistance: Number(preferences.value.preferred_distance)
      } 
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
