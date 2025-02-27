<template>
  <div class="map-container">
    <l-map
      v-model:zoom="zoom"
      :center="center"
      :use-global-leaflet="false"
      style="height: 400px; width: 100%;"
      @click="handleMapClick"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>

      <!-- Route line between SMCC and room location -->
      <l-polyline
        v-if="markerLatLng"
        :lat-lngs="[smccMarker.position, markerLatLng]"
        color="#FF9800"
        :weight="3"
        :opacity="0.7"
      >
        <l-popup>
          <div>Distance: {{ calculateDistance() }} km</div>
        </l-popup>
      </l-polyline>

      <!-- SMCC Marker (always visible) -->
      <l-marker
        :lat-lng="smccMarker.position"
        :icon="smccMarker.icon"
        :draggable="false"
      >
        <l-popup>
          <div class="font-weight-bold">{{ smccMarker.title }}</div>
        </l-popup>
      </l-marker>

      <!-- Room Location Marker (if provided) -->
      <l-marker
        v-if="markerLatLng"
        :lat-lng="markerLatLng"
        :draggable="true"
        @dragend="handleMarkerDragEnd"
      >
        <l-popup>
          <div>
            {{ popupContent }}<br>
            Distance from SMCC: {{ calculateDistance() }} km
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup, LPolyline } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from 'leaflet';

// Fix for the default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
});

// Create custom star icon for SMCC
const smccIcon = L.divIcon({
  html: `<div class="star-marker">
          <svg viewBox="0 0 24 24" style="width: 50px; height: 50px;">
            <path fill="#FF9800" d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z" />
          </svg>
        </div>`,
  className: 'custom-div-icon',
  iconSize: [30, 30],
  iconAnchor: [15, 15],
  popupAnchor: [0, -15],
});

export default {
  name: "LeafletMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LPolyline,
  },
  props: {
    markerLatLng: {
      type: Array,
      default: null,
    },
    popupContent: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      // Default center is set to SMCC coordinates
      center: [8.9882671, 125.3404024],
      zoom: 15,
      smccMarker: {
        position: [8.9882671, 125.3404024],
        title: 'Saint Michael College of Caraga',
        icon: smccIcon
      }
    };
  },
  methods: {
    handleMapClick(event) {
      // Emit the click event with the coordinates
      this.$emit('marker-click', event);
    },
    handleMarkerDragEnd(event) {
      // Emit the new marker position after dragging
      const latLng = event.target.getLatLng();
      this.$emit('marker-click', { latlng: latLng });
    },
    updateCenter(newCenter) {
      this.center = newCenter;
    },
    calculateDistance() {
      if (!this.markerLatLng) return 0;
      
      const lat1 = this.smccMarker.position[0];
      const lon1 = this.smccMarker.position[1];
      const lat2 = this.markerLatLng[0];
      const lon2 = this.markerLatLng[1];
      
      const R = 6371; // Earth's radius in kilometers
      const dLat = this.toRad(lat2 - lat1);
      const dLon = this.toRad(lon2 - lon1);
      
      const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(this.toRad(lat1)) * Math.cos(this.toRad(lat2)) *
                Math.sin(dLon/2) * Math.sin(dLon/2);
      
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      const distance = R * c;
      
      return distance.toFixed(2);
    },
    toRad(value) {
      return value * Math.PI / 180;
    }
  },
  watch: {
    markerLatLng(newVal) {
      if (newVal) {
        this.updateCenter(newVal);
      }
    }
  }
};
</script>

<style scoped>
.map-container {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
  width: 100%;
  min-height: 200px;
  position: relative;
}

/* Make sure Leaflet container takes full height */
:deep(.leaflet-container) {
  width: 100%;
  height: 100%;
  z-index: 1;
}

:deep(.custom-div-icon) {
  background: none;
  border: none;
}

:deep(.star-marker) {
  display: flex;
  justify-content: center;
  align-items: center;
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.5));
}

:deep(.star-marker svg) {
  transform-origin: center;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}
</style> 