<template>
  <div>
    <div class="d-flex align-center justify-space-between mb-4">
      <h1 class="text-h4">Landlord Dashboard</h1>
      <v-btn
        color="primary"
        variant="text"
        prepend-icon="mdi-account-cog"
        to="/landlord/profile"
      >
        Profile Settings
      </v-btn>
    </div>

    <!-- Quick Stats -->
    <v-row class="mb-6">
      <v-col cols="12" sm="4">
        <v-card>
          <v-card-text class="text-center">
            <div class="text-h4 mb-2">{{ rooms.length }}</div>
            <div class="text-subtitle-1">Total Rooms</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card>
          <v-card-text class="text-center">
            <div class="text-h4 mb-2">{{ availableRooms }}</div>
            <div class="text-subtitle-1">Available Rooms</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card>
          <v-card-text class="text-center">
            <div class="text-h4 mb-2">₱{{ averagePrice }}</div>
            <div class="text-subtitle-1">Average Price</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add Room Button -->
    <div class="d-flex justify-end mb-4">
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="dialog = true"
      >
        Add New Room
      </v-btn>
    </div>

    <!-- Add/Edit Room Dialog -->
    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form">
            <v-container>
              <!-- Basic Information -->
              <div class="text-h6 mb-2">Basic Information</div>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.title"
                    label="Title"
                    :rules="[rules.required]"
                    hint="A descriptive title for your room"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.price"
                    label="Monthly Rent"
                    type="number"
                    prefix="₱"
                    :rules="[rules.required, rules.positive]"
                    hint="Monthly rent amount"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    v-model="editedItem.description"
                    label="Description"
                    :rules="[rules.required]"
                    hint="Detailed description of the room"
                    persistent-hint
                    rows="3"
                  ></v-textarea>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.location"
                    label="Location"
                    :rules="[rules.required]"
                    hint="Room location or neighborhood"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="editedItem.capacity"
                    label="Capacity"
                    type="number"
                    :rules="[rules.required, rules.positive, rules.integer]"
                    hint="Maximum number of occupants"
                    persistent-hint
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Amenities -->
              <div class="text-h6 mb-2">Amenities</div>
              <v-row>
                <v-col cols="12">
                  <v-combobox
                    v-model="editedItem.amenities"
                    :items="commonAmenities"
                    label="Available Amenities"
                    multiple
                    chips
                    :rules="[rules.required]"
                    hint="Select or type amenities available in the room"
                    persistent-hint
                  ></v-combobox>
                </v-col>
              </v-row>

              <!-- Ratings -->
              <div class="text-h6 mb-2">Property Ratings</div>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.safety_score"
                    label="Safety Score"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                    hint="Rate the safety of the neighborhood (1-10)"
                    persistent-hint
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="editedItem.safety_score"
                        type="number"
                        style="width: 70px"
                        density="compact"
                        hide-details
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.cleanliness_score"
                    label="Cleanliness Score"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                    hint="Rate the cleanliness of the property (1-10)"
                    persistent-hint
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="editedItem.cleanliness_score"
                        type="number"
                        style="width: 70px"
                        density="compact"
                        hide-details
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.accessibility_score"
                    label="Accessibility Score"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                    hint="Rate the accessibility to public transport/amenities (1-10)"
                    persistent-hint
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="editedItem.accessibility_score"
                        type="number"
                        style="width: 70px"
                        density="compact"
                        hide-details
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.noise_level"
                    label="Noise Level"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                    hint="Rate the noise level (1=quiet, 10=noisy)"
                    persistent-hint
                  >
                    <template v-slot:append>
                      <v-text-field
                        v-model="editedItem.noise_level"
                        type="number"
                        style="width: 70px"
                        density="compact"
                        hide-details
                      ></v-text-field>
                    </template>
                  </v-slider>
                </v-col>
              </v-row>

              <!-- Image Upload -->
              <div class="text-h6 mb-2">Room Images</div>
              <v-row>
                <v-col cols="12">
                  <v-file-input
                    v-model="roomImages"
                    accept="image/*"
                    label="Room Images"
                    prepend-icon="mdi-camera"
                    :rules="[editedItem.id ? undefined : rules.images]"
                    hint="Upload clear images of the room (you can select multiple)"
                    persistent-hint
                    show-size
                    multiple
                  >
                    <template v-slot:selection="{ fileNames }">
                      <template v-for="fileName in fileNames" :key="fileName">
                        <v-chip
                          size="small"
                          label
                          color="primary"
                          class="me-2"
                        >
                          {{ fileName }}
                        </v-chip>
                      </template>
                    </template>
                  </v-file-input>
                </v-col>
                <v-col cols="12" v-if="editedItem.image_urls && editedItem.image_urls.length > 0">
                  <div class="text-subtitle-2 mb-2">Current Images:</div>
                  <v-row>
                    <v-col v-for="(url, index) in parseImageUrls(editedItem.image_urls)" :key="index" cols="12" sm="6" md="4">
                      <v-img
                        :src="url"
                        max-height="200"
                        contain
                        class="bg-grey-lighten-2"
                      ></v-img>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            variant="text"
            @click="close"
          >
            Cancel
          </v-btn>
          <v-btn
            color="success"
            variant="text"
            @click="save"
            :loading="loading"
            :disabled="loading"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Rooms Table -->
    <v-card>
      <v-card-title>
        <v-text-field
          v-model="search"
          prepend-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
          density="compact"
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="rooms"
        :search="search"
        class="elevation-1"
      >
        <template v-slot:item.image_urls="{ item }">
          <v-img
            :src="parseImageUrls(item.image_urls)?.[0]"
            height="100"
            width="150"
            cover
            class="bg-grey-lighten-2"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
              </v-row>
            </template>
          </v-img>
        </template>

        <template v-slot:item.price="{ item }">
          ₱{{ item.price }}
        </template>

        <template v-slot:item.availability="{ item }">
          <v-chip
            :color="item.availability ? 'success' : 'error'"
            :text="item.availability ? 'Available' : 'Occupied'"
            size="small"
          ></v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-tooltip text="Edit Room">
            <template v-slot:activator="{ props }">
              <v-btn
                icon="mdi-pencil"
                size="small"
                color="primary"
                v-bind="props"
                @click="editItem(item)"
                class="mr-2"
              ></v-btn>
            </template>
          </v-tooltip>
          <v-tooltip text="Toggle Availability">
            <template v-slot:activator="{ props }">
              <v-btn
                :icon="item.availability ? 'mdi-close' : 'mdi-check'"
                size="small"
                :color="item.availability ? 'error' : 'success'"
                v-bind="props"
                @click="toggleAvailability(item)"
                class="mr-2"
              ></v-btn>
            </template>
          </v-tooltip>
          <v-tooltip text="Delete Room">
            <template v-slot:activator="{ props }">
              <v-btn
                icon="mdi-delete"
                size="small"
                color="error"
                v-bind="props"
                @click="deleteItem(item)"
              ></v-btn>
            </template>
          </v-tooltip>
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

