<template>
  <div class="register-container">
    <v-container class="fill-height mt-12" fluid>
      <v-row align-items="center" justify="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="rounded-lg" elevation="12">
            <v-toolbar color="primary" dark flat class="rounded-t-lg">
              <v-toolbar-title class="text-h5 font-weight-bold"> Create Account </v-toolbar-title>
            </v-toolbar>

            <v-card-text class="pa-6">
              <v-form @submit.prevent="handleSubmit" ref="form">
                <v-text-field
                  v-model="email"
                  :rules="emailRules"
                  label="Email"
                  prepend-icon="mdi-email"
                  type="email"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  :rules="[rules.required, rules.min]"
                  label="Password"
                  prepend-icon="mdi-lock"
                  :type="showPassword ? 'text' : 'password'"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="showPassword = !showPassword"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="confirmPassword"
                  :rules="[rules.required, rules.passwordMatch]"
                  label="Confirm Password"
                  prepend-icon="mdi-lock-check"
                  :type="showPassword ? 'text' : 'password'"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="contactNumber"
                  label="Contact Number"
                  :rules="contactNumberRules"
                  prepend-icon="mdi-phone"
                  persistent-hint
                  hint="Enter your contact number (required for landlords)"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                ></v-text-field>

                <v-select
                  v-model="userType"
                  :items="userTypes"
                  :rules="[rules.required]"
                  label="Account Type"
                  prepend-icon="mdi-account"
                  variant="outlined"
                  density="comfortable"
                  class="mt-6"
                  required
                   @keyup.enter="handleSubmit"
                ></v-select>
              </v-form>
            </v-card-text>

            <v-card-actions class="pa-6 pt-0">
              <v-btn
                color="primary"
                variant="elevated"
                @click="handleSubmit"
                :loading="loading"
                :disabled="loading"
                block
                size="large"
                class="mb-3"
              >
                <v-icon start>mdi-account-plus</v-icon>
                Register
              </v-btn>
            </v-card-actions>

            <v-card-text class="text-center pb-3">
              <span class="text-grey">Already have an account? </span>
              <v-btn
                to="/login"
                color="primary"
                variant="text"
                class="text-decoration-none font-weight-bold"
              >
                Sign in
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
        {{ snackbarText }}
      </v-snackbar>
      
      <!-- Email Verification Dialog -->
      <EmailVerification 
        v-model="showVerificationDialog" 
        :email="email"
      />
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import EmailVerification from '@/components/EmailVerification.vue'

const router = useRouter()
const auth = useAuthStore()

const form = ref(null)
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const userType = ref('')
const contactNumber = ref('')
const showPassword = ref(false)
const loading = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')
const showVerificationDialog = ref(false)

const userTypes = [
  { title: 'Landlord', value: 'landlord' },
  { title: 'Tenant', value: 'tenant' },
]

const rules = {
  required: (v) => !!v || 'Field is required',
  email: (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
  min: (v) => v.length >= 6 || 'Min 6 characters',
  passwordMatch: (v) => v === password.value || 'Passwords must match',
}

// Email validation rules with domain check for tenants
const emailRules = computed(() => {
  const baseRules = [
    rules.required,
    rules.email
  ]
  
  // Add domain validation for tenant accounts
  if (userType.value === 'tenant') {
    baseRules.push(
      (v) => v.endsWith('@smccnasipit.edu.ph') || 'Tenant accounts must use an @smccnasipit.edu.ph email address'
    )
  }
  
  return baseRules
})

const contactNumberRules = [
  (v) => !v || /^\+?[\d\s-]+$/.test(v) || 'Contact number must be valid',
  (v) =>
    !userType.value ||
    userType.value !== 'landlord' ||
    !!v ||
    'Contact number is required for landlords',
]

// Watch for user type changes to revalidate email
watch(userType, async () => {
  if (form.value) {
    await form.value.validate()
  }
})

const handleSubmit = async () => {
  const { valid } = await form.value.validate()

  if (!valid) {
    snackbarText.value = 'Please fix the form errors before submitting'
    snackbarColor.value = 'warning'
    snackbar.value = true
    return
  }

  loading.value = true

  try {
    const response = await auth.register(email.value, password.value, userType.value, contactNumber.value)
    
    // All accounts are auto-verified now, so we can just show success and redirect to login
    snackbarText.value = 'Registration successful! Please login.'
    snackbarColor.value = 'success'
    snackbar.value = true
    router.push('/login')
  } catch (error) {
    if (error.response) {
      snackbarText.value = error.response.data.error || 'Registration failed'
    } else if (error.request) {
      snackbarText.value = 'Network error. Please check your connection.'
    } else {
      snackbarText.value = error.message || 'Registration failed'
    }
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}
</script>
