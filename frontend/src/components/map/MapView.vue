<template>
    <div class="map-container">
      <div id="map" ref="map"></div>
      <div class="map-controls" v-if="showControls">
        <div class="btn-group">
          <button class="btn btn-sm btn-primary" @click="zoomIn"><i class="fas fa-plus"></i></button>
          <button class="btn btn-sm btn-primary" @click="zoomOut"><i class="fas fa-minus"></i></button>
          <button class="btn btn-sm btn-secondary" @click="resetView"><i class="fas fa-home"></i></button>
        </div>
      </div>
      <div class="map-legend" v-if="showLegend">
        <h6>Légende</h6>
        <div class="legend-item">
          <span class="legend-color" style="background-color: #ff0000;"></span>
          <span>Signal excellent (> -70 dBm)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background-color: #ffff00;"></span>
          <span>Signal bon (-85 à -70 dBm)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background-color: #00ff00;"></span>
          <span>Signal moyen (-100 à -85 dBm)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background-color: #0000ff;"></span>
          <span>Signal faible (< -100 dBm)</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import L from 'leaflet'
  import 'leaflet.heat';
  //import 'leaflet.heat/dist/leaflet-heat.js';
  import 'leaflet/dist/leaflet.css'
  import icon from 'leaflet/dist/images/marker-icon.png';
  import iconShadow from 'leaflet/dist/images/marker-shadow.png';

  let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
  });

  L.Marker.prototype.options.icon = DefaultIcon;
  
  export default {
    name: 'MapView',
    props: {
      center: {
        type: Array,
        default: () => [48.8566, 2.3522] // Paris by default
      },
      zoom: {
        type: Number,
        default: 13
      },
      markers: {
        type: Array,
        default: () => []
      },
      coverageData: {
        type: Object,
        default: null
      },
      showControls: {
        type: Boolean,
        default: true
      },
      showLegend: {
        type: Boolean,
        default: true
      }
    },
    data() {
      return {
        map: null,
        tileLayer: null,
        markerLayer: null,
        coverageLayer: null
      }
    },
    mounted() {
      //this.initMap()
      //this.addMarkers()
      //if (this.coverageData) {
      //  this.addCoverageLayer()
      //}
      this.$nextTick(() => {
        console.log('DOM prêt, initialisation de la carte');
        this.initMap();
        if (this.markers.length > 0) {
          this.addMarkers();
        }
        if (this.coverageData) {
          this.addCoverageLayer();
        }
      });
    },
    methods: {
      initMap() {
        console.log('Élément map:', this.$refs.map);
        this.map = L.map(this.$refs.map).setView(this.center, this.zoom)
        
        //this.tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        //}).addTo(this.map)
        //Essayez cette alternative si OpenStreetMap ne fonctionne pas
         this.tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
           attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
         }).addTo(this.map);
        
        this.markerLayer = L.layerGroup().addTo(this.map)
      },
      addMarkers() {
        this.markerLayer.clearLayers()
        
        this.markers.forEach(marker => {
          const icon = L.divIcon({
            html: `<i class="fas fa-broadcast-tower fa-2x" style="color: ${marker.color || 'red'};"></i>`,
            className: 'custom-div-icon',
            iconSize: [30, 30],
            iconAnchor: [15, 30]
          })
          
          const markerObj = L.marker([marker.lat, marker.lng], { icon })
          
          if (marker.popup) {
            markerObj.bindPopup(marker.popup)
          }
          
          markerObj.addTo(this.markerLayer)
        })
      },
      addCoverageLayer() {
        if (this.coverageLayer) {
          this.map.removeLayer(this.coverageLayer)
        }
        
        if (!this.coverageData || !this.coverageData.signal_strength_data) {
          return
        }
        
        const heatmapData = []
        
        Object.entries(this.coverageData.signal_strength_data).forEach(([coord, signal]) => {
          const [lng, lat] = coord.split(',').map(parseFloat)
          
          // Normalize signal strength to a value between 0 and 1
          // Assuming signal strength ranges from -120 dBm to -50 dBm
          const normalizedIntensity = (signal + 120) / 70
          
          heatmapData.push([lat, lng, normalizedIntensity])
        })
        
        this.coverageLayer = L.heatLayer(heatmapData, {
          radius: 25,
          blur: 15,
          maxZoom: 17,
          gradient: {
            0.4: 'blue',
            0.6: 'lime',
            0.8: 'yellow',
            1.0: 'red'
          }
        }).addTo(this.map)
        
        // Adjust map view to fit coverage
        if (heatmapData.length > 0) {
          const bounds = L.latLngBounds(heatmapData.map(point => [point[0], point[1]]))
          this.map.fitBounds(bounds)
        }
      },
      zoomIn() {
        this.map.zoomIn()
      },
      zoomOut() {
        this.map.zoomOut()
      },
      resetView() {
        this.map.setView(this.center, this.zoom)
      }
    },
    watch: {
      markers: {
        handler() {
          this.addMarkers()
        },
        deep: true
      },
      coverageData: {
        handler() {
          if (this.coverageData) {
            this.addCoverageLayer()
          }
        },
        deep: true
      },
      center: {
        handler(newCenter) {
          if (this.map) {
            this.map.setView(newCenter, this.map.getZoom())
          }
        },
        deep: true
      }
    },
    beforeUnmount() {
      if (this.map) {
        this.map.remove()
      }
    }
  }
  </script>
  
  <style scoped>
  .map-container {
    position: relative;
    width: 100%;
    height: 500px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  #map {
    width: 100%;
    height: 100%;
  }
  
  .map-controls {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1000;
  }
  
  .map-legend {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 10px;
    border-radius: 5px;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
  }
  
  .legend-color {
    display: inline-block;
    width: 20px;
    height: 10px;
    margin-right: 5px;
  }
  </style>