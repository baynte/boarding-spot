<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          
          <v-card-text>
            <v-form @submit.prevent="handleSubmit" ref="form">
              <v-text-field
                v-model="email"
                :rules="[rules.required, rules.email]"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
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
                required
              ></v-text-field>

              <v-text-field
                v-model="confirmPassword"
                :rules="[rules.required, rules.passwordMatch]"
                label="Confirm Password"
                prepend-icon="mdi-lock-check"
                :type="showPassword ? 'text' : 'password'"
                required
              ></v-text-field>

              <v-text-field
                v-model="contactNumber"
                label="Contact Number"
                :rules="contactNumberRules"
                persistent-hint
                hint="Enter your contact number (required for landlords)"
              ></v-text-field>

              <v-select
                v-model="userType"
                :items="userTypes"
                :rules="[rules.required]"
                label="Account Type"
                prepend-icon="mdi-account"
                required
              ></v-select>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="handleSubmit"
              :loading="loading"
              :disabled="loading"
            >
              Register
            </v-btn>
          </v-card-actions>

          <v-card-text class="text-center">
            Already have an account?
            <router-link to="/login">Login here</router-link>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
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
  { title: 'Tenant', value: 'tenant' }
]

const rules = {
  required: v => !!v || 'Field is required',
  email: v => /.+@.+\..+/.test(v) || 'Email must be valid',
  min: v => v.length >= 6 || 'Min 6 characters',
  passwordMatch: v => v === password.value || 'Passwords must match'
}

const contactNumberRules = [
  v => !v || /^\+?[\d\s-]+$/.test(v) || 'Contact number must be valid',
  v => !userType.value || userType.value !== 'landlord' || !!v || 'Contact number is required for landlords'
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