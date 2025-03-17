<template>
  <div class="login-container">
    <v-container class="fill-height mt-12" fluid>
      <v-row align-items="center" justify="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="rounded-lg" elevation="12">
            <v-toolbar color="primary" dark flat class="rounded-t-lg">
              <v-toolbar-title class="text-h5 font-weight-medium"> Welcome Back </v-toolbar-title>
            </v-toolbar>

            <v-card-text class="pa-6">
              <v-form @submit.prevent="handleSubmit" ref="form">
              <v-text-field
                v-model="email"
                :rules="[rules.required, rules.email]"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                required
                variant="outlined"
                density="comfortable"
                class="mb-4"
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
                variant="outlined"
                density="comfortable"
                @keyup.enter="handleSubmit"
              ></v-text-field>
              </v-form>
            </v-card-text>

            <v-card-actions class="pa-6 pt-0">
              <v-btn
              color="primary"
              @click="handleSubmit"
              :loading="loading"
              variant="elevated"
              size="large"
              type="submit"
              block
              class="mb-1"
              >
              <v-icon left class="mr-2">mdi-login</v-icon>
              Login
              </v-btn>
            </v-card-actions>

            <v-card-text class="text-center pb-2">
              <span class="text-medium-emphasis">Don't have an account? </span>
              <v-btn
                to="/register"
                color="secondary"
                variant="text"
                class="text-decoration-none font-weight-medium"
              >
                Register here
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

<style scoped>

</style>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import EmailVerification from '@/components/EmailVerification.vue'

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
const showVerificationDialog = ref(false)

const rules = {
  required: (v) => !!v || 'Field is required',
  email: (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
  min: (v) => v.length >= 6 || 'Min 6 characters',
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
    // All accounts are auto-verified now, so we don't need to check for verification errors
    snackbarText.value = error.response?.data?.error || 'Login failed'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}
</script>
