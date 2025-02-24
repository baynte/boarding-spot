<template>
  <div class="register-container">
    <v-container class="fill-height mt-12" fluid>
      <v-row align-items="center" justify="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="elevation-12 rounded-lg">
            <v-toolbar color="primary" dark flat class="rounded-t-lg">
              <v-toolbar-title class="text-h5 font-weight-bold"> Create Account </v-toolbar-title>
            </v-toolbar>

            <v-card-text class="pa-6">
              <v-form @submit.prevent="handleSubmit" ref="form">
                <v-text-field
                  v-model="email"
                  :rules="[rules.required, rules.email]"
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
              <router-link to="/login" class="text-primary font-weight-bold text-decoration-none">
                Sign in
              </router-link>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
        {{ snackbarText }}
      </v-snackbar>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref(null)
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const userType = ref('')
const showPassword = ref(false)
const loading = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

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

const contactNumberRules = [
  (v) => !v || /^\+?[\d\s-]+$/.test(v) || 'Contact number must be valid',
  (v) =>
    !userType.value ||
    userType.value !== 'landlord' ||
    !!v ||
    'Contact number is required for landlords',
]

const handleSubmit = async () => {
  const { valid } = await form.value.validate()

  if (!valid) return

  loading.value = true

  try {
    await auth.register(email.value, password.value, userType.value)
    snackbarText.value = 'Registration successful! Please login.'
    snackbarColor.value = 'success'
    snackbar.value = true
    router.push('/login')
  } catch (error) {
    snackbarText.value = error.response?.data?.error || 'Registration failed'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}
</script>
