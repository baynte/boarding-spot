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
      <l-marker
        v-if="markerLatLng"
        :lat-lng="markerLatLng"
        draggable="true"
        @dragend="handleMarkerDragEnd"
      >
        <l-popup>
          <div>{{ popupContent }}</div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from 'leaflet';

// Fix for the marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
});

export default {
  name: "LeafletMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
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
      // Default center is set to SMCC area (approximate coordinates)
      center: [14.6091, 121.0223],
      zoom: 13,
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
</style> 