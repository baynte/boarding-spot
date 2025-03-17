import { defineStore } from 'pinia'
import axios from '@/utils/axios'

export const useAuthStore = defineStore('auth', {
  state: () => {
    // Initialize state from localStorage with proper logging
    const pendingVerification = localStorage.getItem('pendingVerification')
    console.log('Auth store initialized with pendingVerification:', pendingVerification)
    
    return {
      user: null,
      token: localStorage.getItem('token') || null,
      userType: localStorage.getItem('userType') || null,
      isAdmin: localStorage.getItem('isAdmin') === 'true' || false,
      pendingVerification: pendingVerification || null
    }
  },
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isLandlord: (state) => state.userType === 'landlord',
    isTenant: (state) => state.userType === 'tenant',
    isAdminUser: (state) => state.isAdmin,
    hasPendingVerification: (state) => !!state.pendingVerification
  },
  
  actions: {
    async login(email, password) {
      try {
        const response = await axios.post('/auth/login', {
          email,
          password
        })
        
        this.token = response.data.access_token
        this.userType = response.data.user_type
        this.isAdmin = response.data.is_admin
        
        localStorage.setItem('token', this.token)
        localStorage.setItem('userType', this.userType)
        localStorage.setItem('isAdmin', this.isAdmin)
        
        // Clear any pending verification
        this.pendingVerification = null
        localStorage.removeItem('pendingVerification')
        console.log('Cleared pendingVerification after successful login')
        
        return true
      } catch (error) {
        // All accounts are auto-verified now, so we don't need to check for verification errors
        console.error('Login error:', error)
        throw error
      }
    },
    
    async register(email, password, userType, contactNumber) {
      try {
        const response = await axios.post('/auth/register', {
          email,
          password,
          user_type: userType,
          contact_number: contactNumber
        })
        
        return {
          success: true,
          requiresVerification: response.data.email_verification_required
        }
      } catch (error) {
        throw error
      }
    },
    
    async resendVerificationEmail(email) {
      try {
        console.log('Auth store: Resending verification email to:', email)
        const response = await axios.post('/auth/resend-verification', { email })
        console.log('Auth store: Resend verification response:', response.data)
        return true
      } catch (error) {
        console.error('Auth store: Error resending verification email:', error)
        if (error.response) {
          console.error('Auth store: Error response data:', error.response.data)
        }
        throw error
      }
    },
    
    setPendingVerification(email) {
      console.log('Auth store: Manually setting pendingVerification to:', email)
      this.pendingVerification = email
      if (email) {
        localStorage.setItem('pendingVerification', email)
      } else {
        localStorage.removeItem('pendingVerification')
      }
    },
    
    clearPendingVerification() {
      console.log('Auth store: Clearing pendingVerification')
      this.pendingVerification = null
      localStorage.removeItem('pendingVerification')
    },
    
    logout() {
      this.token = null
      this.userType = null
      this.user = null
      this.isAdmin = false
      this.pendingVerification = null
      localStorage.removeItem('token')
      localStorage.removeItem('userType')
      localStorage.removeItem('isAdmin')
      localStorage.removeItem('pendingVerification')
      console.log('Auth store: Logged out and cleared all state')
    }
  }
}) 