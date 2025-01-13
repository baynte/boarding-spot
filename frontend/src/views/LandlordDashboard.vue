<template>
  <div>
    <h1 class="text-h4 mb-4">Landlord Dashboard</h1>

    <!-- Add Room Dialog -->
    <v-dialog v-model="dialog" max-width="800px">
      <template v-slot:activator="{ props }">
        <v-btn
          color="primary"
          v-bind="props"
          class="mb-4"
        >
          Add New Room
        </v-btn>
      </template>

      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form">
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.title"
                    label="Title"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.price"
                    label="Price"
                    type="number"
                    prefix="$"
                    :rules="[rules.required, rules.positive]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.size"
                    label="Size (sq ft)"
                    type="number"
                    :rules="[rules.required, rules.positive]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="editedItem.location"
                    label="Location"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    v-model="editedItem.description"
                    label="Description"
                    :rules="[rules.required]"
                  ></v-textarea>
                </v-col>
                <v-col cols="12">
                  <v-combobox
                    v-model="editedItem.amenities"
                    :items="commonAmenities"
                    label="Amenities"
                    multiple
                    chips
                    :rules="[rules.required]"
                  ></v-combobox>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.safety_score"
                    label="Safety Score"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                  ></v-slider>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.cleanliness_score"
                    label="Cleanliness Score"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                  ></v-slider>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.accessibility_score"
                    label="Accessibility Score"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                  ></v-slider>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-slider
                    v-model="editedItem.noise_level"
                    label="Noise Level"
                    min="1"
                    max="10"
                    step="0.5"
                    thumb-label
                  ></v-slider>
                </v-col>
                <v-col cols="12">
                  <v-file-input
                    v-model="roomImage"
                    accept="image/*"
                    label="Room Image"
                    prepend-icon="mdi-camera"
                    :rules="[editedItem.id ? undefined : rules.required]"
                  ></v-file-input>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="close">Cancel</v-btn>
          <v-btn color="success" variant="text" @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Rooms Table -->
    <v-data-table
      :headers="headers"
      :items="rooms"
      class="elevation-1"
    >
      <template v-slot:item.image_url="{ item }">
        <v-img
          :src="item.image_url"
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
        ${{ item.price }}
      </template>

      <template v-slot:item.availability="{ item }">
        <v-chip
          :color="item.availability ? 'success' : 'error'"
          :text="item.availability ? 'Available' : 'Occupied'"
        ></v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
          size="small"
          class="me-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          size="small"
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const dialog = ref(false)
const form = ref(null)
const rooms = ref([])
const roomImage = ref(null)
const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const headers = [
  { title: 'Image', key: 'image_url', sortable: false },
  { title: 'Title', key: 'title' },
  { title: 'Price', key: 'price' },
  { title: 'Location', key: 'location' },
  { title: 'Size', key: 'size' },
  { title: 'Status', key: 'availability' },
  { title: 'Actions', key: 'actions', sortable: false }
]

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

const defaultItem = {
  title: '',
  description: '',
  price: 0,
  size: 0,
  location: '',
  amenities: [],
  safety_score: 5,
  cleanliness_score: 5,
  accessibility_score: 5,
  noise_level: 5,
  availability: true
}

const editedItem = ref({ ...defaultItem })
const editedIndex = ref(-1)

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New Room' : 'Edit Room'
})

const rules = {
  required: v => !!v || 'Field is required',
  positive: v => v > 0 || 'Must be greater than 0'
}

onMounted(async () => {
  await fetchRooms()
})

const fetchRooms = async () => {
  try {
    const response = await axios.get('http://localhost:5000/landlord/rooms')
    rooms.value = response.data
  } catch (error) {
    snackbarText.value = 'Error fetching rooms'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const editItem = (item) => {
  editedIndex.value = rooms.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const deleteItem = async (item) => {
  if (!confirm('Are you sure you want to delete this room?')) return
  
  try {
    await axios.delete(`http://localhost:5000/landlord/rooms/${item.id}`)
    const index = rooms.value.indexOf(item)
    rooms.value.splice(index, 1)
    snackbarText.value = 'Room deleted successfully'
    snackbarColor.value = 'success'
    snackbar.value = true
  } catch (error) {
    snackbarText.value = 'Error deleting room'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

const close = () => {
  dialog.value = false
  editedIndex.value = -1
  editedItem.value = Object.assign({}, defaultItem)
  roomImage.value = null
  form.value?.reset()
}

const save = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  const formData = new FormData()
  Object.keys(editedItem.value).forEach(key => {
    if (key === 'amenities') {
      formData.append(key, JSON.stringify(editedItem.value[key]))
    } else {
      formData.append(key, editedItem.value[key])
    }
  })

  if (roomImage.value) {
    formData.append('image', roomImage.value)
  }

  try {
    if (editedIndex.value > -1) {
      await axios.put(`http://localhost:5000/landlord/rooms/${editedItem.value.id}`, formData)
      Object.assign(rooms.value[editedIndex.value], editedItem.value)
      snackbarText.value = 'Room updated successfully'
    } else {
      const response = await axios.post('http://localhost:5000/landlord/rooms', formData)
      rooms.value.push(response.data)
      snackbarText.value = 'Room created successfully'
    }
    snackbarColor.value = 'success'
    close()
  } catch (error) {
    snackbarText.value = 'Error saving room'
    snackbarColor.value = 'error'
  }
  snackbar.value = true
}
</script> 