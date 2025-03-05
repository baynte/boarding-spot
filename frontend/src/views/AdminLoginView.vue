<template>
  <div class="admin-login">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="pa-6 mt-10" elevation="10">
            <v-card-title class="text-center text-h4 mb-4">
              Admin Login
            </v-card-title>
            
            <v-alert
              v-if="error"
              type="error"
              class="mb-4"
              density="compact"
              closable
              @click:close="error = ''"
            >
              {{ error }}
            </v-alert>
            
            <v-form @submit.prevent="handleLogin" ref="form">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                required
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                variant="outlined"
                prepend-inner-icon="mdi-email"
                class="mb-4"
              ></v-text-field>
              
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
                :rules="[v => !!v || 'Password is required']"
                variant="outlined"
                prepend-inner-icon="mdi-lock"
                class="mb-6"
              ></v-text-field>
              
              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
              >
                Login
              </v-btn>
            </v-form>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const form = ref(null)

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  const { valid } = await form.value.validate()
  
  if (!valid) return
  
  loading.value = true
  error.value = ''
  
  try {
    await auth.login(email.value, password.value)
    
    if (auth.isAdminUser) {
      router.push('/admin/dashboard')
    } else {
      error.value = 'You do not have admin privileges'
      auth.logout()
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script> 