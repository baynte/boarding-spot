<template>
  <div class="admin-dashboard">
    <v-container fluid>
      <!-- Header -->
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6 mt-4" elevation="2" rounded="xl">
            <v-card-title class="text-h4 py-8 px-8 d-flex align-center bg-primary text-white">
              <v-icon size="36" class="mr-4">mdi-view-dashboard</v-icon>
              Admin Dashboard
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Stats Cards -->
      <v-row class="mb-8">
        <v-col cols="12" md="4">
          <v-card hover elevation="2" rounded="xl" class="stat-card gradient-primary" theme="dark">
            <v-card-text class="py-8 px-6">
              <div class="d-flex align-center">
                <div class="stat-icon-wrapper mr-6">
                  <v-icon size="42">mdi-account-group</v-icon>
                </div>
                <div>
                  <div class="text-h2 font-weight-bold mb-2">{{ dashboardData.tenant_count || 0 }}</div>
                  <div class="text-subtitle-1 text-medium-emphasis">Total of Tenants</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card hover elevation="2" rounded="xl" class="stat-card gradient-secondary" theme="dark">
            <v-card-text class="py-8 px-6">
              <div class="d-flex align-center">
                <div class="stat-icon-wrapper mr-6">
                  <v-icon size="42">mdi-home-account</v-icon>
                </div>
                <div>
                  <div class="text-h2 font-weight-bold mb-2">{{ dashboardData.landlord_count || 0 }}</div>
                  <div class="text-subtitle-1 text-medium-emphasis">Total of Landlords</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <v-card hover elevation="2" rounded="xl" class="stat-card gradient-info" theme="dark">
            <v-card-text class="py-8 px-6">
              <div class="d-flex align-center">
                <div class="stat-icon-wrapper mr-6">
                  <v-icon size="42">mdi-door</v-icon>
                </div>
                <div>
                  <div class="text-h2 font-weight-bold mb-2">{{ dashboardData.room_count || 0 }}</div>
                  <div class="text-subtitle-1 text-medium-emphasis">Total of Living Spaces</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Recent Users -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card elevation="2" rounded="xl">
            <v-card-title class="py-6 px-8 bg-surface-variant d-flex align-center">
              <v-icon size="28" color="primary" class="mr-3">mdi-clock-outline</v-icon>
              <span class="text-h5">Recent Users</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <v-table hover class="rounded">
                <thead>
                  <tr>
                    <th class="text-subtitle-1 font-weight-bold text-primary">ID</th>
                    <th class="text-subtitle-1 font-weight-bold text-primary">Email</th>
                    <th class="text-subtitle-1 font-weight-bold text-primary">Type</th>
                    <th class="text-subtitle-1 font-weight-bold text-primary">Created At</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in dashboardData.recent_users" :key="user.id" class="table-row">
                    <td class="text-body-1">#{{ user.id }}</td>
                    <td class="text-body-1">{{ user.email }}</td>
                    <td>
                      <v-chip
                        :color="user.user_type === 'tenant' ? 'primary' : 'secondary'"
                        size="small"
                        variant="flat"
                        class="font-weight-medium"
                      >
                        {{ user.user_type }}
                      </v-chip>
                    </td>
                    <td class="text-body-1">{{ formatDate(user.created_at) }}</td>
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
          <v-card elevation="2" rounded="xl">
            <v-card-title class="py-6 px-8 bg-surface-variant d-flex align-center">
              <v-icon size="28" color="primary" class="mr-3">mdi-account-multiple</v-icon>
              <span class="text-h5">All Users</span>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                label="Search users..."
                single-line
                hide-details
                density="comfortable"
                variant="outlined"
                class="search-field"
                bg-color="white"
              ></v-text-field>
            </v-card-title>
            <v-card-text class="pa-6">
              <v-data-table
                :headers="headers"
                :items="users"
                :search="search"
                :loading="loading"
                hover
                dense
                class="elevation-1 rounded"
              >
                <template v-slot:item.user_type="{ item }">
                  <v-chip
                    :color="item.user_type === 'tenant' ? 'primary' : 'secondary'"
                    size="small"
                    variant="flat"
                    class="font-weight-medium"
                  >
                    {{ item.user_type }}
                  </v-chip>
                </template>
                <template v-slot:item.is_admin="{ item }">
                  <v-chip
                    :color="item.is_admin ? 'success' : 'grey'"
                    size="small"
                    variant="flat"
                    class="font-weight-medium"
                  >
                    {{ item.is_admin ? 'Yes' : 'No' }}
                  </v-chip>
                </template>
                <template v-slot:item.created_at="{ item }">
                  {{ formatDate(item.created_at) }}
                </template>
                <template v-slot:item.is_landlord_approved="{ item }">
                  <v-chip
                    :color="item.is_landlord_approved ? 'success' : 'warning'"
                    size="small"
                    variant="flat"
                    class="font-weight-medium"
                  >
                    {{ item.is_landlord_approved ? 'Approved' : 'Pending' }}
                  </v-chip>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    icon
                    size="35"
                    color="primary"
                    variant="flat"
                    class="mr-2"
                    @click="openEditDialog(item)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    size="35"
                    color="error"
                    variant="flat"
                    @click="deleteUser(item)"
                  >
                    <v-icon>mdi-delete</v-icon>
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
      <v-card rounded="xl">
        <v-card-title class="text-h5 pa-6 bg-surface-variant d-flex align-center">
          <v-icon size="28" color="primary" class="mr-3">mdi-account-edit</v-icon>
          Edit User
        </v-card-title>
        <v-card-text class="pa-8">
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="editedItem.email"
                label="Email"
                disabled
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="editedItem.user_type"
                :items="['tenant', 'landlord']"
                label="User Type"
                variant="outlined"
                density="comfortable"
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-switch
                v-model="editedItem.is_admin"
                label="Admin Status"
                color="success"
                hide-details
                inset
              ></v-switch>
            </v-col>
            <v-col cols="12" >
              <v-switch
                v-model="editedItem.is_landlord_approved"
                label="Approve"
                color="success"
                hide-details
                inset
              ></v-switch>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn color="error" variant="outlined" @click="editDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" variant="elevated" class="ml-4" @click="saveUser">
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.stat-card {
  transition: all 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-6px);
}
.search-field {
  max-width: 300px;
}
.stat-icon-wrapper {
  padding: 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
}
.gradient-primary {
  background: linear-gradient(135deg, #1867C0 0%, #5CBBF6 100%);
}
.gradient-secondary {
  background: linear-gradient(135deg, #80ffc0 0%, #00ff40 100%);
}
.gradient-info {
  background: linear-gradient(135deg, #0288D1 0%, #4FC3F7 100%);
}
.table-row:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}
</style>

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
  { title: 'Status', key: 'is_landlord_approved' },
  { title: 'Created At', key: 'created_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const editDialog = ref(false)
const editedItem = ref({
  id: null,
  email: '',
  user_type: '',
  is_landlord_approved: false,
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