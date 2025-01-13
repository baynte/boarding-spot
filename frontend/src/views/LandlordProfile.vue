<template>
  <div>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h5 mb-2">
              Profile Settings
            </v-card-title>

            <v-card-text>
              <v-alert
                v-if="successMessage"
                type="success"
                class="mb-4"
              >
                {{ successMessage }}
              </v-alert>

              <v-alert
                v-if="errorMessage"
                type="error"
                class="mb-4"
              >
                {{ errorMessage }}
              </v-alert>

              <v-form @submit.prevent="updateProfile" ref="form">
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="profile.email"
                      label="Email"
                      type="email"
                      :rules="[rules.required, rules.email]"
                      readonly
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <v-text-field
                      v-model="profile.contact_number"
                      label="Contact Number"
                      :rules="[rules.required, rules.phone]"
                      placeholder="Enter your contact number"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <v-text-field
                      v-model="profile.currentPassword"
                      label="Current Password"
                      type="password"
                      :rules="[rules.required]"
                      placeholder="Enter current password to make changes"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <v-text-field
                      v-model="profile.newPassword"
                      label="New Password (Optional)"
                      type="password"
                      :rules="[rules.passwordOptional]"
                      placeholder="Leave blank to keep current password"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <v-text-field
                      v-model="profile.confirmPassword"
                      label="Confirm New Password"
                      type="password"
                      :rules="[rules.passwordMatch]"
                      placeholder="Confirm new password"
                      :disabled="!profile.newPassword"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-row class="mt-4">
                  <v-col cols="12">
                    <v-btn
                      color="primary"
                      type="submit"
                      :loading="loading"
                      block
                    >
                      Update Profile
                    </v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const router = useRouter()
const form = ref(null)
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const profile = ref({
  email: '',
  contact_number: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const rules = {
  required: v => !!v || 'This field is required',
  email: v => /.+@.+\..+/.test(v) || 'Please enter a valid email',
  phone: v => /^\+?[\d\s-]{10,}$/.test(v) || 'Please enter a valid phone number',
  passwordOptional: v => !v || v.length >= 8 || 'Password must be at least 8 characters',
  passwordMatch: v => !profile.value.newPassword || v === profile.value.newPassword || 'Passwords must match'
}

const fetchProfile = async () => {
  try {
    const response = await axios.get('/landlord/profile')
    profile.value.email = response.data.email
    profile.value.contact_number = response.data.contact_number
  } catch (error) {
    errorMessage.value = 'Failed to load profile data'
    console.error('Error fetching profile:', error)
  }
}

const updateProfile = async () => {
  if (!form.value.validate()) return

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const updateData = {
      contact_number: profile.value.contact_number,
      current_password: profile.value.currentPassword
    }

    if (profile.value.newPassword) {
      updateData.new_password = profile.value.newPassword
    }

    await axios.put('/landlord/profile', updateData)
    successMessage.value = 'Profile updated successfully'
    
    // Clear sensitive fields
    profile.value.currentPassword = ''
    profile.value.newPassword = ''
    profile.value.confirmPassword = ''
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Failed to update profile'
    console.error('Error updating profile:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script> 