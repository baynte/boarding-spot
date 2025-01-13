import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    userType: localStorage.getItem('userType') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isLandlord: (state) => state.userType === 'landlord',
    isTenant: (state) => state.userType === 'tenant'
  },
  
  actions: {
    async login(email, password) {
      try {
        const response = await axios.post('http://localhost:5000/auth/login', {
          email,
          password
        })
        
        this.token = response.data.access_token
        this.userType = response.data.user_type
        
        localStorage.setItem('token', this.token)
        localStorage.setItem('userType', this.userType)
        
        // Set default Authorization header for all future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },
    
    async register(email, password, userType) {
      try {
        await axios.post('http://localhost:5000/auth/register', {
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
      localStorage.removeItem('token')
      localStorage.removeItem('userType')
      delete axios.defaults.headers.common['Authorization']
    }
  }
}) 