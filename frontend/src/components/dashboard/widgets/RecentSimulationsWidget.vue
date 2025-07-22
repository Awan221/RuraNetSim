<template>
  <div class="card h-100">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Dernières simulations</h5>
      <router-link to="/simulations" class="btn btn-sm btn-outline-primary">
        Voir tout
      </router-link>
    </div>
    <div class="card-body p-0">
      <div v-if="!hasSimulations" class="h-100 d-flex flex-column justify-content-center align-items-center text-muted p-4">
        <i class="fas fa-inbox fa-3x mb-3"></i>
        <p class="mb-0 text-center">Aucune simulation récente à afficher</p>
      </div>
      <div v-else class="list-group list-group-flush">
        <div 
          v-for="simulation in recentSimulations" 
          :key="simulation.id"
          class="list-group-item list-group-item-action"
          @click="viewSimulation(simulation.id)"
        >
          <div class="d-flex w-100 justify-content-between align-items-center">
            <div class="me-3">
              <h6 class="mb-1">{{ simulation.name }}</h6>
              <div class="d-flex flex-wrap align-items-center text-muted small">
                <span class="me-2">
                  <i class="fas fa-mobile-alt me-1"></i>
                  {{ getTechnologyLabel(simulation.technology) }}
                </span>
                <span class="me-2">
                  <i class="fas fa-map-marker-alt me-1"></i>
                  {{ simulation.terrain_type || 'Non spécifié' }}
                </span>
                <span>
                  <i class="far fa-calendar-alt me-1"></i>
                  {{ formatDate(simulation.created_at) }}
                </span>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <div class="me-3 text-end">
                <div class="fw-bold">{{ simulation.coverage_percentage || 0 }}%</div>
                <div class="small text-muted">Couverture</div>
              </div>
              <div class="status-badge" :class="getStatusClass(simulation.status)">
                {{ getStatusLabel(simulation.status) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer bg-transparent text-center">
      <button class="btn btn-sm btn-outline-primary" @click="startNewSimulation">
        <i class="fas fa-plus me-1"></i> Nouvelle simulation
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecentSimulationsWidget',
  props: {
    simulations: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  computed: {
    hasSimulations() {
      return this.simulations && this.simulations.length > 0;
    },
    recentSimulations() {
      return [...this.simulations]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5);
    }
  },
  methods: {
    getTechnologyLabel(tech) {
      const techMap = {
        '2G': '2G',
        '3G': '3G',
        '4G': '4G',
        '5G': '5G'
      };
      return techMap[tech] || tech || 'Inconnu';
    },
    
    getStatusClass(status) {
      const statusClasses = {
        'completed': 'bg-success',
        'running': 'bg-warning',
        'failed': 'bg-danger',
        'pending': 'bg-secondary'
      };
      return statusClasses[status] || 'bg-secondary';
    },
    
    getStatusLabel(status) {
      const statusLabels = {
        'completed': 'Terminé',
        'running': 'En cours',
        'failed': 'Échoué',
        'pending': 'En attente'
      };
      return statusLabels[status] || status || 'Inconnu';
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    },
    
    viewSimulation(id) {
      this.$router.push(`/simulations/${id}`);
    },
    
    startNewSimulation() {
      this.$router.push('/simulation/new');
    }
  }
};
</script>

<style scoped>
.list-group-item {
  border-left: 0;
  border-right: 0;
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.list-group-item:first-child {
  border-top: 0;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.list-group-item:last-child {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  z-index: 1;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.7rem;
  font-weight: 600;
  color: white;
  text-transform: capitalize;
  min-width: 80px;
  text-align: center;
}

.bg-success {
  background-color: #198754 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
  color: #212529 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}

.bg-secondary {
  background-color: #6c757d !important;
}

.small {
  font-size: 0.75rem;
}

.text-muted {
  color: #6c757d !important;
}

.fw-bold {
  font-weight: 600 !important;
}
</style>
