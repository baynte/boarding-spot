<template>
  <div class="dashboard-container pa-6">
    <!-- Header Section -->
    <v-container fluid class="header-section pb-6">
      <v-row align-items ="center" justify="space-between">
        <v-col cols="auto">
          <h1 class="text-h3 font-weight-bold primary--text">Landlord Dashboard</h1>
          <div class="text-subtitle-1 text-medium-emphasis mt-1">
            Manage your properties efficiently
          </div>
        </v-col>
        <v-col cols="auto">
          <v-btn
            color="primary"
            variant="elevated"
            prepend-icon="mdi-account-cog"
            to="/landlord/profile"
            class="elevation-2 mt-10"
          >
            Profile Settings
          </v-btn>
        </v-col>
      </v-row>

      <!-- Stats Cards -->
      <v-row class="mt-4 mb-3">
        <v-col cols="12" sm="4">
          <v-card elevation="3" class="stat-card rounded-lg" hover>
            <v-card-text class="pa-6">
              <div class="d-flex align-center">
                <v-icon size="36" color="primary" class="mr-4">mdi-home-group</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold mb-1">{{ rooms.length }}</div>
                  <div class="text-subtitle-1 text-medium-emphasis">Total Rooms</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card elevation="3" class="stat-card rounded-lg" hover>
            <v-card-text class="pa-6">
              <div class="d-flex align-center">
                <v-icon size="36" color="success" class="mr-4">mdi-check-circle</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold mb-1">{{ availableRooms }}</div>
                  <div class="text-subtitle-1 text-medium-emphasis">Available Rooms</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card elevation="3" class="stat-card rounded-lg" hover>
            <v-card-text class="pa-6">
              <div class="d-flex align-center">
                <v-icon size="36" color="info" class="mr-4">mdi-currency-php</v-icon>
                <div>
                  <div class="text-h4 font-weight-bold mb-1">
                    ₱{{ averagePrice.toLocaleString() }}
                  </div>
                  <div class="text-subtitle-1 text-medium-emphasis">Average Price</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Add Room Button -->
    <div class="d-flex justify-end mb-4">
      <v-btn color="primary" prepend-icon="mdi-plus" @click="dialog = true">
        Add Living Space
      </v-btn>
    </div>

    <!-- Add/Edit Room Dialog -->
    <v-dialog v-model="dialog" max-width="800px" persistent>
      <v-card class="rounded-lg">
      <v-card-title class="d-flex align-center pa-3 bg-primary">
        <v-icon size="25" color="white" class="mr-2">
        {{ editedItem.id ? 'mdi-pencil' : 'mdi-plus-circle' }}
        </v-icon>
        <span class="text-h5 font-weight-medium white--text">{{ formTitle }}</span>
        <v-spacer></v-spacer>
        <v-btn
        icon="mdi-close"
        variant="text"
        size="small"
        color="white"
        @click="close"
        ></v-btn>
      </v-card-title>

      <v-divider></v-divider>

        <v-card-text>
          <v-form ref="form">
            <v-container>
              <!-- Basic Information Section -->
              <div class="d-flex align-center mb-4">
          <v-icon color="primary" class="mr-2">mdi-information</v-icon>
          <div class="text-h6 font-weight-medium">Basic Information</div>
              </div>
              
              <v-row>
          <!-- Title Field with Icon -->
          <v-col cols="12" sm="6" >
            <v-text-field
              v-model="editedItem.title"
              label="Title"
              :rules="[rules.required]"
              hint="A descriptive title for your room"
              persistent-hint
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-tag"
              class="rounded-lg"
            ></v-text-field>
          </v-col>

          <!-- Price Field  -->
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="editedItem.price"
              label="Monthly Rent"
              type="number"
              prefix="₱"
              :rules="[rules.required, rules.positive]"
              hint="Monthly rent amount"
              persistent-hint
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-cash"
              class="rounded-lg"
            ></v-text-field>
          </v-col>

          <!-- Description Field -->
          <v-col cols="12">
            <v-textarea
              v-model="editedItem.description"
              label="Description"
              :rules="[rules.required]"
              hint="Detailed description of the room"
              persistent-hint
              rows="3"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-text"
              class="rounded-lg"
              auto-grow
            ></v-textarea>
          </v-col>

          <!-- Capacity Field -->
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="editedItem.capacity"
              label="Capacity"
              type="number"
              min="1"
              hint="Number of tenants that can occupy"
              persistent-hint
              :rules="[rules.required, rules.positive]"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-account-group"
              class="rounded-lg"
            ></v-text-field>
          </v-col>

          <!-- Location Field -->
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="editedItem.location"
              label="Location"
              :rules="[rules.required]"
              hint="Location of the room"
              persistent-hint
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-map-marker"
              class="rounded-lg"
            ></v-text-field>
          </v-col>

          <!-- Living Space Type Field -->
          <v-col cols="12" sm="6">
            <v-select
              v-model="editedItem.living_space_type"
              :items="livingSpaceTypes"
              label="Living Space Type"
              :rules="[rules.required]"
              hint="Type of living space"
              persistent-hint
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-home"
              class="rounded-lg"
            ></v-select>
          </v-col>

          <!-- Map Section -->
          <v-col cols="12">
            <v-card class="pa-4 rounded-lg" variant="outlined">
              <div class="d-flex align-center mb-3">
                <v-icon color="primary" class="mr-2">mdi-map-marker</v-icon>
                <div class="text-subtitle-1 font-weight-medium">Pin Location</div>
              </div>
              <div class="text-caption mb-4 text-grey-darken-1">
                Click on the map to set the exact location of your room
              </div>
              <leaflet-map
                :marker-lat-lng="markerPosition"
                :popup-content="editedItem.title || 'New Room'"
                @marker-click="handleMarkerClick"
                ref="mapRef"
                class="rounded-lg"
                style="height: 300px; z-index: 1;"
              />
            </v-card>
          </v-col>
              </v-row>

                <!-- Amenities Section -->
                <div class="d-flex align-center mb-4 mt-5">
                <v-icon color="primary" class="mr-2">mdi-star-box-multiple</v-icon>
                <div class="text-h6 font-weight-medium">Amenities</div>
                </div>
                <v-row>
                <v-col cols="12">
                  <v-combobox
                  v-model="editedItem.amenities"
                  :items="commonAmenities"
                  label="Available Amenities"
                  multiple
                  chips
                  closable-chips
                  variant="outlined"
                  density="comfortable"
                  :rules="[rules.required]"
                  hint="Select from common amenities or type new ones"
                  persistent-hint
                  prepend-inner-icon="mdi-plus-box-multiple"
                  class="rounded-lg"
                  >
                  <template v-slot:chip="{ props, item }">
                    <v-chip
                    v-bind="props"
                    color="primary"
                    variant="flat"
                    :prepend-icon="commonAmenities.includes(item.title) ? 'mdi-check' : 'mdi-plus'"
                    >
                    {{ item.title }}
                    </v-chip>
                  </template>
                  </v-combobox>
                </v-col>
                </v-row>

                <!-- Images Section -->
                <div class="d-flex align-center mb-4 mt-6">
                <v-icon color="primary" class="mr-2">mdi-image-multiple</v-icon>
                <div class="text-h6 font-weight-medium">Room Images</div>
                </div>
                <v-row>
                <v-col cols="12">
                  <v-file-input
                  v-model="roomImages"
                  accept="image/*"
                  label="Upload Room Images"
                  :rules="[editedItem.id ? undefined : rules.images]"
                  hint="Supports multiple images (JPG, PNG up to 5MB each)"
                  persistent-hint
                  show-size
                  multiple
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-camera"
                  class="rounded-lg"
                  truncate-length="25"
                  :loading="loading"
                  >
                  <template v-slot:selection="{ fileNames }">
                    <v-chip
                    v-for="fileName in fileNames"
                    :key="fileName"
                    size="small"
                    color="primary"
                    variant="flat"
                    class="me-2"
                    prepend-icon="mdi-file-image"
                    >
                    {{ fileName }}
                    </v-chip>
                  </template>
                  </v-file-input>
                </v-col>

                <!-- Current Images Gallery -->
                <v-col cols="12" v-if="editedItem.image_urls && editedItem.image_urls.length > 0">
                  <v-card variant="outlined" class="pa-4 rounded-lg">
                  <div class="text-subtitle-1 font-weight-medium mb-3">Current Images</div>
                  <v-row>
                    <v-col
                    v-for="(url, index) in parseImageUrls(editedItem.image_urls)"
                    :key="index"
                    cols="12"
                    sm="6"
                    md="4"
                    >
                    <v-hover v-slot="{ isHovering, props }">
                      <v-card
                      v-bind="props"
                      :elevation="isHovering ? 4 : 0"
                      class="transition-fast-in-fast-out rounded-lg"
                      >
                      <v-img
                        :src="url"
                        height="200"
                        cover
                        class="rounded-lg"
                        :gradient="isHovering ? 'rgba(0,0,0,.4), rgba(0,0,0,.4)' : ''"
                      >
                        <template v-slot:placeholder>
                        <v-row class="fill-height ma-0" align-items ="center" justify="center">
                          <v-progress-circular indeterminate color="primary"></v-progress-circular>
                        </v-row>
                        </template>
                      </v-img>
                      </v-card>
                    </v-hover>
                    </v-col>
                  </v-row>
                  </v-card>
                </v-col>
                </v-row>
              </v-container>
              </v-form>
            </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="elevated" @click="close" class="mb-3"> Cancel </v-btn>
          <v-btn
            color="success"
            variant="elevated"
            @click="save"
            :loading="loading"
            :disabled="loading"
            class="mb-3 mr-3"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Rooms Table -->
    <v-card class="rooms-table-card rounded-lg overflow-hidden">
      <!-- Search Section -->
      <v-card-title class="search-section pa-6 bg-grey-lighten-4">
      <v-row align-items ="center" no-gutters>
        <v-col cols="12" sm="5">
        <div class="d-flex align-center">
          <v-icon size="24" color="primary" class="mr-2">mdi-format-list-bulleted</v-icon>
          <span class="text-h6 font-weight-medium">Living Spaces</span>
        </div>
        </v-col>
        <v-col cols="12" sm="6">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Search by title, location, or type..."
          variant="outlined"
          density="comfortable"
          hide-details
          class="search-field rounded-pill"
          bg-color="white"
          clearable
        ></v-text-field>
        </v-col>
      </v-row>
      </v-card-title>

      <v-data-table
      :headers="headers"
      :items="rooms"
      :search="search"
      hover
      class="elevation-0"
      :loading="loading"
      loading-text="Loading rooms..."
      >
      <!-- Image Column -->
      <template v-slot:item.image_urls="{ item }">
        <v-hover v-slot="{ isHovering, props }">
        <v-card
          v-bind="props"
          :elevation="isHovering ? 8 : 2"
          class="ma-2 transition-fast-in-fast-out overflow-hidden"
        >
          <v-img
          :src="parseImageUrls(item.image_urls)?.[0]"
          height="120"
          width="180"
          cover
          class="rounded-lg"
          :class="{ 'img-hover': isHovering }"
          >
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </v-row>
          </template>
          <div v-if="isHovering" class="image-overlay d-flex align-center justify-center">
            <v-btn
            icon="mdi-image-multiple"
            variant="text"
            color="white"
            size="small"
            ></v-btn>
          </div>
          </v-img>
        </v-card>
        </v-hover>
      </template>

      <!-- Price Column -->
      <template v-slot:item.price="{ item }">
        <div class="d-flex align-center">
        <v-icon color="success" size="small" class="mr-1">mdi-currency-php</v-icon>
        <span class="text-success font-weight-bold">
          {{ Number(item.price).toLocaleString() }}
        </span>
        </div>
      </template>

      <!-- Amenities Column -->
      <template v-slot:item.amenities="{ item }">
        <div class="d-flex flex-wrap gap-1">
        <v-chip
          v-for="(amenity, index) in item.amenities.slice(0, 2)"
          :key="index"
          size="x-small"
          variant="flat"
          color="primary"
          class="ma-1"
        >
          {{ amenity }}
        </v-chip>
        <v-chip
          v-if="item.amenities.length > 2"
          size="x-small"
          variant="outlined"
          color="grey"
          class="ma-1"
        >
          +{{ item.amenities.length - 2 }} more
        </v-chip>
        </div>
      </template>

      <!-- Availability Column -->
      <template v-slot:item.availability="{ item }">
        <v-chip
        :color="item.availability ? 'success' : 'error'"
        :text="item.availability ? 'Available' : 'Occupied'"
        size="small"
        variant="flat"
        class="font-weight-medium"
        :prepend-icon="item.availability ? 'mdi-check-circle' : 'mdi-close-circle'"
        ></v-chip>
      </template>

      <!-- Actions Column -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex gap-2">
        <v-btn
          variant="flat"
          size="small"
          color="primary"
          @click="editItem(item)"
          class="action-btn"
          rounded="pill"
        >
          <v-icon>mdi-pencil</v-icon>
          <v-tooltip activator="parent" location="top">Edit Room</v-tooltip>
        </v-btn>

        <v-btn
          variant="flat" 
          size="small"
          :color="item.availability ? 'error' : 'success'"
          @click="toggleAvailability(item)"
          class="action-btn"
          rounded="pill"
        >
          <v-icon>{{ item.availability ? 'mdi-close' : 'mdi-check' }}</v-icon>
          <v-tooltip activator="parent" location="top">
          {{ item.availability ? 'Mark as Occupied' : 'Mark as Available' }}
          </v-tooltip>
        </v-btn>

        <v-btn
          variant="flat"
          size="small"
          color="error"
          @click="deleteItem(item)"
          class="action-btn"
          rounded="pill"
        >
          <v-icon>mdi-delete</v-icon>
          <v-tooltip activator="parent" location="top">Delete Room</v-tooltip>
        </v-btn>
        </div>
      </template>
      </v-data-table>
      </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/utils/axios'
