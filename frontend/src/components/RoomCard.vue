<template>
  <div class="elevation-7" variant="outlined">
    <v-card class="room-card h-100" elevation="3" variant="elevated">
      <!-- Card Header -->
      <v-card-item class="pa-4 header-gradient">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center" style="max-width: 60%">
            <v-avatar color="success" class="me-3" size="36">
              <v-icon size="24" color="white">mdi-home</v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-1 font-weight-bold text-truncate">{{ room.title }}</div>
            </div>
          </div>
          <v-chip
            :color="getMatchColor(match_score)"
            size="small"
            label
            elevation="2"
            class="match-score-chip font-weight-medium"
            variant="elevated"
          >
            <v-icon start :icon="getMatchIcon(match_score)" size="18" class="me-1"></v-icon>
            <span>{{ Math.round(match_score) }}% Match</span>
          </v-chip>
        </div>
      </v-card-item>

      <!-- Card Content -->
      <div class="clickable flex-grow-1" @click="dialog = true">
        <div class="position-relative">
          <v-img
            :src="parseImageUrls(room.image_urls)?.[0] || '/placeholder-room.jpg'"
            height="220"
            cover
            class="bg-grey-lighten-2 image-hover-effect"
          >
          <template v-slot:placeholder>
          <v-row class="fill-height ma-0" align-items="center" justify="center">
            <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
          </v-row>
        </template>
          </v-img>
            
          <div class="d-flex justify-end pa-2">
            <v-chip
              class="rank-chip font-weight-medium"
              :color="getMatchColor(match_score)"
              size="x-large"
              variant="elevated"
              elevation="3"
              label
            >
              #{{ index + 1 }}
            </v-chip>
          </div>
        </div>

        <!-- <v-card-text> -->
           <div class="d-flex align-center mb-2 px-1">
            <div class="text-h5 white--text font-weight-bold px-3">₱{{ formatPrice(room.price) }}</div>
            <div class="text-subtitle-2 white--text ms-1">/month/day</div>
          </div> 

            <div class="d-flex align-center mb-3 px-3"> 
              <v-icon size="22" color="primary" class="me-2">mdi-map-marker</v-icon>
              <span class="text-body-1 text-truncate">{{ room.location }}</span>
              <v-spacer></v-spacer>
              <v-chip
                v-if="room.distance_from_smcc !== null"
                size="x-small"
                color="primary"
                variant="outlined"
                class="ml-2"
              >
                <v-icon size="x-small" start>mdi-map-marker-distance</v-icon>
                {{ formatDistance(room.distance_from_smcc) }} km
              </v-chip>
              <v-btn
                v-if="room.latitude && room.longitude"
                icon="mdi-map-marker"
                size="x-small"
                color="primary"
                variant="text"
                class="ml-2"
                @click.stop="$emit('show-on-map')"
                title="Show on map"
              ></v-btn>
            </div> 

            <!-- Highlighted Amenities -->
            <div v-if="highlight_amenities && highlight_amenities.length > 0" class="px-3 mb-3">
              <v-chip-group>
                <v-chip
                  v-for="amenity in highlight_amenities"
                  :key="amenity"
                  size="small"
                  color="deep-purple"
                  variant="elevated"
                  class="font-weight-medium"
                >
                  <v-icon start size="x-small">mdi-star-plus</v-icon>
                  {{ amenity }}
                </v-chip>
              </v-chip-group>
              <div class="text-caption text-deep-purple mt-1">
                <v-icon size="x-small" color="deep-purple">mdi-information</v-icon>
                Additional valuable amenities
              </div>
            </div>

          <!-- Location Map Preview -->
          <!-- <div v-if="room.latitude && room.longitude" class="mb-2">
            <div class="text-caption mb-1">Debug: Lat: {{ room.latitude }}, Long: {{ room.longitude }}</div>
            <div style="height: 200px">
              <leaflet-map
                :marker-lat-lng="[room.latitude, room.longitude]"
                :popup-content="room.title"
              />
            </div>
          </div> -->

          <!-- <div class="d-flex align-center mb-2">
            <v-icon size="25" class="me-2">mdi-account-group</v-icon>
            <span class="text-body-2"
              >{{ room.capacity }} tenant{{ room.capacity > 1 ? 's' : '' }}</span
            >
          </div> -->

          <!-- <div class="d-flex align-center mb-2">
            <v-icon size="25" class="me-2">mdi-account</v-icon>
            <span class="text-body-2"
              >Contact: {{ room.landlord?.contact_number || 'Not available' }}</span
            >
          </div> -->

          <!-- <div class="d-flex align-center mb-2">
            <v-icon size="25" class="me-2">mdi-email</v-icon>
            <span class="text-body-2">{{ room.landlord?.email || 'Email not available' }}</span>
          </div> -->

          <!-- Description -->
          <!-- <div class="text-body-2 description-box mb-4">
        <v-tooltip location="bottom" max-width="300">
          <template v-slot:activator="{ props }">
            <div v-bind="props" class="text-truncate-2">
              <v-icon size="20" color="grey-darken-1" class="me-1">mdi-text</v-icon>
              {{ room.description }}
            </div>
          </template>
          <span>{{ room.description }}</span>
        </v-tooltip>
      </div> -->

          <!-- Amenities -->
          <!-- <v-chip-group class="mb-3" shows-arrows="always">
            <template v-if="match_details?.amenities?.matched?.length">
              <v-chip
                v-for="amenity in match_details.amenities.matched"
                :key="amenity"
                size="small"
                color="success"
                variant="elevated"
                class="text-caption"
                elevation="10"
              >
                <v-icon start size="x-small">mdi-check</v-icon>
                {{ amenity }}
              </v-chip>
            </template>
            <template v-if="match_details?.amenities?.missing?.length">
              <v-chip
                v-for="amenity in match_details.amenities.missing"
                :key="amenity"
                size="small"
                color="error"
                variant="outlined"
                class="text-caption"
              >
                <v-icon start size="x-small">mdi-close</v-icon>
                {{ amenity }}
              </v-chip>
            </template>
          </v-chip-group> -->

          <!-- <v-divider class="mb-3"></v-divider> -->

          <!-- Match Score Details Dropdown -->
            <v-expansion-panels class="mb-4" @click.stop>
            <v-expansion-panel>
              <v-expansion-panel-title>
              <div class="d-flex align-center justify-space-between w-100">
                <div class="d-flex align-center">
                <v-icon icon="mdi-chart-bar" class="me-2"></v-icon>
                <span class="text-subtitle-1">Match Score Details</span>
                </div>
              </div>
              </v-expansion-panel-title>
              
              <v-expansion-panel-text>
              <v-list class="pa-0">
                <!-- Safety Score -->
                <v-list-item>
                <div class="w-100">
                  <div class="d-flex align-center justify-space-between mb-1">
                  <div class="d-flex align-center">
                    <v-icon size="20" :color="getScoreColor(safetyScore)" class="me-2">mdi-shield-home</v-icon>
                    <span class="text-body-2">Safety Score</span>
                  </div>
                  <v-chip size="x-small" :color="getScoreColor(safetyScore)" label>
                    {{ safetyScore }}/10
                  </v-chip>
                  </div>
                  <v-progress-linear
                  :model-value="safetyScore * 10"
                  :color="getScoreColor(safetyScore)"
                  height="6"
                  rounded
                  ></v-progress-linear>
                </div>
                </v-list-item>

                <!-- Cleanliness Score -->
                <v-list-item>
                <div class="w-100">
                  <div class="d-flex align-center justify-space-between mb-1">
                  <div class="d-flex align-center">
                    <v-icon size="20" :color="getScoreColor(cleanlinessScore)" class="me-2">mdi-broom</v-icon>
                    <span class="text-body-2">Cleanliness Score</span>
                  </div>
                  <v-chip size="x-small" :color="getScoreColor(cleanlinessScore)" label>
                    {{ cleanlinessScore }}/10
                  </v-chip>
                  </div>
                  <v-progress-linear
                  :model-value="cleanlinessScore * 10"
                  :color="getScoreColor(cleanlinessScore)"
                  height="6"
                  rounded
                  ></v-progress-linear>
                </div>
                </v-list-item>

                <!-- Accessibility Score -->
                <v-list-item>
                <div class="w-100">
                  <div class="d-flex align-center justify-space-between mb-1">
                  <div class="d-flex align-center">
                    <v-icon size="20" :color="getScoreColor(accessibilityScore)" class="me-2">mdi-wheelchair-accessibility</v-icon>
                    <span class="text-body-2">Accessibility Score</span>
                  </div>
                  <v-chip size="x-small" :color="getScoreColor(accessibilityScore)" label>
                    {{ accessibilityScore }}/10
                  </v-chip>
                  </div>
                  <v-progress-linear
                  :model-value="accessibilityScore * 10"
                  :color="getScoreColor(accessibilityScore)"
                  height="6"
                  rounded
                  ></v-progress-linear>
                </div>
                </v-list-item>

                <!-- Noise Level -->
                <v-list-item>
                <div class="w-100">
                  <div class="d-flex align-center justify-space-between mb-1">
                  <div class="d-flex align-center">
                    <v-icon size="20" :color="getScoreColor(10 - noiseScore)" class="me-2">mdi-volume-medium</v-icon>
                    <span class="text-body-2">Noise Level</span>
                  </div>
                  <v-chip size="x-small" :color="getScoreColor(10 - noiseScore)" label>
                    {{ noiseScore }}/10
                  </v-chip>
                  </div>
                  <v-progress-linear
                  :model-value="(10 - noiseScore) * 10"
                  :color="getScoreColor(10 - noiseScore)"
                  height="6"
                  rounded
                  ></v-progress-linear>
                </div>
                </v-list-item>
              </v-list>
              </v-expansion-panel-text>
            </v-expansion-panel>
            </v-expansion-panels>

              <!-- Amenity Match -->
              <!-- <v-col cols="12" class="mb-2">
                <div class="d-flex align-center mb-1">
                  <v-icon size="25" :color="getScoreColor(amenityScore / 10)" class="me-1"
                    >mdi-check-circle</v-icon
                  >
                  <span class="text-body-2">Amenity Match</span>
                  <v-spacer></v-spacer>
                  <v-chip size="x-small" :color="getScoreColor(amenityScore / 10)" label>
                    {{ Math.round(amenityScore) }}%
                  </v-chip>
                </div>
                <v-progress-linear
                  :model-value="amenityScore"
                  :color="getScoreColor(amenityScore / 10)"
                  height="8"
                  rounded
                ></v-progress-linear>
              </v-col> -->

              <!-- Location Match -->
              <!-- <v-col cols="12" class="mb-2">
                <div class="d-flex align-center mb-1">
                  <v-icon size="small" :color="getScoreColor(locationScore / 10)" class="me-1">mdi-map-marker-check</v-icon>
                  <span class="text-body-2">Location Match</span>
                  <v-spacer></v-spacer>
                  <v-chip
                    size="x-small"
                    :color="getScoreColor(locationScore / 10)"
                    label
                  >
                    {{ Math.round(locationScore) }}%
                  </v-chip>
                </div>
                <v-progress-linear
                  :model-value="locationScore"
                  :color="getScoreColor(locationScore / 10)"
                  height="8"
                  rounded
                ></v-progress-linear>
              </v-col> -->

              <!-- Price Value -->
              <!-- <v-col cols="12">
                <div class="d-flex align-center mb-1">
                  <v-icon size="25" :color="getScoreColor(priceValueScore / 10)" class="me-1"
                    >mdi-currency-usd</v-icon
                  >
                  <span class="text-body-2">Price Value</span>
                  <v-spacer></v-spacer>
                  <v-chip size="x-small" :color="getScoreColor(priceValueScore / 10)" label>
                    {{ Math.round(priceValueScore) }}%
                  </v-chip>
                </div>
                <v-progress-linear
                  :model-value="priceValueScore"
                  :color="getScoreColor(priceValueScore / 10)"
                  height="8"
                  rounded
                ></v-progress-linear>
              </v-col> -->
            <!-- </v-row>
          </div>
        </v-card-text> -->
      </div>

      <!-- Card Footer -->
      <v-card-item class="bg-grey-lighten-4 mb-2">
        <div class="d-flex align-center justify-space-between">
          <div class="text-subtitle-1">
            Total Distance:
          </div>
          <div class="d-flex align-center">
            <v-chip variant="elevated" color="success"> 
            <v-icon size="small" class="me-1">mdi-map-marker-distance</v-icon>
            <span class="text-body-2">{{ calculateDistance }} km from SMCC</span>
          </v-chip>
          </div>
        </div>
      </v-card-item>

      <!-- Non-clickable rating section -->
      <v-card-text @click.stop>
        <v-divider class="mb-3"></v-divider>
        <div class="d-flex align-center justify-space-between">
          <div class="text-subtitle-1">Tenant Ratings ({{ room.total_ratings || 0 }})</div>
          <rating-dialog
            :room-id="room.id"
            :user-type="user_type"
            :existing-rating="userRating"
            @rating-updated="handleRatingUpdate"
          />
        </div>
        <div v-if="room.total_ratings > 0" class="mt-2">
          <!-- Safety Rating -->
          <div class="d-flex align-center mb-2">
            <v-icon size="22" :color="getScoreColor(room.safety_score)" class="me-1"
              >mdi-shield-home</v-icon
            >
            <span class="text-body-2">Safety:</span>
            <v-rating
              :model-value="room.safety_score"
              color="warning"
              half-increments
              readonly
              density="compact"
              size="small"
              class="ms-2"
            ></v-rating>
            <span class="text-caption ms-2">({{ room.safety_score?.toFixed(1) || 0 }})</span>
          </div>

          <!-- Cleanliness Rating -->
          <div class="d-flex align-center mb-2">
            <v-icon size="22" :color="getScoreColor(room.cleanliness_score)" class="me-1"
              >mdi-broom</v-icon
            >
            <span class="text-body-2">Cleanliness:</span>
            <v-rating
              :model-value="room.cleanliness_score"
              color="warning"
              half-increments
              readonly
              density="compact"
              size="small"
              class="ms-2"
            ></v-rating>
            <span class="text-caption ms-2">({{ room.cleanliness_score?.toFixed(1) || 0 }})</span>
          </div>

          <!-- Accessibility Rating -->
          <div class="d-flex align-center mb-2">
            <v-icon size="22" :color="getScoreColor(room.accessibility_score)" class="me-1"
              >mdi-wheelchair-accessibility</v-icon
            >
            <span class="text-body-2">Accessibility:</span>
            <v-rating
              :model-value="room.accessibility_score"
              color="warning"
              half-increments
              readonly
              density="compact"
              size="small"
              class="ms-2"
            ></v-rating>
            <span class="text-caption ms-2">({{ room.accessibility_score?.toFixed(1) || 0 }})</span>
          </div>

          <!-- Noise Level Rating -->
          <div class="d-flex align-center mb-2">
            <v-icon size="22" :color="getScoreColor(10 - room.noise_level)" class="me-1"
              >mdi-volume-medium</v-icon
            >
            <span class="text-body-2">Noise Level:</span>
            <v-rating
              :model-value="10 - room.noise_level"
              color="warning"
              half-increments
              readonly
              density="compact"
              size="small"
              class="ms-2"
            ></v-rating>
            <span class="text-caption ms-2">({{ room.noise_level?.toFixed(1) || 0 }})</span>
          </div>
        </div>
        <div v-else class="text-body-2 text-grey">No ratings yet</div>
      </v-card-text>
    </v-card>

    <!-- Details Modal -->
    <v-dialog v-model="dialog" max-width="1200">
      <v-card height="90vh" class="d-flex flex-column">
        <!-- Modal Header -->
        <v-card-item class="bg-primary pa-4 elevation-4">
          <div class="d-flex justify-space-between align-center">
            <div class="d-flex align-center">
              <v-icon size="24" class="me-2">mdi-home</v-icon>
              <h2 class="text-h5">{{ room.title }}</h2>
            </div>
            <v-btn icon="mdi-close" variant="text" @click="dialog = false"></v-btn>
          </div>
        </v-card-item>

        <!-- Modal Content -->
        <v-card-text class="pa-0 flex-grow-1 modal-content">
          <v-row no-gutters class="h-100">
            <!-- Image Carousel (60%) -->
            <v-col cols="12" md="7" class="h-100">
              <v-carousel
                v-model="currentSlide"
                show-arrows="hover"
                height="100%"
                hide-delimiter-background
                :continuous="false"
                :touch="true"
                cycle
              >
                <v-carousel-item
                  v-for="(url, index) in parseImageUrls(room.image_urls)"
                  :key="index"
                >
                  <v-img :src="url" height="100%" cover class="bg-grey-lighten-2">
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align-items="center" justify="center">
                        <v-progress-circular
                          indeterminate
                          color="grey-lighten-5"
                        ></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-carousel-item>
              </v-carousel>
            </v-col>

            <!-- Location Map -->
            <v-col cols="12" md="5" class="h-100 details-column">
              <div class="details-content">
                <div v-if="room.latitude && room.longitude" class="mb-5">
                  <div style="height: 300px; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1)">
                    <leaflet-map
                      :marker-lat-lng="[room.latitude, room.longitude]"
                      :popup-content="room.title"
                      :zoom="15"
                      class="rounded-lg overflow-hidden"
                      style="height: 300px"
                    />
                  </div>
                  
                  <!-- Map Details Section -->
                  <div class="map-details mt-3 bg-grey-lighten-4 pa-3 rounded-lg">
                    <div class="d-flex justify-space-between align-center mb-2">
                      <div class="text-subtitle-1 font-weight-medium">Map Details</div>
                      <v-chip
                        size="small"
                        color="primary"
                        variant="elevated"
                        class="font-weight-medium"
                      >
                        <v-icon start size="small">mdi-map-marker-distance</v-icon>
                        {{ calculateDistance }} km
                      </v-chip>
                    </div>
                    
                    <v-divider class="mb-2"></v-divider>
                    
                    <!-- SMCC Coordinates -->
                    <div class="d-flex align-center mb-2">
                      <v-avatar size="25" color="amber" class="me-2">
                        <v-icon size="20" color="white">mdi-school</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-caption text-medium-emphasis">SMCC Location</div>
                        <div class="text-body-5">
                          Lat: {{ SMCC_COORDINATES[0] }}, Long: {{ SMCC_COORDINATES[1] }}
                        </div>
                      </div>
                    </div>
                    
                    <!-- Room Coordinates -->
                    <div class="d-flex align-center">
                      <v-avatar size="25" color="primary" class="me-2">
                        <v-icon size="20" color="white">mdi-home</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-caption text-medium -emphasis">Room Location</div>
                        <div class="text-body-2">
                          Lat: {{ room.latitude }}, Long: {{ room.longitude }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Price Information -->
                <div class="price-section d-flex align-center mb-4 px-1">
                  <div>
                    <div class="text-h4 font-weight-bold primary--text">
                    ₱{{ formatPrice(room.price) }}
                    </div>
                    <div class="text-subtitle-2 text-medium-emphasis">per month</div>
                  </div>
                </div>

                <!-- Location and Capacity -->
                <v-divider class="my-4"></v-divider>
                <div class="rounded-lg py-2 px-2">
                  <div class="d-flex flex-column gap-2">
                    <div class="d-flex align-center">
                      <v-icon size="25" class="me-3">mdi-map-marker</v-icon>
                      <span class="text-body-1">{{ room.location }}</span>
                      <v-spacer></v-spacer>
                      <v-chip
                        v-if="room.distance_from_smcc !== null"
                        size="small"
                        color="primary"
                        variant="outlined"
                        class="ml-2"
                      >
                        <v-icon size="x-small" start>mdi-map-marker-distance</v-icon>
                        {{ formatDistance(room.distance_from_smcc) }} km from SMCC
                      </v-chip>
                      <v-btn
                        v-if="room.latitude && room.longitude"
                        size="small"
                        color="primary"
                        variant="text"
                        class="ml-2"
                        @click="$emit('show-on-map'); dialog = false"
                        prepend-icon="mdi-map-marker"
                      >
                        Show on Map
                      </v-btn>
                    </div>
                    <div class="d-flex align-center mt-2">
                      <v-icon size="25" class="me-3">mdi-account-group</v-icon>
                      <span class="text-body-1"
                        >{{ room.capacity }} tenant{{ room.capacity > 1 ? 's' : '' }}</span
                      >
                    </div>
                  </div>

                  <!-- Description -->
                  <div class="text-body-1 mb-2 mt-2">
                    <v-icon size="25" class="me-3">mdi-text</v-icon>{{ room.description }}
                  </div>
                </div>
                <!-- Amenities -->
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-2">Amenities</h3>
                
                <!-- Highlighted Amenities -->
                <div v-if="highlight_amenities && highlight_amenities.length > 0" class="mb-3">
                  <v-card color="deep-purple-lighten-5" class="pa-3 mb-3">
                    <div class="d-flex align-center mb-2">
                      <v-icon color="deep-purple" class="mr-2">mdi-star-plus</v-icon>
                      <span class="text-subtitle-1 font-weight-medium text-deep-purple">Additional Valuable Amenities</span>
                    </div>
                    <v-chip-group>
                      <v-chip
                        v-for="amenity in highlight_amenities"
                        :key="amenity"
                        size="small"
                        color="deep-purple"
                        variant="elevated"
                        class="font-weight-medium"
                      >
                        {{ amenity }}
                      </v-chip>
                    </v-chip-group>
                    <div class="text-caption mt-2">
                      These valuable amenities weren't in your search criteria but might enhance your living experience.
                    </div>
                  </v-card>
                </div>
                
                <v-chip-group class="mb-4">
                  <v-chip
                    v-for="amenity in parseAmenities(room.amenities)"
                    :key="amenity"
                    size="small"
                    variant="elevated"
                    color="primary"
                    class="text-body-2"
                  >
                    {{ amenity }}
                  </v-chip>
                </v-chip-group>

                <!-- Ratings -->
                <v-divider class="my-3"></v-divider>
                <h3 class="text-h6 mb-3">Property Ratings</h3>
                <v-row dense class="bg-grey-lighten-3 rounded-lg py-3 px-2">
                  <v-col cols="6">
                    <div class="d-flex align-center mb-1">
                      <v-icon size="25" :color="getScoreColor(room.safety_score)" class="me-1"
                        >mdi-shield-home</v-icon
                      >
                      <span class="text-body-2">Safety: {{ room.safety_score }}/10</span>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <div class="d-flex align-center mb-1">
                      <v-icon size="25" :color="getScoreColor(room.cleanliness_score)" class="me-1"
                        >mdi-broom</v-icon
                      >
                      <span class="text-body-2">Cleanliness: {{ room.cleanliness_score }}/10</span>
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <div class="d-flex align-center mb-1">
                      <v-icon
                        size="25"
                        :color="getScoreColor(room.accessibility_score)"
                        class="me-1"
                        >mdi-wheelchair-accessibility</v-icon
                      >
                      <span class="text-body-2"
                        >Accessibility: {{ room.accessibility_score }}/10</span
                      >
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <div class="d-flex align-center mb-1">
                      <v-icon size="25" :color="getScoreColor(10 - room.noise_level)" class="me-1"
                        >mdi-volume-medium</v-icon
                      >
                      <span class="text-body-2">Noise Level: {{ room.noise_level }}/10</span>
                    </div>
                  </v-col>
                </v-row>

                <!-- Contact Information -->
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-2 font-weight-bold">Contact Information</h3>
                <div class="bg-grey-lighten-3 rounded-lg py-3 px-2">
                  <div class="d-flex align-center mb-2">
                    <v-icon size="25" class="me-2">mdi-account</v-icon>
                    <span class="text-body-1">{{
                      room.landlord?.contact_number || 'Not available'
                    }}</span>
                  </div>
                  <div class="d-flex align-center mb-2">
                    <v-icon size="25" class="me-2">mdi-email</v-icon>
                    <span class="text-body-1">{{
                      room.landlord?.email || 'Email not available'
                    }}</span>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import RatingDialog from './RatingDialog.vue'
import LeafletMap from './LeafletMap.vue'
import axios from '@/plugins/axios'

const props = defineProps({
  room: {
    type: Object,
    required: true,
  },
  user_type: {
    type: String,
    default: 'tenant',
  },
  highlight_amenities: {
    type: Array,
    default: () => [],
  },
  index: {
    type: Number,
    default: 0,
  },
})

// Update computed properties to use match_details from the room object
const safetyScore = computed(
  () => props.room.match_details?.safety?.score || props.room.safety_score || 5.0,
)
const cleanlinessScore = computed(
  () => props.room.match_details?.cleanliness?.score || props.room.cleanliness_score || 5.0,
)
const accessibilityScore = computed(
  () => props.room.match_details?.accessibility?.score || props.room.accessibility_score || 5.0,
)
const noiseScore = computed(
  () => props.room.match_details?.noise?.score || props.room.noise_level || 5.0,
)
const amenityScore = computed(() => props.room.match_details?.amenities?.score || 0)
const locationScore = computed(() => props.room.match_details?.location?.score || 0)
const priceValueScore = computed(() => props.room.match_details?.price_value?.score || 0)
const matchedAmenities = computed(() => props.room.match_details?.amenities?.matched || [])
const missingAmenities = computed(() => props.room.match_details?.amenities?.missing || [])

// SMCC coordinates (base point)
const SMCC_COORDINATES = [8.9882671, 125.3404024]

// Calculate distance between room and SMCC
const calculateDistance = computed(() => {
  if (!props.room.latitude || !props.room.longitude) return 'N/A'
  
  // Haversine formula to calculate distance between two points on Earth
  const toRad = (value) => (value * Math.PI) / 180
  const R = 6371 // Earth's radius in km
  
  const lat1 = SMCC_COORDINATES[0]
  const lon1 = SMCC_COORDINATES[1]
  const lat2 = props.room.latitude
  const lon2 = props.room.longitude
  
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * 
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  const distance = R * c
  
  return distance.toFixed(2)
})

const router = useRouter()

const dialog = ref(false)
const currentSlide = ref(0)
const hasRated = ref(false)
const userRating = ref(null)

// Computed properties
const match_score = computed(() => props.room.comprehensive_score || 0)
const match_details = computed(() => props.room.match_details || {
  safety: { score: 0, weight: 0, weighted_score: 0 },
  cleanliness: { score: 0, weight: 0, weighted_score: 0 },
  accessibility: { score: 0, weight: 0, weighted_score: 0 },
  noise: { score: 0, weight: 0, weighted_score: 0 },
  amenities: { score: 0, weight: 0, weighted_score: 0, matched: [], missing: [] },
  location: { score: 0, preferred_location: '', actual_location: '' },
  price_value: { score: 0, preferred_max: 0, actual_price: 0 },
})

const averageRating = computed(() => {
  if (!props.room.avg_safety_rating) return 0
  return (
    (props.room.avg_safety_rating +
      props.room.avg_cleanliness_rating +
      props.room.avg_accessibility_rating +
      (10 - props.room.avg_noise_level_rating)) /
    4
  )
})

const handleRatingUpdate = async (newRating) => {
  userRating.value = newRating
  // Refresh room data to get updated average ratings
  try {
    const response = await axios.get(`/rating/room/${props.room.id}`)
    Object.assign(props.room, response.data.summary)
  } catch (error) {
    console.error('Error refreshing room ratings:', error)
  }
}

onMounted(async () => {
  if (props.user_type === 'tenant') {
    try {
      const response = await axios.get('/rating/user/ratings')
      const ratings = response.data
      userRating.value = ratings.find((r) => r.room_id === props.room.id)
    } catch (error) {
      console.error('Error fetching user ratings:', error)
    }
  }
})

const parseImageUrls = (urls) => {
  if (!urls) return []
  try {
    return typeof urls === 'string' ? JSON.parse(urls) : urls
  } catch (error) {
    console.error('Error parsing image URLs:', error)
    return []
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-PH').format(price)
}

const formatDistance = (distance) => {
  if (distance === null || distance === undefined) return 'Unknown';
  return distance.toFixed(1);
}

const getMatchColor = (score) => {
  if (score >= 90) return 'success'
  if (score >= 85) return 'info'
  if (score >= 75) return 'green-darken-1'
  if (score >= 60) return 'warning'
  return 'grey'
}

const getMatchIcon = (score) => {
  if (score >= 90) return 'mdi-star'
  if (score >= 85) return 'mdi-star-half-full'
  if (score >= 75) return 'mdi-star-outline'
  if (score >= 60) return 'mdi-star-outline'
  return 'mdi-star-off'
}

const getScoreColor = (score) => {
  if (score >= 8) return 'success'
  if (score >= 6) return 'info'
  if (score >= 4) return 'warning'
  return 'error'
}

const parseAmenities = (amenities) => {
  if (!amenities) return []
  if (Array.isArray(amenities)) return amenities
  try {
    return typeof amenities === 'string' ? JSON.parse(amenities) : []
  } catch (error) {
    console.error('Error parsing amenities:', error)
    return []
  }
}

const viewDetails = () => {
  router.push(`/rooms/${props.room.id}`)
}
</script>

<style scoped>
.match-chip {
  position: absolute;
  top: 8px;
  right: 8px;
}

.rank-chip {
  position: absolute;
  top: 8px;
  left: 8px;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.v-card {
  transition: transform 0.2s ease-in-out;
}

.v-card:hover {
  transform: translateY(-4px);
}

/* Add new styles for the modal */
.v-dialog .v-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.v-carousel {
  height: 100%;
  background-color: #000;
}

.v-carousel .v-img {
  object-fit: contain;
}

.clickable {
  cursor: pointer;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.pa-6::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.pa-6 {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.h-100 {
  height: 100%;
}

.modal-content {
  height: calc(90vh - 64px);
  overflow: hidden;
}

.details-column {
  position: relative;
  overflow: hidden;
  height: 100%;
}

.details-content {
  height: 100%;
  overflow-y: auto;
  padding: 22px;
}

/* Show scrollbar */
.details-content::-webkit-scrollbar {
  width: 8px;
}

.details-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.details-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.details-content::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Firefox scrollbar */
.details-content {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}
</style>
