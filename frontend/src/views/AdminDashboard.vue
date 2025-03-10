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
      <v-tabs
        v-model="activeTab"
        bg-color="primary"
        centered
        dark
        class="mb-6 rounded-lg elevation-2"
      >
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
          <v-badge
            v-if="pendingRooms.length > 0"
            :content="pendingRooms.length"
            color="error"
            offset-x="10"
            offset-y="-10"
          ></v-badge>
        </v-tab>
        <v-tab value="approved-landlords" @click="fetchApprovedLandlords">
          <v-icon start>mdi-account-check</v-icon>
          Approved Landlords
          <v-badge
            v-if="approvedLandlordsCount > 0"
            :content="approvedLandlordsCount"
            color="success"
            offset-x="10"
            offset-y="-10"
          ></v-badge>
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- Dashboard Tab -->
        <v-window-item value="dashboard">
          <!-- Stats Cards -->
          <v-row class="mb-8">
            <v-col cols="12" md="4">
              <v-card
                hover
                elevation="4"
                rounded="xl"
                class="stat-card gradient-primary"
                theme="dark"
              >
                <v-card-text class="py-6 px-6">
                  <div class="d-flex align-center">
                    <div class="stat-icon-wrapper mr-6">
                      <v-icon size="48" color="white">mdi-account-group</v-icon>
                    </div>
                    <div>
                      <div class="text-h3 font-weight-bold mb-1">
                        {{ dashboardData.tenant_count || 0 }}
                      </div>
                      <div class="text-subtitle-2 text-white text-opacity-75">
                        Active Tenants
                        <v-icon size="16" class="ml-1">mdi-trending-up</v-icon>
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="4">
              <v-card
                hover
                elevation="4"
                rounded="xl"
                class="stat-card gradient-secondary"
                theme="dark"
              >
                <v-card-text class="py-6 px-6">
                  <div class="d-flex align-center">
                    <div class="stat-icon-wrapper mr-6">
                      <v-icon size="48" color="white">mdi-home-account</v-icon>
                    </div>
                    <div>
                      <div class="text-h3 font-weight-bold mb-1">
                        {{ dashboardData.landlord_count || 0 }}
                      </div>
                      <div class="text-subtitle-2 text-white text-opacity-75">
                        Total of Landlords
                        <v-icon size="16" class="ml-1">mdi-shield-check</v-icon>
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="4">
              <v-card hover elevation="4" rounded="xl" class="stat-card gradient-info" theme="dark">
                <v-card-text class="py-6 px-6">
                  <div class="d-flex align-center">
                    <div class="stat-icon-wrapper mr-6">
                      <v-icon size="48" color="white">mdi-door</v-icon>
                    </div>
                    <div>
                      <div class="text-h3 font-weight-bold mb-1">
                        {{ dashboardData.room_count || 0 }}
                      </div>
                      <div class="text-subtitle-2 text-white text-opacity-75">
                        Total Spaces
                        <v-icon size="16" class="ml-1">mdi-chart-line</v-icon>
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Recent Users -->
          <v-row>
            <v-col cols="12">
              <v-card elevation="2" rounded="xl" class="recent-users-card">
                <v-card-title
                  class="py-6 px-8 bg-success text-white d-flex justify-space-between align-center"
                >
                  <div class="d-flex align-center">
                    <v-icon size="32" color="white" class="mr-3">mdi-clock-outline</v-icon>
                    <div>
                      <span class="text-h5">Recent Users</span>
                      <div class="text-caption text-medium-emphasis mt-1">
                        Latest registered users in the system
                      </div>
                    </div>
                  </div>
                  <v-btn
                    color="light"
                    variant="text"
                    prepend-icon="mdi-refresh"
                    @click="fetchDashboardData"
                  >
                    Refresh
                  </v-btn>
                </v-card-title>

                <v-card-text class="pa-4">
                  <v-table hover class="rounded elevation-1">
                    <thead>
                      <tr>
                        <th class="text-subtitle-2 font-weight-bold text-primary pa-4">ID</th>
                        <th class="text-subtitle-2 font-weight-bold text-primary">Email</th>
                        <th class="text-subtitle-2 font-weight-bold text-primary">Type</th>
                        <th class="text-subtitle-2 font-weight-bold text-primary">Created At</th>
                        <!-- <th class="text-subtitle-2 font-weight-bold text-primary">Status</th> -->
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="user in dashboardData.recent_users"
                        :key="user.id"
                        class="table-row"
                      >
                        <td class="text-subtitle-2 font-weight-medium pa-4">#{{ user.id }}</td>
                        <td class="text-subtitle-2">
                          <div class="d-flex align-center">
                            <v-avatar size="32" color="grey-lighten-4" class="mr-2">
                              <v-icon size="16" color="grey">mdi-account</v-icon>
                            </v-avatar>
                            {{ user.email }}
                          </div>
                        </td>
                        <td>
                          <v-chip
                            :color="user.user_type === 'tenant' ? 'primary' : 'secondary'"
                            size="small"
                            variant="flat"
                            class="font-weight-medium text-caption"
                          >
                            <v-icon size="14" start>
                              {{ user.user_type === 'tenant' ? 'mdi-account' : 'mdi-home-account' }}
                            </v-icon>
                            {{ user.user_type }}
                          </v-chip>
                        </td>
                        <td class="text-subtitle-2 text-medium-emphasis">
                          {{ formatDate(user.created_at) }}
                        </td>
                        <!-- <td>
              <v-chip
                size="small"
                :color="user.is_active ? 'success' : 'warning'"
                variant="flat"
                class="font-weight-medium text-caption"
              >
                {{ user.is_active ? 'Active' : 'Pending' }}
              </v-chip>
             </td>  -->
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
              <v-card elevation="2" rounded="xl" class="user-management-card">
                <v-card-title class="py-6 px-8 bg-success d-flex align-center">
                  <div class="d-flex align-center">
                    <v-icon size="32" color="white" class="mr-3">mdi-account-group</v-icon>
                    <div>
                      <span class="text-h5">User Management</span>
                      <div class="text-caption text-medium-emphasis mt-1">
                        Manage and monitor system users
                      </div>
                    </div>
                  </div>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    prepend-inner-icon="mdi-magnify"
                    label="Search users..."
                    single-line
                    hide-details
                    density="comfortable"
                    variant="outlined"
                    class="search-field mx-4"
                    bg-color="white"
                    clearable
                  ></v-text-field>
                  <v-btn
                    color="white"
                    variant="text"
                    prepend-icon="mdi-refresh"
                    @click="fetchUsers"
                  >
                    Refresh
                  </v-btn>
                </v-card-title>

                <v-card-text class="pa-6">
                  <v-data-table
                    :headers="headers"
                    :items="users"
                    :search="search"
                    :loading="loading"
                    hover
                    class="elevation-1 rounded-lg user-table"
                  >
                    <template v-slot:loader>
                      <v-sheet class="pa-8 d-flex justify-center align-center">
                        <v-progress-circular indeterminate color="primary"></v-progress-circular>
                      </v-sheet>
                    </template>

                    <template v-slot:item.user_type="{ item }">
                      <v-chip
                        :color="item.user_type === 'tenant' ? 'primary' : 'secondary'"
                        size="small"
                        variant="flat"
                        class="font-weight-medium text-capitalize"
                      >
                        <v-icon start size="16">
                          {{ item.user_type === 'tenant' ? 'mdi-account' : 'mdi-home-account' }}
                        </v-icon>
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
                        <v-icon start size="16">
                          {{ item.is_admin ? 'mdi-shield-check' : 'mdi-shield-off' }}
                        </v-icon>
                        {{ item.is_admin ? 'Admin' : 'User' }}
                      </v-chip>
                    </template>

                    <template v-slot:item.is_landlord_approved="{ item }">
                      <v-chip
                        :color="item.is_landlord_approved ? 'success' : 'warning'"
                        size="small"
                        variant="flat"
                        class="font-weight-medium"
                      >
                        <v-icon start size="16">
                          {{ item.is_landlord_approved ? 'mdi-check-circle' : 'mdi-clock-outline' }}
                        </v-icon>
                        {{ item.is_landlord_approved ? 'Approved' : 'Pending' }}
                      </v-chip>
                    </template>

                    <template v-slot:item.created_at="{ item }">
                      <div class="d-flex align-center">
                        <v-icon size="16" color="grey" class="mr-2">mdi-calendar</v-icon>
                        {{ formatDate(item.created_at) }}
                      </div>
                    </template>

                    <template v-slot:item.actions="{ item }">
                      <div class="d-flex">
                        <v-tooltip text="Edit User" location="top">
                          <template v-slot:activator="{ props }">
                            <v-btn
                              icon
                              size="32"
                              color="primary"
                              variant="flat"
                              class="mr-2"
                              v-bind="props"
                              @click="openEditDialog(item)"
                            >
                              <v-icon size="18">mdi-pencil</v-icon>
                            </v-btn>
                          </template>
                        </v-tooltip>

                        <v-tooltip text="Delete User" location="top">
                          <template v-slot:activator="{ props }">
                            <v-btn
                              icon
                              size="32"
                              color="error"
                              variant="flat"
                              v-bind="props"
                              @click="deleteUser(item)"
                            >
                              <v-icon size="18">mdi-delete</v-icon>
                            </v-btn>
                          </template>
                        </v-tooltip>
                      </div>
                    </template>

                    <template v-slot:no-data>
                      <div class="d-flex flex-column align-center py-8">
                        <v-icon size="64" color="grey-lighten-1" class="mb-4">
                          mdi-account-off
                        </v-icon>
                        <div class="text-h6 text-grey-darken-1">No Users Found</div>
                        <div class="text-body-2 text-grey">Try adjusting your search terms</div>
                      </div>
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
              <v-card elevation="3" rounded="xl" class="pending-rooms-card">
                <!-- Enhanced Header Section -->
                <v-card-title class="py-7 px-8 bg-success d-flex align-center">
                  <div class="d-flex align-center">
                    <div class="primary-gradient rounded-circle pa-3 mr-4">
                      <v-icon size="32" color="white">mdi-home-clock</v-icon>
                    </div>
                    <div>
                      <span class="text-h5 font-weight-bold">Pending Room Approvals</span>
                      <div class="text-caption text-medium-emphasis mt-1">
                        Review and manage submitted room listings
                      </div>
                    </div>
                    <v-chip
                      v-if="pendingRooms.length > 0"
                      color="warning"
                      class="ml-4"
                      size="small"
                      elevation="2"
                    >
                      {{ pendingRooms.length }} pending
                    </v-chip>
                  </div>
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
                    style="max-width: 300px"
                  ></v-text-field>
                  <v-btn
                    color="light"
                    prepend-icon="mdi-refresh"
                    @click="fetchPendingRooms"
                    variant="tonal"
                    class="ml-2"
                  >
                    Refresh
                  </v-btn>
                </v-card-title>

                <v-card-text class="pa-6">
                  <!-- Loading State -->
                  <div
                    v-if="loadingPendingRooms"
                    class="d-flex flex-column justify-center align-center py-12"
                  >
                    <v-progress-circular
                      indeterminate
                      color="primary"
                      size="64"
                      class="mb-4"
                    ></v-progress-circular>
                    <span class="text-body-1 text-medium-emphasis">Loading pending rooms...</span>
                  </div>

                  <!-- Empty State -->
                  <div v-else-if="pendingRooms.length === 0" class="empty-state pa-12 text-center">
                    <v-icon size="72" color="primary" class="mb-4 opacity-75"
                      >mdi-check-circle-outline</v-icon
                    >
                    <div class="text-h5 font-weight-bold mb-2 text-primary">All Caught Up!</div>
                    <div class="text-body-1 text-medium-emphasis">
                      There are no pending rooms to review at this time.
                    </div>
                  </div>

                  <!-- No Results State -->
                  <div v-else-if="filteredRooms.length === 0" class="empty-state pa-12 text-center">
                    <v-icon size="72" color="grey-lighten-1" class="mb-4">mdi-text-search</v-icon>
                    <div class="text-h5 font-weight-bold mb-2">No Results Found</div>
                    <div class="text-body-1 text-medium-emphasis mb-4">
                      Try adjusting your search criteria
                    </div>
                    <v-btn
                      variant="outlined"
                      color="primary"
                      @click="roomSearch = ''"
                      prepend-icon="mdi-restart"
                    >
                      Reset Search
                    </v-btn>
                  </div>

                  <!-- Room List -->
                  <div v-else>
                    <v-expansion-panels class="room-panels">
                      <v-expansion-panel
                        v-for="room in paginatedRooms"
                        :key="room.id"
                        class="mb-4 room-panel"
                        rounded="lg"
                      >
                        <v-expansion-panel-title class="py-4">
                          <div class="d-flex align-center">
                            <v-avatar size="56" class="mr-4 elevation-2" rounded>
                              <v-img
                                :src="room.image_urls?.[0] || '/default-room.jpg'"
                                cover
                                :gradient="'to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 100%'"
                              ></v-img>
                            </v-avatar>
                            <div>
                              <div class="text-h6 font-weight-bold mb-1">{{ room.title }}</div>
                              <div class="d-flex align-center text-body-2 text-medium-emphasis">
                                <v-icon size="16" class="mr-1">mdi-map-marker</v-icon>
                                {{ room.location }}
                                <v-divider vertical class="mx-2"></v-divider>
                                <v-icon size="16" class="mr-1">mdi-currency-php</v-icon>
                                {{ room.price.toLocaleString() }}
                              </div>
                            </div>
                          </div>
                        </v-expansion-panel-title>

                        <!-- Enhanced Room Details Section -->
                        <v-expansion-panel-text class="pa-6">
                          <v-row>
                            <v-col cols="12" md="6">
                              <v-card elevation="2" rounded="lg" class="overflow-hidden">
                                <v-carousel
                                  height="400"
                                  hide-delimiters
                                  show-arrows="hover"
                                  cycle
                                  interval="5000"
                                  v-if="room.image_urls?.length"
                                >
                                  <v-carousel-item
                                    v-for="(image, i) in room.image_urls"
                                    :key="i"
                                    :src="image"
                                    cover
                                  >
                                    <template v-slot:placeholder>
                                      <v-row
                                        class="fill-height"
                                        align-items="center"
                                        justify="center"
                                      >
                                        <v-progress-circular
                                          indeterminate
                                          color="primary"
                                        ></v-progress-circular>
                                      </v-row>
                                    </template>
                                  </v-carousel-item>
                                </v-carousel>
                              </v-card>
                            </v-col>

                            <v-col cols="12" md="6">
                              <!-- Room Details Card -->
                              <v-card elevation="2" rounded="lg" class="mb-4">
                                <v-card-title class="py-4 px-6 bg-primary text-white">
                                  <v-icon start>mdi-information</v-icon>
                                  Room Details
                                </v-card-title>
                                <v-card-text class="pa-4">
                                  <v-list density="comfortable">
                                    <v-list-item
                                      v-for="(detail, index) in [
                                        {
                                          icon: 'mdi-currency-php',
                                          label: 'Price',
                                          value: `₱${room.price.toLocaleString()}`,
                                        },
                                        {
                                          icon: 'mdi-account-group',
                                          label: 'Capacity',
                                          value: `${room.capacity} person(s)`,
                                        },
                                        {
                                          icon: 'mdi-map-marker',
                                          label: 'Location',
                                          value: room.location,
                                        },
                                        {
                                          icon: 'mdi-home-variant',
                                          label: 'Type',
                                          value: room.living_space_type,
                                        },
                                      ]"
                                      :key="index"
                                    >
                                      <template v-slot:prepend>
                                        <v-icon
                                          :color="index % 2 ? 'secondary' : 'primary'"
                                          class="mr-2"
                                          >{{ detail.icon }}</v-icon
                                        >
                                      </template>
                                      <v-list-item-title>
                                        <span class="font-weight-medium">{{ detail.label }}:</span>
                                        {{ detail.value }}
                                      </v-list-item-title>
                                    </v-list-item>
                                  </v-list>
                                </v-card-text>
                              </v-card>

                              <!-- Landlord Info Card -->
                              <v-card elevation="2" rounded="lg" class="mb-4">
                                <v-card-title class="py-4 px-6 bg-secondary text-white">
                                  <v-icon start>mdi-account</v-icon>
                                  Landlord Information
                                </v-card-title>
                                <v-card-text class="pa-4">
                                  <v-list density="comfortable">
                                    <v-list-item>
                                      <template v-slot:prepend>
                                        <v-icon color="primary">mdi-email</v-icon>
                                      </template>
                                      <v-list-item-title>{{
                                        room.landlord.email
                                      }}</v-list-item-title>
                                    </v-list-item>
                                    <v-list-item v-if="room.landlord.contact_number">
                                      <template v-slot:prepend>
                                        <v-icon color="primary">mdi-phone</v-icon>
                                      </template>
                                      <v-list-item-title>{{
                                        room.landlord.contact_number
                                      }}</v-list-item-title>
                                    </v-list-item>
                                  </v-list>
                                </v-card-text>
                              </v-card>

                              <!-- Amenities Section -->
                              <v-card elevation="2" rounded="lg">
                                <v-card-title class="py-4 px-6 bg-info text-white">
                                  <v-icon start>mdi-star</v-icon>
                                  Amenities
                                </v-card-title>
                                <v-card-text class="pa-4">
                                  <v-chip-group>
                                    <v-chip
                                      v-for="amenity in room.amenities"
                                      :key="amenity"
                                      color="info"
                                      variant="outlined"
                                      size="small"
                                      class="font-weight-medium"
                                    >
                                      <v-icon start size="16">mdi-check-circle</v-icon>
                                      {{ amenity }}
                                    </v-chip>
                                  </v-chip-group>
                                </v-card-text>
                              </v-card>
                            </v-col>
                          </v-row>

                          <!-- Admin Actions Section -->
                          <v-card elevation="2" rounded="lg" class="mt-6">
                            <v-card-title class="py-4 px-6 bg-grey-lighten-3">
                              <v-icon start>mdi-clipboard-text</v-icon>
                              Admin Review
                            </v-card-title>
                            <v-card-text class="pa-4">
                              <v-textarea
                                v-model="room.adminNotes"
                                label="Admin Notes"
                                hint="Required for rejection. Please provide detailed feedback."
                                persistent-hint
                                rows="3"
                                variant="outlined"
                                class="mb-4"
                              ></v-textarea>

                              <div class="d-flex justify-end gap-4">
                                <v-btn
                                  color="error"
                                  variant="outlined"
                                  prepend-icon="mdi-close"
                                  @click="rejectRoom(room)"
                                  :disabled="!room.adminNotes"
                                  size="large"
                                >
                                  Reject Listing
                                </v-btn>
                                <v-btn
                                  color="success"
                                  variant="elevated"
                                  prepend-icon="mdi-check"
                                  @click="approveRoom(room)"
                                  size="large"
                                >
                                  Approve Listing
                                </v-btn>
                              </div>
                            </v-card-text>
                          </v-card>
                        </v-expansion-panel-text>
                      </v-expansion-panel>
                    </v-expansion-panels>

                    <!-- Enhanced Pagination -->
                    <div class="d-flex flex-column align-center mt-8">
                      <div class="text-body-2 text-medium-emphasis mb-4">
                        Showing {{ paginationStart }} - {{ paginationEnd }} of
                        {{ filteredRooms.length }} rooms
                        <span v-if="roomSearch && filteredRooms.length !== pendingRooms.length">
                          (filtered from {{ pendingRooms.length }} total)
                        </span>
                      </div>
                      <v-pagination
                        v-model="currentPage"
                        :length="totalPages"
                        :total-visible="7"
                        rounded="circle"
                        elevation="2"
                        active-color="primary"
                      ></v-pagination>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>

        <!-- Approved Landlords Tab -->
        <v-window-item value="approved-landlords">
          <v-row>
            <v-col cols="12">
              <v-card elevation="3" rounded="xl">
                <!-- Header Section -->
                <v-card-title class="py-7 px-8 bg-success d-flex align-center text-white">
                  <div class="d-flex align-center">
                    <div class="primary-gradient rounded-circle pa-3 mr-4">
                      <v-icon size="32" color="white">mdi-account-check</v-icon>
                    </div>
                    <div>
                      <span class="text-h5 font-weight-bold">Approved Landlords</span>
                      <div class="text-caption mt-1">
                        View and manage approved landlord accounts
                      </div>
                    </div>
                    <v-chip
                      v-if="approvedLandlordsCount > 0"
                      color="primary"
                      class="ml-4"
                      size="small"
                      variant="elevated"
                    >
                      {{ approvedLandlordsCount }} approved
                    </v-chip>
                  </div>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="landlordSearch"
                    prepend-inner-icon="mdi-magnify"
                    label="Search landlords..."
                    single-line
                    hide-details
                    density="comfortable"
                    variant="outlined"
                    class="search-field mx-4"
                    bg-color="white"
                    clearable
                    style="max-width: 300px"
                  ></v-text-field>
                  <v-btn
                    color="light"
                    prepend-icon="mdi-refresh"
                    @click="fetchApprovedLandlords"
                    variant="tonal"
                    class="ml-2"
                  >
                    Refresh
                  </v-btn>
                </v-card-title>

                <v-card-text class="pa-6">
                  <!-- Loading State -->
                  <div
                    v-if="loadingLandlords"
                    class="d-flex flex-column justify-center align-center py-12"
                  >
                    <v-progress-circular
                      indeterminate
                      color="primary"
                      size="64"
                      class="mb-4"
                    ></v-progress-circular>
                    <span class="text-body-1 text-medium-emphasis">Loading landlords...</span>
                  </div>

                  <!-- Empty State -->
                  <div
                    v-else-if="approvedLandlordsCount === 0"
                    class="empty-state pa-12 text-center"
                  >
                    <v-icon size="72" color="grey-lighten-1" class="mb-4">mdi-account-off</v-icon>
                    <div class="text-h5 font-weight-bold mb-2">No Approved Landlords</div>
                    <div class="text-body-1 text-medium-emphasis">
                      There are no approved landlords in the system yet.
                    </div>
                  </div>

                  <!-- Landlord List -->
                  <v-table v-else hover class="elevation-1 rounded-lg">
                    <thead>
                      <tr>
                        <th class="text-subtitle-2 font-weight-bold text-primary pa-4">ID</th>
                        <th class="text-subtitle-2 font-weight-bold text-primary">Email</th>
                        <th class="text-subtitle-2 font-weight-bold text-primary">Status</th>
                        <th class="text-subtitle-2 font-weight-bold text-primary">Joined Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="landlord in paginatedLandlords" :key="landlord.id">
                        <td class="text-subtitle-2 font-weight-medium pa-4">#{{ landlord.id }}</td>
                        <td>
                          <div class="d-flex align-center">
                            <v-avatar size="32" color="primary" class="mr-2">
                              <v-icon size="16" color="white">mdi-account</v-icon>
                            </v-avatar>
                            {{ landlord.email }}
                          </div>
                        </td>
                        <!-- <td class="text-subtitle-2">
                          <v-chip
                            size="small"
                            color="info"
                            variant="flat"
                            v-if="landlord.contact_number"
                          >
                            <v-icon start size="14">mdi-phone</v-icon>
                            {{ landlord.contact_number }}
                          </v-chip>
                          <span v-else class="text-medium-emphasis">Not provided</span>
                        </td> -->
                        <td>
                          <v-chip size="small" :color="landlord.details.statusColor" variant="flat">
                            {{ landlord.details.status }}
                          </v-chip>
                        </td>
                        <td class="text-subtitle-2">{{ landlord.details.createdAt }}</td>
                      </tr>
                    </tbody>
                  </v-table>

                  <!-- Pagination -->
                  <div class="d-flex justify-center mt-6">
                    <v-pagination
                      v-model="landlordPage"
                      :length="Math.ceil(filteredLandlords.length / itemsPerPage)"
                      :total-visible="7"
                      rounded="circle"
                    ></v-pagination>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>
    </v-container>

    <!-- Edit User Dialog -->
    <v-dialog v-model="editDialog" max-width="600px" persistent>
      <v-card rounded="xl" elevation="8">
        <!-- Header -->
        <v-card-title class="py-7 px-8 bg-primary text-white d-flex align-center">
          <v-icon size="32" class="mr-4">mdi-account-edit</v-icon>
          <div>
            <div class="text-h5 font-weight-bold">Edit User Profile</div>
            <div class="text-caption mt-1 text-white text-opacity-75">
              Modify user details and permissions
            </div>
          </div>
        </v-card-title>

        <!-- Content -->
        <v-card-text class="pa-8" >
          <v-form>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.email"
                  label="Email Address"
                  disabled
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-email"
                  bg-color="grey-lighten-4"
                  class="mb-2"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-select
                  v-model="editedItem.user_type"
                  :items="[
                    { title: 'Tenant', value: 'tenant', icon: 'mdi-account' },
                    { title: 'Landlord', value: 'landlord', icon: 'mdi-home-account' },
                  ]"
                  label="User Type"
                  variant="outlined"
                  density="comfortable"
                  item-title="title"
                  item-value="value"
                  class="mb-2"
                >
                  <template v-slot:prepend-inner>
                    <v-icon :color="editedItem.user_type === 'landlord' ? 'secondary' : 'primary'">
                      {{ editedItem.user_type === 'landlord' ? 'mdi-home-account' : 'mdi-account' }}
                    </v-icon>
                  </template>
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template v-slot:prepend>
                        <v-icon :color="item.raw.value === 'landlord' ? 'secondary' : 'primary'">
                          {{ item.raw.icon }}
                        </v-icon>
                      </template>
                      <v-list-item-title>{{ item.raw.title }}</v-list-item-title>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12">
                <v-card variant="outlined" rounded="lg" class="pa-4">
                  <div class="d-flex justify-space-between align-center">
                    <div>
                      <div class="text-subtitle-1 font-weight-bold mb-1">
                        Landlord Approval Status
                      </div>
                      <div class="text-caption text-medium-emphasis">
                        {{
                          editedItem.is_landlord_approved
                            ? 'User is approved as a landlord'
                            : 'User is pending approval'
                        }}
                      </div>
                    </div>
                    <v-switch
                      v-model="editedItem.is_landlord_approved"
                      color="success"
                      hide-details
                      inset
                      :true-icon="'mdi-check-circle'"
                      :false-icon="'mdi-clock-outline'"
                    ></v-switch>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <!-- Actions -->
        <v-divider></v-divider>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn
            color="grey-darken-1"
            variant="text"
            @click="editDialog = false"
            prepend-icon="mdi-close"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            variant="elevated"
            class="ml-4"
            @click="saveUser"
            prepend-icon="mdi-content-save"
            :loading="loading"
          >
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
/* Card Styles */
.stat-card {
  transition: all 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-6px);
}