import LeafletMap from '@/components/LeafletMap.vue'

const form = ref(null)
const dialog = ref(false)
const loading = ref(false)
const rooms = ref([])
const roomImages = ref(null)
const search = ref('')
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')
const mapRef = ref(null)

const markerPosition = ref(null)

const livingSpaceTypes = ['Boarding House', 'Apartment', 'House', 'Dormitory', 'Condo Unit']

const editedItem = ref({
  id: null,
  title: '',
  description: '',
  price: 0,
  capacity: 1,
  location: '',
  living_space_type: '',
  amenities: [],
  image_urls: null,
  availability: true,
  latitude: null,
  longitude: null,
})

const formTitle = computed(() => (editedItem.value.id ? 'Edit Room' : 'Add Living Space'))

const availableRooms = computed(() => rooms.value.filter((room) => room.availability).length)
const averagePrice = computed(() => {
  if (rooms.value.length === 0) return 0
  const total = rooms.value.reduce((sum, room) => sum + room.price, 0)
  return Math.round(total / rooms.value.length)
})

const commonAmenities = [
  'WiFi',
  'Air Conditioning',
  'Heating',
  'Kitchen',
  'Laundry',
  'Parking',
  'TV',
  'Private Bathroom',
  'Study Desk',
  'Closet',
  'CCTV',
  'Fire Exits',
  'Common CR',
  'Appliances',
  'Receiving Area',
]

