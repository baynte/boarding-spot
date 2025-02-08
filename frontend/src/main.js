import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// Leaflet
import 'leaflet/dist/leaflet.css'

// Initialize axios auth header from localStorage
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',    // Material Blue
          secondary: '#64B5F6',  // Lighter Blue
          accent: '#82B1FF',     // Blue accent
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
    },
  },
  defaults: {
    VBtn: {
      variant: 'flat',
      style: 'text-transform: none; font-weight: 500;',
    },
    VCard: {
      elevation: 0,
      border: true,
    },
  },
})

// Import base styles
import '@/assets/base.css'
import '@/assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app') 