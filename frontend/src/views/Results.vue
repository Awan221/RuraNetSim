<template>
    <div class="results">
      <div class="container">
        <h1 class="mb-4">Résultats de simulation</h1>
        
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Chargement...</span>
          </div>
          <p class="mt-3">Chargement des résultats...</p>
        </div>
        
        <div v-else-if="error" class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
        
        <div v-else-if="simulation">
          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">{{ simulation.name }}</h5>
            </div>
            <div class="card-body">
              <p v-if="simulation.description">{{ simulation.description }}</p>
              
              <div class="row">
                <div class="col-md-6">
                  <h6>Paramètres</h6>
                  <table class="table table-sm" v-if="simulation.parameters && simulation.parameters.length">
                    <tbody>
                      <tr v-for="(param, index) in simulation.parameters" :key="index">
                        <td>Technologie</td>
                        <td>{{ param.technology }}</td>
                      </tr>
                      <tr v-for="(param, index) in simulation.parameters" :key="'p'+index">
                        <td>Modèle de propagation</td>
                        <td>{{ param.propagation_model }}</td>
                      </tr>
                      <tr v-for="(param, index) in simulation.parameters" :key="'f'+index">
                        <td>Fréquence</td>
                        <td>{{ param.frequency }} MHz</td>
                      </tr>
                      <tr v-for="(param, index) in simulation.parameters" :key="'h'+index">
                        <td>Hauteur d'antenne</td>
                        <td>{{ param.antenna_height }} m</td>
                      </tr>
                      <tr v-for="(param, index) in simulation.parameters" :key="'p2'+index">
                        <td>Puissance d'antenne</td>
                        <td>{{ param.antenna_power }} dBm</td>
                      </tr>
                      <tr v-for="(param, index) in simulation.parameters" :key="'t'+index">
                        <td>Type de terrain</td>
                        <td>{{ param.terrain_type }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <div class="col-md-6">
                  <h6>Résultats</h6>
                  <table class="table table-sm" v-if="simulation.results && simulation.results.length">
                    <tbody>
                      <tr v-for="(result, index) in simulation.results" :key="index">
                        <td>Couverture</td>
                        <td>{{ result.coverage_percentage.toFixed(2) }}%</td>
                      </tr>
                      <tr v-for="(result, index) in simulation.results" :key="'p'+index" v-if="result.population_covered">
                        <td>Population couverte</td>
                        <td>{{ result.population_covered.toLocaleString() }}</td>
                      </tr>
                      <tr>
                        <td>Date de simulation</td>
                        <td>{{ new Date(simulation.created_at).toLocaleString() }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          
          <div class="map-container mb-4" v-if="simulation.parameters && simulation.parameters.length && simulation.results && simulation.results.length">
            <h5>Carte de couverture</h5>
            <MapView 
              :center="getMapCenter(simulation.parameters[0])" 
              :zoom="12" 
              :markers="getAntennaMarkers(simulation.parameters[0])"
              :coverageData="{ signal_strength_data: simulation.results[0].signal_strength_data }"
            />
          </div>
          
          <div class="d-flex justify-content-end">
            <button class="btn btn-primary me-2" @click="exportPDF">
              <i class="fas fa-file-pdf me-1"></i> Exporter en PDF
            </button>
            <router-link to="/simulation" class="btn btn-secondary">
              <i class="fas fa-plus me-1"></i> Nouvelle simulation
            </router-link>
          </div>
        </div>
        
        <div v-else class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          Aucun résultat trouvé pour cette simulation.
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import MapView from '@/components/map/MapView.vue'
  
  export default {
    name: 'Results',
    components: {
      MapView
    },
    props: {
      id: {
        type: [String, Number],
        required: true
      }
    },
    data() {
      return {
        simulation: null,
        loading: false,
        error: null
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated'])
    },
    created() {
      this.fetchSimulation()
    },
    methods: {
      async fetchSimulation() {
        if (!this.isAuthenticated) {
          this.$router.push('/login')
          return
        }
        
        this.loading = true
        try {
          this.simulation = await this.$store.dispatch('fetchSimulation', this.id)
        } catch (error) {
          this.error = 'Erreur lors du chargement de la simulation'
          console.error('Error fetching simulation:', error)
        } finally {
          this.loading = false
        }
      },
      getMapCenter(params) {
        if (params && params.location) {
          const coords = params.location.coordinates
          return [coords[1], coords[0]] // [lat, lng]
        }
        return [48.8566, 2.3522] // Paris by default
      },
      getAntennaMarkers(params) {
        if (params && params.location) {
          const coords = params.location.coordinates
          return [
            {
              lat: coords[1],
              lng: coords[0],
              color: this.getTechnologyColor(params.technology),
              popup: `<strong>${params.technology}</strong><br>Puissance: ${params.antenna_power} dBm<br>Hauteur: ${params.antenna_height} m`
            }
          ]
        }
        return []
      },
      getTechnologyColor(technology) {
        switch (technology) {
          case '2G': return '#FF5722'
          case '3G': return '#2196F3'
          case '4G': return '#4CAF50'
          default: return '#9C27B0'
        }
      },
      exportPDF() {
        this.$store.dispatch('exportSimulationPdf', this.id)
          .catch(error => {
            console.error('Error exporting PDF:', error)
          })
      }
    }
  }
  </script>
  
  <style scoped>
  .map-container {
    margin-top: 20px;
  }
  </style>