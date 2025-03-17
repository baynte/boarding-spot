<template>
  <v-dialog v-model="dialog" persistent max-width="500">
    <v-card class="rounded-lg">
      <v-toolbar color="primary" dark flat class="rounded-t-lg">
        <v-toolbar-title class="text-h5 font-weight-bold">Email Verification Required</v-toolbar-title>
      </v-toolbar>

      <v-card-text class="pa-6 text-center">
        <v-icon size="64" color="primary" class="mb-4">mdi-email-check</v-icon>
        <h2 class="text-h5 mb-4">Verify Your Email</h2>
        <p class="mb-4">
          We've sent a verification email to <strong>{{ emailToVerify }}</strong>. Please check your inbox and click the verification link to activate your account.
        </p>
        <p class="mb-6 text-body-2">
          If you don't see the email, check your spam folder or click the button below to resend the verification email.
        </p>

        <v-alert
          v-if="message"
          :type="messageType"
          class="mb-4"
          dense
        >
          {{ message }}
        </v-alert>
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-btn
          color="primary"
          variant="elevated"
          @click="resendVerification"
          :loading="loading"
          :disabled="loading"
          block
          size="large"
          class="mb-3"
        >
          <v-icon start>mdi-email-send</v-icon>
          Resend Verification Email
        </v-btn>

        <v-btn
          color="grey-lighten-1"
          variant="text"
          @click="closeDialog"
          block
          size="large"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  email: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const router = useRouter()
const loading = ref(false)
const message = ref('')
const messageType = ref('info')

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const emailToVerify = computed(() => props.email)

const resendVerification = async () => {
  if (!emailToVerify.value) {
    message.value = 'No email address found for verification'
    messageType.value = 'error'
    return
  }
  
  loading.value = true
  message.value = ''
  
  try {
    const response = await axios.post('/auth/resend-verification', { email: emailToVerify.value })
    message.value = response.data.message || 'Verification email sent successfully!'
    messageType.value = 'success'
    
    // If the account was auto-verified, close the dialog and redirect to login
    if (response.data.message && response.data.message.includes('automatically verified')) {
      setTimeout(() => {
        closeDialog()
      }, 2000) // Close after 2 seconds to let the user read the message
    }
  } catch (error) {
    if (error.response) {
      message.value = error.response.data.error || 'Failed to send verification email'
    } else if (error.request) {
      message.value = 'Network error. Please check your connection.'
    } else {
      message.value = error.message || 'Failed to send verification email'
    }
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const closeDialog = () => {
  dialog.value = false
  router.push('/login')
}
</script> 