<template>
    <div class="results-view">
      <div class="card">
        <div class="card-header bg-success text-white">
          <h5 class="mb-0">Résultats de simulation</h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Chargement...</span>
            </div>
            <p class="mt-3">Calcul des résultats en cours...</p>
          </div>
          
          <div v-else-if="error" class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ error }}
          </div>
          
          <div v-else-if="results">
            <div class="row mb-4">
              <div class="col-md-6">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">Statistiques de couverture</h5>
                    <div class="stats-container">
                      <div class="stat-item">
                        <div class="stat-value">{{ results.coverage_percentage.toFixed(2) }}%</div>
                        <div class="stat-label">Zone couverte</div>
                      </div>
                      <div class="stat-item" v-if="results.population_covered !== null">
                        <div class="stat-value">{{ results.population_covered.toLocaleString() }}</div>
                        <div class="stat-label">Population couverte</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-md-6">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">Qualité du signal</h5>
                    <div class="signal-quality-chart">
                      <CoverageChart :data="signalQualityData" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="map-container mb-4">
              <h5>Carte de couverture</h5>
              <MapView 
                :center="mapCenter" 
                :zoom="12" 
                :markers="antennaMarkers"
                :coverageData="results"
              />
            </div>
            
            <div class="d-flex justify-content-end">
              <button class="btn btn-primary me-2" @click="exportPDF">
                <i class="fas fa-file-pdf me-1"></i> Exporter en PDF
              </button>
              <button class="btn btn-secondary" @click="$emit('new-simulation')">
                <i class="fas fa-plus me-1"></i> Nouvelle simulation
              </button>
            </div>
          </div>
          
          <div v-else class="alert alert-info">
            <i class="fas fa-info-circle me-2"></i>
            Aucun résultat disponible. Veuillez lancer une simulation.
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import MapView from '@/components/map/MapView.vue'
  import CoverageChart from '@/components/charts/CoverageChart.vue'
  
  export default {
    name: 'ResultsView',
    components: {
      MapView,
      CoverageChart
    },
    props: {
      results: {
        type: Object,
        default: null
      },
      simulationId: {
        type: Number,
        default: null
      },
      parameters: {
        type: Object,
        default: () => ({})
      },
      loading: {
        type: Boolean,
        default: false
      },
      error: {
        type: String,
        default: null
      }
    },
    computed: {
      signalQualityData() {
        console.log('Calcul des données de qualité du signal');
        console.log('Résultats:', this.results);
    
        // Valeurs par défaut si aucune donnée n'est disponible
        const defaultData = [
          { label: 'Excellent (>-70 dBm)', value: 0, color: '#4CAF50' },
          { label: 'Bon (-85 à -70 dBm)', value: 0, color: '#8BC34A' },
          { label: 'Moyen (-100 à -85 dBm)', value: 0, color: '#FFC107' },
          { label: 'Faible (<-100 dBm)', value: 0, color: '#F44336' }
        ];
    
        if (!this.results || !this.results.signal_strength_data) {
          console.warn('Données de signal manquantes');
          return defaultData;
        }
        
        try {
          const signalData = Object.values(this.results.signal_strength_data);
          console.log('Valeurs de signal:', signalData);
      
          if (!signalData || signalData.length === 0) {
            console.warn('Aucune valeur de signal');
            return defaultData;
          }
      
          // Compter les signaux dans différentes plages de qualité
          const excellent = signalData.filter(signal => signal >= -70).length;
          const good = signalData.filter(signal => signal >= -85 && signal < -70).length;
          const fair = signalData.filter(signal => signal >= -100 && signal < -85).length;
          const poor = signalData.filter(signal => signal < -100).length;
      
          console.log('Répartition des signaux:', { excellent, good, fair, poor });
      
          return [
            { label: 'Excellent (>-70 dBm)', value: excellent, color: '#4CAF50' },
            { label: 'Bon (-85 à -70 dBm)', value: good, color: '#8BC34A' },
            { label: 'Moyen (-100 à -85 dBm)', value: fair, color: '#FFC107' },
            { label: 'Faible (<-100 dBm)', value: poor, color: '#F44336' }
          ];
        } catch (error) {
          console.error('Erreur lors du calcul des données de qualité du signal:', error);
          return defaultData;
        }
      },
      mapCenter() {
        if (this.parameters && this.parameters.latitude && this.parameters.longitude) {
          return [this.parameters.latitude, this.parameters.longitude]
        }
        return [48.8566, 2.3522] // Paris by default
      },
      antennaMarkers() {
        if (this.parameters && this.parameters.latitude && this.parameters.longitude) {
          return [
            {
              lat: this.parameters.latitude,
              lng: this.parameters.longitude,
              color: this.getTechnologyColor(this.parameters.technology),
              popup: `<strong>${this.parameters.technology}</strong><br>Puissance: ${this.parameters.antenna_power} dBm<br>Hauteur: ${this.parameters.antenna_height} m`
            }
          ]
        }
        return []
      },
      /*signalQualityData() {
        if (!this.results || !this.results.signal_strength_data) {
          return []
        }
        
        const signalData = Object.values(this.results.signal_strength_data)
        
        // Count signals in different quality ranges
        const excellent = signalData.filter(signal => signal >= -70).length
        const good = signalData.filter(signal => signal >= -85 && signal < -70).length
        const fair = signalData.filter(signal => signal >= -100 && signal < -85).length
        const poor = signalData.filter(signal => signal < -100).length
        
        return [
          { label: 'Excellent (>-70 dBm)', value: excellent, color: '#4CAF50' },
          { label: 'Bon (-85 à -70 dBm)', value: good, color: '#8BC34A' },
          { label: 'Moyen (-100 à -85 dBm)', value: fair, color: '#FFC107' },
          { label: 'Faible (<-100 dBm)', value: poor, color: '#F44336' }
        ]
      }*/
    },
    methods: {
      getTechnologyColor(technology) {
        switch (technology) {
          case '2G': return '#FF5722'
          case '3G': return '#2196F3'
          case '4G': return '#4CAF50'
          default: return '#9C27B0'
        }
      },
      exportPDF() {
        if (this.simulationId) {
          this.$store.dispatch('exportSimulationPdf', this.simulationId)
            .catch(error => {
              console.error('Error exporting PDF:', error)
            })
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .stats-container {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }
  
  .stat-item {
    text-align: center;
  }
  
  .stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary-color);
  }
  
  .stat-label {
    font-size: 0.9rem;
    color: #666;
  }
  
  .map-container {
    margin-top: 20px;
  }
  
  .signal-quality-chart {
    height: 250px;
  }
  </style>