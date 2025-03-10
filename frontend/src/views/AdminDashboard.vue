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
      
      <!-- Navigation Tabs -->
      <v-tabs v-model="activeTab" bg-color="primary" centered dark class="mb-6 rounded-lg elevation-2">
        <v-tab value="dashboard">
          <v-icon start>mdi-view-dashboard</v-icon>
          Dashboard
        </v-tab>
        <v-tab value="users">
          <v-icon start>mdi-account-group</v-icon>
          Users
        </v-tab>
        <v-tab value="pending-rooms">
          <v-icon start>mdi-home-clock</v-icon>
          Pending Rooms
          <v-badge v-if="pendingRooms.length > 0" :content="pendingRooms.length" color="error" offset-x="10" offset-y="-10"></v-badge>
        </v-tab>
      </v-tabs>
      
      <v-window v-model="activeTab">
        <!-- Dashboard Tab -->
        <v-window-item value="dashboard">
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
        </v-window-item>
        
        <!-- Users Tab -->
        <v-window-item value="users">
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
        </v-window-item>
        
        <!-- Pending Rooms Tab -->
        <v-window-item value="pending-rooms">
          <v-row>
            <v-col cols="12">
              <v-card elevation="2" rounded="xl">
                <v-card-title class="py-6 px-8 bg-surface-variant d-flex align-center">
                  <v-icon size="28" color="primary" class="mr-3">mdi-home-clock</v-icon>
                  <span class="text-h5">Pending Room Approvals</span>
                  <v-chip
                    v-if="pendingRooms.length > 0"
                    color="warning"
                    class="ml-3"
                    size="small"
                  >
                    {{ pendingRooms.length }} pending
                  </v-chip>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="roomSearch"
                    prepend-inner-icon="mdi-magnify"
                    label="Search rooms..."
                    single-line
                    hide-details
                    density="comfortable"
                    variant="outlined"
                    class="search-field mx-4"
                    bg-color="white"
                    clearable
                  ></v-text-field>
                  <v-btn color="primary" prepend-icon="mdi-refresh" @click="fetchPendingRooms">
                    Refresh
                  </v-btn>
                </v-card-title>
                
                <v-card-text class="pa-6">
                  <div v-if="loadingPendingRooms" class="d-flex justify-center align-center py-8">
                    <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
                  </div>
                  
                  <div v-else-if="pendingRooms.length === 0" class="text-center py-8">
                    <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-check-circle</v-icon>
                    <div class="text-h5 text-grey-darken-1">No pending rooms to approve</div>
                    <div class="text-body-1 text-grey">All rooms have been reviewed</div>
                  </div>
                  
                  <div v-else-if="filteredRooms.length === 0" class="text-center py-8">
                    <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-magnify-close</v-icon>
                    <div class="text-h5 text-grey-darken-1">No matching rooms found</div>
                    <div class="text-body-1 text-grey">
                      Try adjusting your search term or 
                      <v-btn variant="text" color="primary" @click="roomSearch = ''">clear the filter</v-btn>
                    </div>
                  </div>
                  
                  <div v-else>
                    <v-expansion-panels>
                      <v-expansion-panel
                        v-for="room in paginatedRooms"
                        :key="room.id"
                        class="mb-4"
                        rounded="lg"
                      >
                        <v-expansion-panel-title>
                          <div class="d-flex align-center">
                            <v-avatar size="40" class="mr-4" rounded>
                              <v-img
                                :src="room.image_urls && room.image_urls.length > 0 ? room.image_urls[0] : '/default-room.jpg'"
                                cover
                              ></v-img>
                            </v-avatar>
                            <div>
                              <div class="text-subtitle-1 font-weight-bold">{{ room.title }}</div>
                              <div class="text-caption text-grey">{{ room.location }} - ₱{{ room.price.toLocaleString() }}</div>
                            </div>
                          </div>
                        </v-expansion-panel-title>
                        
                        <v-expansion-panel-text>
                          <v-row>
                            <v-col cols="12" md="6">
                              <v-carousel
                                height="300"
                                hide-delimiters
                                show-arrows="hover"
                                v-if="room.image_urls && room.image_urls.length > 0"
                              >
                                <v-carousel-item
                                  v-for="(image, i) in room.image_urls"
                                  :key="i"
                                  :src="image"
                                  cover
                                ></v-carousel-item>
                              </v-carousel>
                              <v-img
                                v-else
                                src="/default-room.jpg"
                                height="300"
                                cover
                              ></v-img>
                            </v-col>
                            
                            <v-col cols="12" md="6">
                              <div class="text-h6 font-weight-bold mb-2">Room Details</div>
                              <v-list density="compact">
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="primary">mdi-currency-php</v-icon>
                                  </template>
                                  <v-list-item-title>Price: ₱{{ room.price.toLocaleString() }}</v-list-item-title>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="primary">mdi-account-group</v-icon>
                                  </template>
                                  <v-list-item-title>Capacity: {{ room.capacity }} person(s)</v-list-item-title>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="primary">mdi-map-marker</v-icon>
                                  </template>
                                  <v-list-item-title>Location: {{ room.location }}</v-list-item-title>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="primary">mdi-home-variant</v-icon>
                                  </template>
                                  <v-list-item-title>Type: {{ room.living_space_type }}</v-list-item-title>
                                </v-list-item>
                              </v-list>
                              
                              <div class="text-h6 font-weight-bold mt-4 mb-2">Landlord Information</div>
                              <v-list density="compact">
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="primary">mdi-email</v-icon>
                                  </template>
                                  <v-list-item-title>{{ room.landlord.email }}</v-list-item-title>
                                </v-list-item>
                                
                                <v-list-item v-if="room.landlord.contact_number">
                                  <template v-slot:prepend>
                                    <v-icon color="primary">mdi-phone</v-icon>
                                  </template>
                                  <v-list-item-title>{{ room.landlord.contact_number }}</v-list-item-title>
                                </v-list-item>
                              </v-list>
                              
                              <div class="text-h6 font-weight-bold mt-4 mb-2">Amenities</div>
                              <v-chip-group>
                                <v-chip
                                  v-for="amenity in room.amenities"
                                  :key="amenity"
                                  color="primary"
                                  variant="outlined"
                                  size="small"
                                  class="font-weight-medium"
                                >
                                  {{ amenity }}
                                </v-chip>
                                <v-chip
                                  v-if="!room.amenities || room.amenities.length === 0"
                                  color="grey"
                                  variant="outlined"
                                  size="small"
                                  class="font-weight-medium"
                                >
                                  No amenities listed
                                </v-chip>
                              </v-chip-group>
                              
                              <div class="text-h6 font-weight-bold mt-4 mb-2">Description</div>
                              <p class="text-body-1">{{ room.description }}</p>
                            </v-col>
                          </v-row>
                          
                          <v-divider class="my-4"></v-divider>
                          
                          <v-row>
                            <v-col cols="12">
                              <v-textarea
                                v-model="room.adminNotes"
                                label="Admin Notes"
                                hint="Add notes about this room (required for rejection)"
                                persistent-hint
                                rows="3"
                                variant="outlined"
                              ></v-textarea>
                            </v-col>
                          </v-row>
                          
                          <v-row class="mt-2">
                            <v-col cols="12" class="d-flex justify-end">
                              <v-btn
                                color="error"
                                variant="outlined"
                                prepend-icon="mdi-close"
                                class="mr-4"
                                @click="rejectRoom(room)"
                                :disabled="!room.adminNotes"
                              >
                                Reject
                              </v-btn>
                              <v-btn
                                color="success"
                                variant="elevated"
                                prepend-icon="mdi-check"
                                @click="approveRoom(room)"
                              >
                                Approve
                              </v-btn>
                            </v-col>
                          </v-row>
                        </v-expansion-panel-text>
                      </v-expansion-panel>
                    </v-expansion-panels>
                    
                    <!-- Pagination -->
                    <div class="d-flex flex-column align-center mt-6">
                      <div class="text-caption text-grey mb-2">
                        Showing {{ paginationStart }} - {{ paginationEnd }} of {{ filteredRooms.length }} rooms
                        <span v-if="roomSearch && filteredRooms.length !== pendingRooms.length">
                          (filtered from {{ pendingRooms.length }} total)
                        </span>
                      </div>
                      <v-pagination
                        v-model="currentPage"
                        :length="totalPages"
                        :total-visible="7"
                        rounded="circle"
                        color="primary"
                      ></v-pagination>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>
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
            <!-- <v-col cols="12">
              <v-switch
                v-model="editedItem.is_admin"
                label="Admin Status"
                color="success"
                hide-details
                inset
              ></v-switch>
            </v-col> -->
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
    
    <!-- Notification Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
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
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const auth = useAuthStore()
const router = useRouter()

