<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
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
              Login
            </v-btn>
          </v-card-actions>

          <v-card-text class="text-center">
            Don't have an account?
            <router-link to="/register">Register here</router-link>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref(null)
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const rules = {
  required: v => !!v || 'Field is required',
  email: v => /.+@.+\..+/.test(v) || 'Email must be valid',
  min: v => v.length >= 6 || 'Min 6 characters'
}

const handleSubmit = async () => {
  const { valid } = await form.value.validate()
  
  if (!valid) return
  
  loading.value = true
  
  try {
    await auth.login(email.value, password.value)
    snackbarText.value = 'Login successful!'
    snackbarColor.value = 'success'
    snackbar.value = true
    
    // Set the redirect path based on user type
    const redirectPath = auth.isLandlord ? '/landlord' : '/tenant'
    
    // Navigate first, then refresh
    await router.push(redirectPath)
    window.location.reload()
  } catch (error) {
    snackbarText.value = error.response?.data?.error || 'Login failed'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}
</script> 