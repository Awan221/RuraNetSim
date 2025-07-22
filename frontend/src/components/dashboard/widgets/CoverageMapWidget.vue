<template>
  <div class="card h-100">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Carte de couverture</h5>
      <div class="btn-group" role="group">
        <button 
          class="btn btn-sm btn-outline-secondary"
          @click="changeMapType('standard')"
          :class="{ 'active': mapType === 'standard' }"
        >
          Standard
        </button>
        <button 
          class="btn btn-sm btn-outline-secondary"
          @click="changeMapType('satellite')"
          :class="{ 'active': mapType === 'satellite' }"
        >
          Satellite
        </button>
        <button 
          class="btn btn-sm btn-outline-secondary"
          @click="changeMapType('terrain')"
          :class="{ 'active': mapType === 'terrain' }"
        >
          Relief
        </button>
      </div>
    </div>
    <div class="card-body p-0" style="height: 400px;">
      <div id="coverage-map" class="h-100 w-100">
        <div v-if="!hasSimulations" class="h-100 d-flex flex-column justify-content-center align-items-center text-muted">
          <i class="fas fa-map-marked-alt fa-3x mb-3"></i>
          <p class="mb-0">Aucune donnée de simulation à afficher</p>
        </div>
        <div v-else class="h-100 d-flex justify-content-center align-items-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Chargement...</span>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer bg-transparent d-flex justify-content-between align-items-center">
      <div class="legend">
        <span class="me-3">Légende :</span>
        <span class="legend-item me-2">
          <span class="legend-color" style="background-color: #1e88e5;"></span>
          <span>Bonne couverture</span>
        </span>
        <span class="legend-item me-2">
          <span class="legend-color" style="background-color: #ff9800;"></span>
          <span>Couverture moyenne</span>
        </span>
        <span class="legend-item">
          <span class="legend-color" style="background-color: #f44336;"></span>
          <span>Faible couverture</span>
        </span>
      </div>
      <button class="btn btn-sm btn-outline-primary" @click="exportMap">
        <i class="fas fa-download me-1"></i> Exporter
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CoverageMapWidget',
  props: {
    simulations: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  data() {
    return {
      map: null,
      mapType: 'standard',
      markers: [],
      circles: []
    };
  },
  computed: {
    hasSimulations() {
      return this.simulations && this.simulations.length > 0;
    }
  },
  watch: {
    simulations: {
      handler() {
        this.updateMap();
      },
      deep: true
    },
    mapType() {
      this.updateMap();
    }
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      // Initialisation de la carte avec Leaflet ou une autre bibliothèque cartographique
      // Cette méthode sera implémentée plus tard avec la logique de la carte
      console.log('Initialisation de la carte de couverture');
    },
    updateMap() {
      if (!this.map) return;
      
      // Nettoyer les marqueurs et cercles existants
      this.clearMap();
      
      if (!this.hasSimulations) return;
      
      // Ajouter des marqueurs pour chaque simulation
      this.simulations.forEach(simulation => {
        if (simulation.latitude && simulation.longitude) {
          this.addSimulationToMap(simulation);
        }
      });
      
      // Ajuster la vue pour afficher tous les marqueurs
      this.fitMapToMarkers();
    },
    addSimulationToMap(simulation) {
      // Implémenter l'ajout d'un marqueur et d'un cercle de couverture pour une simulation
      console.log('Ajout de la simulation à la carte :', simulation.id);
      
      // Exemple avec Leaflet (à implémenter) :
      /*
      const marker = L.marker([simulation.latitude, simulation.longitude])
        .addTo(this.map)
        .bindPopup(`<b>${simulation.name}</b><br>${simulation.technology} - ${simulation.coverage_percentage}%`);
      
      const circle = L.circle([simulation.latitude, simulation.longitude], {
        color: this.getCoverageColor(simulation.coverage_percentage),
        fillColor: this.getCoverageColor(simulation.coverage_percentage, 0.2),
        fillOpacity: 0.5,
        radius: simulation.radius * 1000 // Convertir en mètres
      }).addTo(this.map);
      
      this.markers.push(marker);
      this.circles.push(circle);
      */
    },
    clearMap() {
      // Nettoyer les marqueurs et cercles existants
      this.markers.forEach(marker => marker.remove());
      this.circles.forEach(circle => circle.remove());
      this.markers = [];
      this.circles = [];
    },
    fitMapToMarkers() {
      if (this.markers.length === 0) return;
      
      // Ajuster la vue pour afficher tous les marqueurs
      // Exemple avec Leaflet :
      // this.map.fitBounds(L.featureGroup(this.markers).getBounds().pad(0.1));
    },
    getCoverageColor(coveragePercentage) {
      if (coveragePercentage >= 80) return '#1e88e5'; // Bleu pour bonne couverture
      if (coveragePercentage >= 50) return '#ff9800'; // Orange pour couverture moyenne
      return '#f44336'; // Rouge pour faible couverture
    },
    changeMapType(type) {
      this.mapType = type;
      // Implémenter le changement de type de carte
    },
    exportMap() {
      // Implémenter l'export de la carte
      console.log('Export de la carte');
      
      // Exemple d'export d'image (à implémenter avec une bibliothèque comme html2canvas)
      /*
      html2canvas(document.getElementById('coverage-map')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'carte-couverture.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
      });
      */
    }
  }
};
</script>

<style scoped>
.legend {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  font-size: 0.8rem;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}

.legend-color {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 0.5rem;
}

.btn-outline-secondary.active {
  background-color: #6c757d;
  color: white;
  border-color: #6c757d;
}

#coverage-map {
  min-height: 300px;
  background-color: #f8f9fa;
}
</style>