/* Search Field */
.search-field {
  max-width: 300px;
}

/* Icon Wrappers */
.stat-icon-wrapper {
  padding: 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
}

/* Gradient Backgrounds */
.gradient-primary {
  background: linear-gradient(135deg, #1867c0 0%, #5cbbf6 100%);
}
.gradient-secondary {
  background: linear-gradient(135deg, #80ffc0 0%, #00ff40 100%);
}
.gradient-info {
  background: linear-gradient(135deg, #0288d1 0%, #4fc3f7 100%);
}

/* Table Styles */
.table-row:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}

/* Room Panel Styles */
.room-panel {
  margin-bottom: 16px;
  transition: all 0.2s ease;
}
.room-panel:hover {
  transform: translateX(4px);
}

/* Admin Dashboard Header */
.admin-dashboard .v-card-title {
  border-radius: 16px 16px 0 0;
}

/* User Management Table */
.user-table {
  border-radius: 8px;
  overflow: hidden;
}

/* Empty State Styles */
.empty-state {
  background-color: rgba(var(--v-theme-surface), 0.8);
  border-radius: 16px;
  transition: all 0.3s ease;
}
.empty-state:hover {
  background-color: rgba(var(--v-theme-surface), 1);
}

/* Pagination Controls */
.v-pagination {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 4px;
  border-radius: 50px;
  background: white;
}

/* Animation Effects */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card,
.room-panel {
  animation: fadeIn 0.5s ease forwards;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Image Gallery */
.v-carousel {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Chip Styles */
.v-chip {
  transition: all 0.2s ease;
}
.v-chip:hover {
  transform: scale(1.05);
}

/* Card Hover Effects */
.v-card {
  transition: all 0.3s ease;
}
.v-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Dialog Animations */
.v-dialog-transition-enter-active {
  transition: all 0.3s ease-out;
}
.v-dialog-transition-leave-active {
  transition: all 0.2s ease-in;
}

/* Button Hover Effects */
.v-btn {
  transition: all 0.2s ease;
}
.v-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  recent_users: [],
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
  { title: 'Actions', key: 'actions', sortable: false },
]

const editDialog = ref(false)
const editedItem = ref({
  id: null,
  email: '',
  user_type: '',
  is_landlord_approved: false,
  is_admin: false,
  contact_number: ''
})

// Notification
const snackbar = ref(false)
const snackbarColor = ref('')
const snackbarText = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10
const totalPages = computed(() => Math.ceil(filteredRooms.value.length / itemsPerPage))

// Computed property for filtered rooms
const filteredRooms = computed(() => {
  if (!roomSearch.value) return pendingRooms.value

  const searchTerm = roomSearch.value.toLowerCase()
  return pendingRooms.value.filter(
    (room) =>
      room.title.toLowerCase().includes(searchTerm) ||
      room.description.toLowerCase().includes(searchTerm) ||
      room.location.toLowerCase().includes(searchTerm) ||
      room.living_space_type.toLowerCase().includes(searchTerm),
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
    minute: '2-digit',
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
    pendingRooms.value = response.data.map((room) => ({
      ...room,
      adminNotes: room.admin_notes || '',
      // Ensure amenities are properly parsed
      amenities: parseAmenities(room.amenities),
      // Ensure image URLs are properly parsed
      image_urls: parseImageUrls(room.image_urls),
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
      admin_notes: room.adminNotes,
    })

    // Remove the room from the pending list
    pendingRooms.value = pendingRooms.value.filter((r) => r.id !== room.id)

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
    snackbarText.value =
      'Failed to reject room: ' + (error.response?.data?.error || 'Unknown error')
  }
}

// Approve a room
const approveRoom = async (room) => {
  try {
    await axios.put(`/admin/rooms/${room.id}/approve`)

    // Remove the room from the pending list
    pendingRooms.value = pendingRooms.value.filter((r) => r.id !== room.id)

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
    snackbarText.value =
      'Failed to approve room: ' + (error.response?.data?.error || 'Unknown error')
  }
}

// Approved landlords data and functions
const approvedLandlords = ref([])
const loadingLandlords = ref(false)
const landlordSearch = ref('')
const landlordPage = ref(1)

// Computed property for paginated landlords 
const paginatedLandlords = computed(() => {
  const startIndex = (landlordPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return filteredLandlords.value.slice(startIndex, endIndex)
})

// Display landlord details
const displayLandlordDetails = (landlord) => {
  return {
    email: landlord.email,
    // Get contact number from the profile object if it exists
    contact_number: landlord.profile?.contact_number || landlord.contact_number || 'Not provided',
    createdAt: formatDate(landlord.created_at), 
    status: landlord.is_landlord_approved ? 'Approved' : 'Pending',
    statusColor: landlord.is_landlord_approved ? 'success' : 'warning',
  }
}

// Fetch approved landlords with detailed information
const fetchApprovedLandlords = async () => {
  loadingLandlords.value = true
  try {
    const response = await axios.get('/admin/users', {
      params: {
        user_type: 'landlord',
        is_landlord_approved: true,
        include_profile: true // Request to include profile data
      },
    })
    approvedLandlords.value = response.data
      .filter((user) => user.user_type === 'landlord' && user.is_landlord_approved)
      .map((landlord) => ({
        ...landlord,
        details: displayLandlordDetails(landlord),
        // Ensure contact number is accessible from both places
        contact_number: landlord.profile?.contact_number || landlord.contact_number
      }))
  } catch (error) {
    console.error('Error fetching approved landlords:', error)
    snackbar.value = true
    snackbarColor.value = 'error'
    snackbarText.value = 'Failed to fetch landlords: ' + (error.response?.data?.message || 'Network error')
  } finally {
    loadingLandlords.value = false
  }
}

// Computed property for filtered landlords
const filteredLandlords = computed(() => {
  if (!landlordSearch.value) return approvedLandlords.value

  const searchTerm = landlordSearch.value.toLowerCase()
  return approvedLandlords.value.filter((landlord) => 
    landlord.email.toLowerCase().includes(searchTerm) ||
    (landlord.contact_number && landlord.contact_number.includes(searchTerm)) ||
    landlord.details.createdAt.toLowerCase().includes(searchTerm)
  )
})

// Store badge count
const approvedLandlordsCount = computed(() => approvedLandlords.value.length)


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
      is_landlord_approved: editedItem.value.is_landlord_approved,
    })

    // Update local data
    const index = users.value.findIndex((user) => user.id === editedItem.value.id)
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
    snackbarText.value =
      'Failed to update user: ' + (error.response?.data?.error || 'Unknown error')
  }
}

// Delete user
const deleteUser = async (item) => {
  if (
    !confirm(`Are you sure you want to delete user ${item.email}? This action cannot be undone.`)
  ) {
    return
  }

  try {
    await axios.delete(`/admin/users/${item.id}`)

    // Remove user from local data
    users.value = users.value.filter((user) => user.id !== item.id)

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
    snackbarText.value =
      'Failed to delete user: ' + (error.response?.data?.error || 'Unknown error')
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
