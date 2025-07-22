<template>
    <div class="parameters-input">
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Paramètres de simulation</h5>
        </div>
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-6">
              <div class="form-group">
                <label for="technology">Technologie</label>
                <select class="form-select" id="technology" v-model="parameters.technology">
                  <option value="2G">2G - GSM</option>
                  <option value="3G">3G - UMTS</option>
                  <option value="4G">4G - LTE</option>
                </select>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label for="propagation_model">Modèle de propagation</label>
                <select class="form-select" id="propagation_model" v-model="parameters.propagation_model">
                  <option value="OKUMURA_HATA">Okumura-Hata</option>
                  <option value="COST_231">COST-231</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-4">
              <div class="form-group">
                <label for="frequency">Fréquence (MHz)</label>
                <input type="number" class="form-control" id="frequency" v-model.number="parameters.frequency">
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="antenna_height">Hauteur d'antenne (m)</label>
                <input type="number" class="form-control" id="antenna_height" v-model.number="parameters.antenna_height">
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="antenna_power">Puissance d'antenne (dBm)</label>
                <input type="number" class="form-control" id="antenna_power" v-model.number="parameters.antenna_power">
              </div>
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <div class="form-group">
                <label for="terrain_type">Type de terrain</label>
                <select class="form-select" id="terrain_type" v-model="parameters.terrain_type">
                  <option value="URBAN">Urbain</option>
                  <option value="SUBURBAN">Suburbain</option>
                  <option value="RURAL">Rural</option>
                  <option value="OPEN">Ouvert</option>
                </select>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label for="radius">Rayon de simulation (km)</label>
                <input type="number" class="form-control" id="radius" v-model.number="parameters.radius">
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-end">
            <button class="btn btn-primary" @click="updateParameters">Mettre à jour</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ParametersInput',
    props: {
      value: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        parameters: { ...this.value }
      }
    },
    watch: {
      value: {
        handler(newValue) {
          this.parameters = { ...newValue }
        },
        deep: true
      }
    },
    methods: {
      updateParameters() {
        this.$emit('input', this.parameters)
        this.$emit('update', this.parameters)
      }
    }
  }
  </script>