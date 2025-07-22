<template>
    <div class="simulation-list">
      <div class="container">
        <h1 class="mb-4">Mes simulations</h1>
        
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Chargement...</span>
          </div>
          <p class="mt-3">Chargement des simulations...</p>
        </div>
        
        <div v-else-if="error" class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
        
        <div v-else-if="simulations.length === 0" class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          Vous n'avez pas encore créé de simulation.
        </div>
        
        <div v-else>
          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Simulations récentes</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Nom</th>
                      <th>Technologie</th>
                      <th>Date de création</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="sim in (Array.isArray(simulations) ? simulations.filter(s => s && s.id) : [])" :key="sim.id">

                      <td>{{ sim.name }}</td>
                      <td>{{ getSimulationTechnology(sim) }}</td>
                      <td>{{ new Date(sim.created_at).toLocaleString() }}</td>
                      <td>
                        <router-link :to="`/results/${sim.id}`" class="btn btn-sm btn-primary me-2">
                          <i class="fas fa-eye me-1"></i> Voir
                        </router-link>
                        <button class="btn btn-sm btn-danger" @click="deleteSimulation(sim.id)">
                          <i class="fas fa-trash me-1"></i> Supprimer
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-end">
            <router-link to="/simulation" class="btn btn-primary">
              <i class="fas fa-plus me-1"></i> Nouvelle simulation
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'SimulationList',
    data() {
      return {
        loading: false,
        error: null
      }
    },
    computed: {
      ...mapGetters(['simulations'])
    },
    created() {
      this.fetchSimulations()
    },
    methods: {
      async fetchSimulations() {
        this.loading = true
        try {
          await this.$store.dispatch('fetchSimulations')
          this.error = null
        } catch (error) {
          this.error = 'Erreur lors du chargement des simulations'
          console.error('Error fetching simulations:', error)
        } finally {
          this.loading = false
        }
      },
      getSimulationTechnology(simulation) {
        if (simulation.parameters && simulation.parameters.length > 0) {
          return simulation.parameters[0].technology
        }
        return 'N/A'
      },
      async deleteSimulation(id) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cette simulation?')) {
          try {
            await this.$store.dispatch('deleteSimulation', id)
            this.fetchSimulations()
          } catch (error) {
            console.error('Error deleting simulation:', error)
          }
        }
      }
    }
  }
  </script>