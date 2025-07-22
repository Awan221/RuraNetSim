<template>
    <div class="simulation-form">
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Nouvelle Simulation</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="submitForm" @keydown.enter.prevent>
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="name" class="form-label">Nom de la simulation</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  v-model="formData.name" 
                  required
                  placeholder="Ex: Simulation réseau 4G - Zone rurale"
                >
              </div>
              <div class="col-md-6">
                <label for="technology" class="form-label">Technologie</label>
                <select class="form-select" id="technology" v-model="formData.technology" required @change="onTechnologyChange">
                  <option value="">Sélectionner une technologie</option>
                  <option value="2G">2G - GSM</option>
                  <option value="3G">3G - UMTS</option>
                  <option value="4G">4G - LTE</option>
                  <option value="5G">5G - Nouvelle Radio (NR)</option>
                </select>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="propagation_model" class="form-label">Modèle de propagation</label>
                <select 
                  class="form-select" 
                  id="propagation_model" 
                  v-model="formData.propagation_model" 
                  required
                  :disabled="formData.technology === '5G'"
                >
                  <option value="">Sélectionner un modèle</option>
                  <option value="OKUMURA_HATA">Okumura-Hata</option>
                  <option value="COST_231">COST-231</option>
                  <option v-if="formData.technology === '5G'" value="3GPP_TR_38901">3GPP TR 38.901 (5G)</option>
                </select>
              </div>
              
              <!-- Sélecteur de type de réseau 5G -->
              <div v-if="formData.technology === '5G'" class="col-12 mt-3">
                <h6>Paramètres 5G</h6>
                <NetworkTypeSelector 
                  v-model="network5GParams"
                  @network-type-change="on5GNetworkTypeChange"
                  @scenario-change="on5GScenarioChange"
                />
              </div>
              <div class="col-md-6">
                <label for="terrain_type" class="form-label">Type de terrain</label>
                <select class="form-select" id="terrain_type" v-model="formData.terrain_type" required>
                  <option value="">Sélectionner un type de terrain</option>
                  <option value="URBAN">Urbain</option>
                  <option value="SUBURBAN">Suburbain</option>
                  <option value="RURAL">Rural</option>
                  <option value="OPEN">Ouvert</option>
                </select>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-4">
                <label for="frequency" class="form-label">Fréquence (MHz)</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="frequency" 
                  v-model.number="formData.frequency" 
                  required
                  min="700"
                  max="2600"
                  step="0.1"
                >
                <div class="form-text">Plage valide: 700-2600 MHz</div>
              </div>
              <div class="col-md-4">
                <label for="antenna_height" class="form-label">Hauteur d'antenne (m)</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="antenna_height" 
                  v-model.number="formData.antenna_height" 
                  required
                  min="3"
                  max="200"
                  step="0.1"
                >
                <div class="form-text">Plage valide: 3-200 m</div>
              </div>
              <div class="col-md-4">
                <label for="antenna_power" class="form-label">Puissance d'antenne (dBm)</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="antenna_power" 
                  v-model.number="formData.antenna_power" 
                  required
                  min="10"
                  max="60"
                  step="0.1"
                >
                <div class="form-text">Plage valide: 10-60 dBm</div>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-4">
                <label for="latitude" class="form-label">Latitude</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="latitude" 
                  v-model.number="formData.latitude" 
                  required
                  min="-90"
                  max="90"
                  step="0.000001"
                >
              </div>
              <div class="col-md-4">
                <label for="longitude" class="form-label">Longitude</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="longitude" 
                  v-model.number="formData.longitude" 
                  required
                  min="-180"
                  max="180"
                  step="0.000001"
                >
              </div>
              <div class="col-md-4">
                <label for="radius" class="form-label">Rayon de simulation (km)</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="radius" 
                  v-model.number="formData.radius" 
                  required
                  min="1"
                  max="20"
                  step="0.1"
                >
                <div class="form-text">Plage valide: 1-20 km</div>
              </div>
            </div>
            
            <div class="mb-3">
              <label for="population_density" class="form-label">Densité de population (hab/km²)</label>
              <input 
                type="number" 
                class="form-control" 
                id="population_density" 
                v-model.number="formData.population_density" 
                min="0"
                step="0.1"
              >
              <div class="form-text">Optionnel - Pour estimer la population couverte</div>
            </div>
            
            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea 
                class="form-control" 
                id="description" 
                v-model="formData.description" 
                rows="3"
                placeholder="Description optionnelle de la simulation"
              ></textarea>
            </div>
            
            <div class="d-flex justify-content-between">
              <button type="button" class="btn btn-secondary" @click="resetForm">Réinitialiser</button>
              <button 
                type="submit" 
                class="btn btn-primary" 
                :disabled="isLoading"
                @click="submitForm"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                Lancer la simulation
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import NetworkTypeSelector from './NetworkTypeSelector.vue'
  
  export default {
    components: {
      NetworkTypeSelector
    },
    
    name: 'SimulationForm',
    data() {
      return {
        formData: {
          name: '',
          technology: '4G',
          propagation_model: 'OKUMURA_HATA',
          frequency: 1800,
          bandwidth: 10,
          antenna_height: 30,
          antenna_power: 43,
          terrain_type: 'URBAN',
          location: '',
          latitude: 0,
          longitude: 0,
          radius: 1,
          population_density: 100, // Densité de population par kilomètre carré
          description: ''
        },
        network5GParams: {
          networkType: '5g',
          scenario: 'UMa',
          los_condition: 'LOS',
          h_bs: 10.0,
          h_ut: 1.5,
          h: 20.0,
          w: 20.0
        }
      }
    },
    computed: {
      ...mapGetters(['isLoading'])
    },
    methods: {
      onTechnologyChange() {
        if (this.formData.technology === '5G') {
          this.formData.propagation_model = '3GPP_TR_38901';
          // Initialiser les paramètres 5G par défaut
          this.network5GParams = {
            networkType: '5g',
            scenario: 'UMa',
            los_condition: 'LOS',
            h_bs: 10.0,
            h_ut: 1.5,
            h: 20.0,
            w: 20.0
          };
        } else {
          this.formData.propagation_model = '';
        }
      },
      
      on5GNetworkTypeChange(networkType) {
        // Mettre à jour les paramètres en fonction du type de réseau 5G
        console.log('Type de réseau 5G changé:', networkType);
      },
      
      on5GScenarioChange(scenario) {
        // Mettre à jour les paramètres en fonction du scénario 5G
        console.log('Scénario 5G changé:', scenario);
      },
      
      submitForm() {
        console.log('Soumission du formulaire...');
        // Fusionner les données du formulaire avec les paramètres 5G si nécessaire
        const formData = { ...this.formData };
        
        if (this.formData.technology === '5G') {
          formData.network5GParams = this.network5GParams;
        }
        
        console.log('Données du formulaire à envoyer :', formData);
        this.$emit('submit-form', formData);
      },
      
      resetForm() {
        this.formData = {
          name: '',
          technology: '4G',
          propagation_model: 'OKUMURA_HATA',
          terrain_type: 'URBAN',
          frequency: 1800,
          bandwidth: 10,
          antenna_height: 30,
          antenna_power: 43,
          latitude: 0,
          longitude: 0,
          radius: 1,
          population_density: 100, // Densité de population par kilomètre carré
          description: ''
        };
        this.network5GParams = {};
        this.$emit('reset');
      }
    }
  }
  </script>