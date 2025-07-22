<template>
    <div class="simulation">
      <div class="container">
        <h1 class="mb-4">Simulation de réseau</h1>
        
        <div v-if="error" class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
        
        <div v-if="showResults">
          <ResultsView 
            :results="simulationResults" 
            :simulationId="simulationId"
            :parameters="simulationParameters"
            :loading="isLoading"
            :error="error"
            @new-simulation="resetSimulation"
          />
        </div>
        <div v-else>
          <SimulationForm @submit-form="runSimulation" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import SimulationForm from '@/components/simulation/SimulationForm.vue'
  import ResultsView from '@/components/simulation/ResultsView.vue'
  
  export default {
    name: 'Simulation',
    components: {
      SimulationForm,
      ResultsView
    },
    data() {
      return {
        showResults: false,
        simulationResults: null,
        simulationId: null,
        simulationParameters: null,
        error: null
      }
    },
    computed: {
      ...mapGetters(['isLoading'])
    },
    methods: {
      async runSimulation(data) {
        console.log('runSimulation appelé avec les données :', data);
        try {
          this.error = null;
          console.log('Début de la simulation...');
          const response = await this.$store.dispatch('runSimulation', data);
          console.log('Réponse de la simulation :', response);
          
          await this.$store.dispatch('fetchSimulations');
          
          this.simulationResults = response.result;
          this.simulationId = response.simulation_id;
          this.simulationParameters = data;
          this.showResults = true;
          console.log('Simulation terminée avec succès');
        } catch (error) {
          console.error('Erreur lors de la simulation :', error);
          this.error = error.response?.data?.error || 'Une erreur est survenue lors de la simulation';
          console.error('Simulation error:', error)
        }
      },
      resetSimulation() {
        this.showResults = false
        this.simulationResults = null
        this.simulationId = null
        this.simulationParameters = null
        this.error = null
      }
    }
  }
  </script>