const rules = {
  required: (v) => !!v || 'Field is required',
  positive: (v) => v > 0 || 'Must be greater than 0',
  integer: (v) => Number.isInteger(Number(v)) || 'Must be a whole number',
  amenities: (v) => (v && v.length > 0) || 'At least one amenity is required',
  images: (files) => !files || files.length > 0 || 'At least one image is required',
}

const parseImageUrls = (urls) => {
  if (!urls) return []
  try {
    return typeof urls === 'string' ? JSON.parse(urls) : urls
  } catch (error) {
    console.error('Error parsing image URLs:', error)
    return []
  }
}

const headers = [
  {
    title: 'Images',
    key: 'image_urls',
    sortable: false,
    align: 'center',
  },
  { title: 'Title', key: 'title' },
  { title: 'Description', key: 'description' },
  { title: 'Price', key: 'price' },
  { title: 'Capacity', key: 'capacity' },
  { title: 'Location', key: 'location' },
  { title: 'Living Space Type', key: 'living_space_type' },
  { title: 'Amenities', key: 'amenities' },
  { title: 'Availability', key: 'availability' },
  { title: 'Actions', key: 'actions', sortable: false },
]

onMounted(async () => {
  await fetchRooms()
})

const fetchRooms = async () => {
  try {
    const response = await axios.get('/landlord/rooms')
    rooms.value = response.data
  } catch (error) {
    console.error('Error fetching rooms:', error)
    snackbarText.value = error.response?.data?.error || 'Error fetching rooms'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const handleMarkerClick = (event) => {
  if (mapRef.value) {
    const { lat, lng } = event.latlng
    markerPosition.value = [lat, lng]
    editedItem.value.latitude = lat
    editedItem.value.longitude = lng
  }
}

const editItem = (item) => {
  editedItem.value = { ...item }
  markerPosition.value = item.latitude && item.longitude ? [item.latitude, item.longitude] : null
  dialog.value = true
}

const close = () => {
  dialog.value = false
  roomImages.value = null
  markerPosition.value = null
  editedItem.value = {
    id: null,
    title: '',
    description: '',
    price: 0,
    capacity: 1,
    location: '',
    living_space_type: '',
    amenities: [],
    image_urls: null,
    availability: true,
    latitude: null,
    longitude: null,
  }
}

const save = async () => {
  const { valid } = await form.value.validate()
  if (!valid) {
    snackbarText.value = 'Please fill in all required fields correctly'
    snackbarColor.value = 'error'
    snackbar.value = true
    return
  }

  loading.value = true

  try {
    const formData = new FormData()
    formData.append('title', editedItem.value.title)
    formData.append('description', editedItem.value.description)
    formData.append('price', editedItem.value.price)
    formData.append('capacity', editedItem.value.capacity)
    formData.append('location', editedItem.value.location)
    formData.append('living_space_type', editedItem.value.living_space_type)
    formData.append('amenities', JSON.stringify(editedItem.value.amenities))

    if (editedItem.value.latitude && editedItem.value.longitude) {
      formData.append('latitude', editedItem.value.latitude)
      formData.append('longitude', editedItem.value.longitude)
    }

    // Handle multiple images
    if (roomImages.value) {
      for (const file of roomImages.value) {
        formData.append('images', file)
      }
    }

    if (editedItem.value.id) {
      await axios.put(`/landlord/rooms/${editedItem.value.id}`, formData)
      snackbarText.value = 'Room updated successfully'
    } else {
      await axios.post('/landlord/rooms', formData)
      snackbarText.value = 'Room added successfully'
    }

    snackbarColor.value = 'success'
    snackbar.value = true
    await fetchRooms()
    close()
  } catch (error) {
    console.error('Error saving room:', error)
    snackbarText.value = error.response?.data?.error || 'Error saving room'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}

const toggleAvailability = async (item) => {
  try {
    loading.value = true
    const formData = new FormData()
    formData.append('title', item.title)
    formData.append('description', item.description)
    formData.append('price', item.price)
    formData.append('capacity', item.capacity)
    formData.append('location', item.location)
    formData.append('living_space_type', item.living_space_type)
    formData.append('amenities', JSON.stringify(item.amenities))
    formData.append('availability', !item.availability)

    await axios.put(`/landlord/rooms/${item.id}`, formData)
    item.availability = !item.availability

    snackbarText.value = `Room marked as ${item.availability ? 'available' : 'occupied'}`
    snackbarColor.value = 'success'
    snackbar.value = true
    await fetchRooms()
  } catch (error) {
    console.error('Error updating room availability:', error.response || error)
    snackbarText.value = error.response?.data?.error || 'Error updating room availability'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}

const deleteItem = async (item) => {
  const confirmed = window.confirm('Are you sure you want to delete this room?')
  if (!confirmed) return

  try {
    await axios.delete(`/landlord/rooms/${item.id}`)
    snackbarText.value = 'Room deleted successfully'
    snackbarColor.value = 'success'
    snackbar.value = true
    await fetchRooms()
  } catch (error) {
    console.error('Error deleting room:', error)
    snackbarText.value = error.response?.data?.error || 'Error deleting room'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>

export default { name: "LandlordDashboard", components: { LeafletMap } }
<style scoped>
.rooms-table-card {
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.search-field {
  transition: all 0.3s ease;
}

.search-field:hover {
  transform: translateY(-1px);
}

.img-hover {
  transform: scale(1.05);
  transition: transform 0.3s ease;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  transition: opacity 0.3s ease;
}

.action-btn {
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
}
</style>

export default { name: "LandlordDashboard", components: { LeafletMap } }
