import { defineStore } from 'pinia'
import axios from '@/utils/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    userType: localStorage.getItem('userType') || null,
    isAdmin: localStorage.getItem('isAdmin') === 'true' || false
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isLandlord: (state) => state.userType === 'landlord',
    isTenant: (state) => state.userType === 'tenant',
    isAdminUser: (state) => state.isAdmin
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
        
        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },
    
    async register(email, password, userType) {
      try {
        await axios.post('/auth/register', {
          email,
          password,
          user_type: userType
        })
        return true
      } catch (error) {
        console.error('Registration error:', error)
        throw error
      }
    },
    
    logout() {
      this.token = null
      this.userType = null
      this.user = null
      this.isAdmin = false
      localStorage.removeItem('token')
      localStorage.removeItem('userType')
      localStorage.removeItem('isAdmin')
    }
  }
}) 