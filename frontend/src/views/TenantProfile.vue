<template>
  <div class="profile-container">
    <v-container class="my-12">
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card elevation="6" rounded="lg" class="pa-6">
            <v-card-title class="text-h4 font-weight-bold mb-6 text-center">
              Tenant Profile
            </v-card-title>

            <v-card-text>
              <!-- Profile Picture Section -->
              <div class="text-center mb-8">
                <v-hover v-slot="{ isHovering, props }">
                  <v-avatar
                    size="180"
                    class="mb-4 elevation-3"
                    v-bind="props"
                  >
                    <v-img
                      :src="profile.avatar_url || '/default-avatar.png'"
                      alt="Profile Picture"
                      cover
                      :class="{ 'opacity-75': isHovering }"
                    >
                      <template v-slot:placeholder>
                        <v-row align-items="center" justify="center">
                          <v-progress-circular color="primary" indeterminate></v-progress-circular>
                        </v-row>
                      </template>
                    </v-img>
                  </v-avatar>
                </v-hover>
                <div class="mt-2">
                  <v-file-input
                    v-model="avatarFile"
                    accept="image/*"
                    hide-details
                    class="hidden-input"
                    @change="handleAvatarChange"
                  ></v-file-input>
                  <v-btn
                    color="primary"
                    variant="outlined"
                    prepend-icon="mdi-camera"
                    @click="triggerFileInput"
                  >
                    Change Photo
                  </v-btn>
                </div>
              </div>

              <v-form @submit.prevent="updateProfile" class="px-md-6">
                <div class="mb-8">
                  <div class="text-h6 font-weight-medium mb-4">Basic Information</div>
                  <v-text-field
                    v-model="profile.email"
                    label="Email Address"
                    type="email"
                    readonly
                    variant="outlined"
                    density="comfortable"
                    bg-color="grey-lighten-4"
                    class="mb-4"
                    prepend-inner-icon="mdi-email"
                  ></v-text-field>

                  <v-text-field
                    v-model="profile.full_name"
                    label="Full Name"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-account"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="profile.contact_number"
                    label="Contact Number"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-phone"
                    class="mb-4"
                  ></v-text-field>

                  <v-textarea
                    v-model="profile.bio"
                    label="About Me"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-text-box"
                    rows="3"
                    auto-grow
                  ></v-textarea>
                </div>

                <v-divider class="mb-8"></v-divider>

                <div class="mb-6">
                  <div class="text-h6 font-weight-medium mb-4">Security</div>
                  <v-text-field
                    v-model="profile.currentPassword"
                    label="Current Password"
                    type="password"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-lock"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="profile.newPassword"
                    label="New Password"
                    type="password"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-lock-plus"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="profile.confirmPassword"
                    label="Confirm New Password"
                    type="password"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-lock-check"
                  ></v-text-field>
                </div>

                <v-alert
                  v-if="errorMessage"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                >
                  {{ errorMessage }}
                </v-alert>

                <v-alert
                  v-if="successMessage"
                  type="success"
                  variant="tonal"
                  class="mb-4"
                >
                  {{ successMessage }}
                </v-alert>

                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                  class="mt-6"
                >
                  Save Changes
                </v-btn>
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
import axios from '@/plugins/axios'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const avatarFile = ref(null)

const profile = ref({
  email: '',
  full_name: '',
  contact_number: '',
  bio: '',
  avatar_url: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const fetchProfile = async () => {
  loading.value = true
  errorMessage.value = ''
  
  try {
    const response = await axios.get('/tenant/profile')
    profile.value.email = response.data.email
    profile.value.full_name = response.data.full_name || ''
    profile.value.contact_number = response.data.contact_number || ''
    profile.value.bio = response.data.bio || ''
    profile.value.avatar_url = response.data.avatar_url
  } catch (error) {
    console.error('Error fetching profile:', error)
    errorMessage.value = error.response?.data?.error || 'Failed to load profile data'
  } finally {
    loading.value = false
  }
}

const updateProfile = async () => {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  // Validate passwords if changing
  if (profile.value.newPassword || profile.value.currentPassword) {
    if (!profile.value.currentPassword) {
      errorMessage.value = 'Current password is required'
      loading.value = false
      return
    }
    if (profile.value.newPassword !== profile.value.confirmPassword) {
      errorMessage.value = 'New passwords do not match'
      loading.value = false
      return
    }
  }

  try {
    const updateData = {
      full_name: profile.value.full_name,
      contact_number: profile.value.contact_number,
      bio: profile.value.bio,
      current_password: profile.value.currentPassword,
      new_password: profile.value.newPassword
    }

    await axios.put('/tenant/profile', updateData)
    successMessage.value = 'Profile updated successfully'
    
    // Clear password fields after successful update
    profile.value.currentPassword = ''
    profile.value.newPassword = ''
    profile.value.confirmPassword = ''
  } catch (error) {
    console.error('Error updating profile:', error)
    errorMessage.value = error.response?.data?.error || 'Failed to update profile'
  } finally {
    loading.value = false
  }
}

const triggerFileInput = () => {
  document.querySelector('.hidden-input input').click()
}

const handleAvatarChange = async () => {
  if (!avatarFile.value) return
  
  loading.value = true
  errorMessage.value = ''
  
  try {
    const formData = new FormData()
    formData.append('avatar', avatarFile.value)
    
    const response = await axios.post('/tenant/profile/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    profile.value.avatar_url = response.data.avatar_url
    successMessage.value = 'Profile picture updated successfully'
  } catch (error) {
    console.error('Error uploading avatar:', error)
    errorMessage.value = error.response?.data?.error || 'Failed to upload profile picture'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}

.hidden-input {
  display: none;
}

.v-avatar {
  border: 2px solid #e0e0e0;
}
</style> 