const form = ref(null)
const dialog = ref(false)
const loading = ref(false)
const rooms = ref([])
const roomImages = ref(null)
const search = ref('')
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const editedItem = ref({
  id: null,
  title: '',
  description: '',
  price: 0,
  capacity: 1,
  location: '',
  amenities: [],
  safety_score: 5,
  cleanliness_score: 5,
  accessibility_score: 5,
  noise_level: 5,
  image_urls: null,
  availability: true
})

const formTitle = computed(() => editedItem.value.id ? 'Edit Room' : 'Add Room')

const availableRooms = computed(() => rooms.value.filter(room => room.availability).length)
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
  'Closet'
]

const rules = {
  required: v => !!v || 'Field is required',
  positive: v => v > 0 || 'Must be greater than 0',
  integer: v => Number.isInteger(Number(v)) || 'Must be a whole number',
  amenities: v => v && v.length > 0 || 'At least one amenity is required',
  images: files => !files || files.length > 0 || 'At least one image is required'
}

const parseImageUrls = (urls) => {
  if (!urls) return [];
  try {
    return typeof urls === 'string' ? JSON.parse(urls) : urls;
  } catch (error) {
    console.error('Error parsing image URLs:', error);
    return [];
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
  { title: 'Price', key: 'price' },
  { title: 'Location', key: 'location' },
  { title: 'Availability', key: 'availability' },
  { title: 'Actions', key: 'actions', sortable: false }
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
    formData.append('amenities', JSON.stringify(editedItem.value.amenities))
    formData.append('safety_score', editedItem.value.safety_score)
    formData.append('cleanliness_score', editedItem.value.cleanliness_score)
    formData.append('accessibility_score', editedItem.value.accessibility_score)
    formData.append('noise_level', editedItem.value.noise_level)
    formData.append('availability', editedItem.value.availability)

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

const close = () => {
  dialog.value = false
  roomImages.value = null
  editedItem.value = {
    id: null,
    title: '',
    description: '',
    price: 0,
    capacity: 1,
    location: '',
    amenities: [],
    safety_score: 5,
    cleanliness_score: 5,
    accessibility_score: 5,
    noise_level: 5,
    image_urls: null,
    availability: true
  }
}

const editItem = (item) => {
  editedItem.value = { ...item }
  dialog.value = true
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
    formData.append('amenities', JSON.stringify(item.amenities))
    formData.append('safety_score', item.safety_score)
    formData.append('cleanliness_score', item.cleanliness_score)
    formData.append('accessibility_score', item.accessibility_score)
    formData.append('noise_level', item.noise_level)
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
