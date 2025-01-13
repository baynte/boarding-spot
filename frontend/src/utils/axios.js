import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Create axios instance with base URL
const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000'
})

// Add request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const auth = useAuthStore()
      auth.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default axiosInstance 