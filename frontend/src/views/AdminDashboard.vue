<template>
  <div class="admin-dashboard">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="text-h4 py-4 px-6">
              Admin Dashboard
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Stats Cards -->
      <v-row>
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2" color="primary" theme="dark">
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold">{{ dashboardData.tenant_count || 0 }}</div>
              <div class="text-subtitle-1">Total Tenants</div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2" color="secondary" theme="dark">
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold">{{ dashboardData.landlord_count || 0 }}</div>
              <div class="text-subtitle-1">Total Landlords</div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card class="mb-4" elevation="2" color="info" theme="dark">
            <v-card-text class="text-center">
              <div class="text-h3 font-weight-bold">{{ dashboardData.room_count || 0 }}</div>
              <div class="text-subtitle-1">Total Rooms</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Recent Users -->
      <v-row>
        <v-col cols="12">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="py-4 px-6">
              Recent Users
            </v-card-title>
            <v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Email</th>
                    <th>Type</th>
                    <th>Created At</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in dashboardData.recent_users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                      <v-chip
                        :color="user.user_type === 'tenant' ? 'primary' : 'secondary'"
                        size="small"
                      >
                        {{ user.user_type }}
                      </v-chip>
                    </td>
                    <td>{{ formatDate(user.created_at) }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- All Users -->
      <v-row>
        <v-col cols="12">
          <v-card elevation="2">
            <v-card-title class="py-4 px-6 d-flex align-center">
              <span>All Users</span>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-inner-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                density="compact"
                class="ml-4"
                style="max-width: 300px"
              ></v-text-field>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="users"
                :search="search"
                :loading="loading"
                class="elevation-1"
              >
                <template v-slot:item.user_type="{ item }">
                  <v-chip
                    :color="item.user_type === 'tenant' ? 'primary' : 'secondary'"
                    size="small"
                  >
                    {{ item.user_type }}
                  </v-chip>
                </template>
                <template v-slot:item.is_admin="{ item }">
                  <v-chip
                    :color="item.is_admin ? 'success' : 'grey'"
                    size="small"
                  >
                    {{ item.is_admin ? 'Yes' : 'No' }}
                  </v-chip>
                </template>
                <template v-slot:item.created_at="{ item }">
                  {{ formatDate(item.created_at) }}
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    icon
                    size="small"
                    color="primary"
                    @click="openEditDialog(item)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    
    <!-- Edit User Dialog -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Edit User</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.email"
                  label="Email"
                  disabled
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.user_type"
                  :items="['tenant', 'landlord']"
                  label="User Type"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-switch
                  v-model="editedItem.is_admin"
                  label="Admin Status"
                  color="primary"
                  hide-details
                ></v-switch>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="editDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" variant="text" @click="saveUser">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const auth = useAuthStore()
const router = useRouter()

// Check if user is admin
if (!auth.isAdminUser) {
  router.push('/admin/login')
}

const dashboardData = ref({
  tenant_count: 0,
  landlord_count: 0,
  room_count: 0,
  recent_users: []
})

const users = ref([])
const loading = ref(true)
const search = ref('')

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Email', key: 'email' },
  { title: 'Type', key: 'user_type' },
  { title: 'Admin', key: 'is_admin' },
  { title: 'Created At', key: 'created_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const editDialog = ref(false)
const editedItem = ref({
  id: null,
  email: '',
  user_type: '',
  is_admin: false
})

// Format date
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    const response = await axios.get('/admin/dashboard')
    dashboardData.value = response.data
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

// Fetch all users
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await axios.get('/admin/users')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
}

// Open edit dialog
const openEditDialog = (item) => {
  editedItem.value = { ...item }
  editDialog.value = true
}

// Save user changes
const saveUser = async () => {
  try {
    await axios.put(`/admin/users/${editedItem.value.id}`, {
      user_type: editedItem.value.user_type,
      is_admin: editedItem.value.is_admin
    })
    
    // Update local data
    const index = users.value.findIndex(user => user.id === editedItem.value.id)
    if (index !== -1) {
      Object.assign(users.value[index], editedItem.value)
    }
    
    editDialog.value = false
    
    // Refresh data
    fetchDashboardData()
    fetchUsers()
  } catch (error) {
    console.error('Error updating user:', error)
  }
}

// Load data on component mount
onMounted(() => {
  fetchDashboardData()
  fetchUsers()
})
</script> 