// Check if user is admin
if (!auth.isAdminUser) {
  router.push('/admin/login')
}

// Tab navigation
const activeTab = ref('dashboard')

const dashboardData = ref({
  tenant_count: 0,
  landlord_count: 0,
  room_count: 0,
  recent_users: []
})

const users = ref([])
const loading = ref(true)
const search = ref('')

// Pending rooms data
const pendingRooms = ref([])
const loadingPendingRooms = ref(false)
const roomSearch = ref('')

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

// Notification
const snackbar = ref(false)
const snackbarColor = ref('')
const snackbarText = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 5
const totalPages = computed(() => Math.ceil(filteredRooms.value.length / itemsPerPage))

// Computed property for filtered rooms
const filteredRooms = computed(() => {
  if (!roomSearch.value) return pendingRooms.value
  
  const searchTerm = roomSearch.value.toLowerCase()
  return pendingRooms.value.filter(room => 
    room.title.toLowerCase().includes(searchTerm) ||
    room.description.toLowerCase().includes(searchTerm) ||
    room.location.toLowerCase().includes(searchTerm) ||
    room.living_space_type.toLowerCase().includes(searchTerm)
  )
})

// Computed property for paginated rooms
const paginatedRooms = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return filteredRooms.value.slice(startIndex, endIndex)
})

// Computed properties for pagination summary
const paginationStart = computed(() => {
  if (filteredRooms.value.length === 0) return 0
  return (currentPage.value - 1) * itemsPerPage + 1
})

const paginationEnd = computed(() => {
  if (filteredRooms.value.length === 0) return 0
  return Math.min(currentPage.value * itemsPerPage, filteredRooms.value.length)
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

// Fetch pending rooms
const fetchPendingRooms = async () => {
  loadingPendingRooms.value = true
  try {
    const response = await axios.get('/admin/rooms/pending')
    pendingRooms.value = response.data.map(room => ({
      ...room,
      adminNotes: room.admin_notes || '',
      // Ensure amenities are properly parsed
      amenities: parseAmenities(room.amenities),
      // Ensure image URLs are properly parsed
      image_urls: parseImageUrls(room.image_urls)
    }))
    
    // Reset pagination to first page
    currentPage.value = 1
  } catch (error) {
    console.error('Error fetching pending rooms:', error)
  } finally {
    loadingPendingRooms.value = false
  }
}

// Helper function to parse amenities
const parseAmenities = (amenitiesData) => {
  if (!amenitiesData) return []
  
  try {
    // If it's already an array, return it
    if (Array.isArray(amenitiesData)) return amenitiesData
    
    // If it's a string, try to parse it as JSON
    return JSON.parse(amenitiesData)
  } catch (error) {
    console.error('Error parsing amenities:', error)
    return []
  }
}

// Helper function to parse image URLs
const parseImageUrls = (imageUrlsData) => {
  if (!imageUrlsData) return []
  
  try {
    // If it's already an array, return it
    if (Array.isArray(imageUrlsData)) return imageUrlsData
    
    // If it's a string, try to parse it as JSON
    return JSON.parse(imageUrlsData)
  } catch (error) {
    console.error('Error parsing image URLs:', error)
    return []
  }
}

// Approve a room
const approveRoom = async (room) => {
  try {
    await axios.put(`/admin/rooms/${room.id}/approve`, {
      admin_notes: room.adminNotes
    })
    
    // Remove the room from the pending list
    pendingRooms.value = pendingRooms.value.filter(r => r.id !== room.id)
    
    // Show success message
    snackbar.value = true
    snackbarColor.value = 'success'
    snackbarText.value = 'Room approved successfully'
    
    // Refresh dashboard data
    fetchDashboardData()
  } catch (error) {
    console.error('Error approving room:', error)
    snackbar.value = true
    snackbarColor.value = 'error'
    snackbarText.value = 'Failed to approve room: ' + (error.response?.data?.error || 'Unknown error')
  }
}

// Reject a room
const rejectRoom = async (room) => {
  if (!room.adminNotes) {
    snackbar.value = true
    snackbarColor.value = 'error'
    snackbarText.value = 'Admin notes are required for rejection'
    return
  }
  
  try {
    await axios.put(`/admin/rooms/${room.id}/reject`, {
      admin_notes: room.adminNotes
    })
    
    // Remove the room from the pending list
    pendingRooms.value = pendingRooms.value.filter(r => r.id !== room.id)
    
    // Show success message
    snackbar.value = true
    snackbarColor.value = 'success'
    snackbarText.value = 'Room rejected successfully'
    
    // Refresh dashboard data
    fetchDashboardData()
  } catch (error) {
    console.error('Error rejecting room:', error)
    snackbar.value = true
    snackbarColor.value = 'error'
    snackbarText.value = 'Failed to reject room: ' + (error.response?.data?.error || 'Unknown error')
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
      is_admin: editedItem.value.is_admin,
      is_landlord_approved: editedItem.value.is_landlord_approved
    })
    
    // Update local data
    const index = users.value.findIndex(user => user.id === editedItem.value.id)
    if (index !== -1) {
      Object.assign(users.value[index], editedItem.value)
    }
    
    editDialog.value = false
    
    // Show success message
    snackbar.value = true
    snackbarColor.value = 'success'
    snackbarText.value = 'User updated successfully'
    
    // Refresh data
    fetchDashboardData()
    fetchUsers()
  } catch (error) {
    console.error('Error updating user:', error)
    snackbar.value = true
    snackbarColor.value = 'error'
    snackbarText.value = 'Failed to update user: ' + (error.response?.data?.error || 'Unknown error')
  }
}

// Delete user
const deleteUser = async (item) => {
  if (!confirm(`Are you sure you want to delete user ${item.email}? This action cannot be undone.`)) {
    return
  }
  
  try {
    await axios.delete(`/admin/users/${item.id}`)
    
    // Remove user from local data
    users.value = users.value.filter(user => user.id !== item.id)
    
    // Show success message
    snackbar.value = true
    snackbarColor.value = 'success'
    snackbarText.value = 'User deleted successfully'
    
    // Refresh dashboard data
    fetchDashboardData()
  } catch (error) {
    console.error('Error deleting user:', error)
    snackbar.value = true
    snackbarColor.value = 'error'
    snackbarText.value = 'Failed to delete user: ' + (error.response?.data?.error || 'Unknown error')
  }
}

// Watch for changes in search term to reset pagination
watch(roomSearch, () => {
  currentPage.value = 1
})

// Load data on component mount
onMounted(() => {
  fetchDashboardData()
  fetchUsers()
  fetchPendingRooms()
})
</script> 