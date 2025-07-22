<template>
  <div class="dashboard">
    <div class="container-fluid">
      <!-- En-tête avec titre et bouton d'action -->
      <div class="row mb-4">
        <div class="col-12 d-flex justify-content-between align-items-center">
          <div>
            <h1 class="mb-0">Tableau de bord</h1>
            <p class="text-muted">Vue d'ensemble de vos simulations et statistiques</p>
          </div>
          <button 
            class="btn btn-outline-primary" 
            @click="toggleEditMode"
            :title="editMode ? 'Terminer la personnalisation' : 'Personnaliser le tableau de bord'"
          >
            <i :class="editMode ? 'fas fa-check' : 'fas fa-cog'"></i>
            {{ editMode ? 'Terminer' : 'Personnaliser' }}
          </button>
        </div>
      </div>

      <!-- Filtres du tableau de bord -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-3">
                  <label class="form-label">Période</label>
                  <select class="form-select" v-model="filters.period">
                    <option value="7days">7 derniers jours</option>
                    <option value="30days">30 derniers jours</option>
                    <option value="90days">3 derniers mois</option>
                    <option value="all">Toutes les périodes</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Technologie</label>
                  <select class="form-select" v-model="filters.technology">
                    <option value="all">Toutes</option>
                    <option value="2G">2G</option>
                    <option value="3G">3G</option>
                    <option value="4G">4G</option>
                    <option value="5G">5G</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Type de zone</label>
                  <select class="form-select" v-model="filters.areaType">
                    <option value="all">Tous</option>
                    <option value="URBAN">Urbain</option>
                    <option value="SUBURBAN">Péri-urbain</option>
                    <option value="RURAL">Rural</option>
                    <option value="OPEN">Zone ouverte</option>
                  </select>
                </div>
                <div class="col-md-3 d-flex align-items-end">
                  <button class="btn btn-primary w-100" @click="applyFilters" :disabled="isLoading">
                    <i class="fas fa-filter me-2"></i>
                    {{ isLoading ? 'Chargement...' : 'Appliquer les filtres' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- État de chargement -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Chargement...</span>
        </div>
        <p class="mt-3">Chargement des données du tableau de bord...</p>
      </div>

      <!-- Grille des widgets -->
      <div v-else>
        <!-- Widgets principaux -->
        <div class="row">
          <!-- Carte de couverture -->
          <div class="col-12 col-xl-8 mb-4">
            <CoverageMapWidget :simulations="filteredSimulations" />
          </div>
          
          <!-- Métriques de performance -->
          <div class="col-12 col-xl-4 mb-4">
            <PerformanceMetricsWidget :simulations="filteredSimulations" />
          </div>
        </div>

        <!-- Widgets secondaires -->
        <div class="row">
          <!-- Dernières simulations -->
          <div class="col-12 col-lg-6 mb-4">
            <RecentSimulationsWidget :simulations="recentSimulations" />
          </div>
          
          <!-- Statistiques d'utilisation -->
          <div class="col-12 col-lg-6 mb-4">
            <UsageStatisticsWidget :simulations="recentSimulations" />
          </div>
        </div>

        <!-- Grille des widgets dynamiques -->
        <div class="row">
          <div class="col-12">
            <div class="row g-4">
              <!-- Widgets actifs -->
              <template v-for="widgetId in activeWidgets" :key="widgetId">
                <div class="col-12 col-md-6 col-lg-4">
                  <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                      <h5 class="mb-0">{{ getWidgetTitle(widgetId) }}</h5>
                      <div>
                        <button 
                          v-if="editMode"
                          class="btn btn-sm btn-outline-danger ms-2"
                          @click="removeWidget(widgetId)"
                          title="Supprimer ce widget"
                        >
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                    </div>
                    <div class="card-body">
                      <component 
                        :is="getWidgetComponent(widgetId)" 
                        :simulations="simulations"
                        :filters="filters"
                        :key="widgetId + '-component'"
                      />
                    </div>
                  </div>
                </div>
              </template>

              <!-- Bouton pour ajouter des widgets -->
              <div v-if="editMode" class="col-12">
                <div class="card">
                  <div class="card-body text-center">
                    <h5 class="mb-3">Ajouter un widget</h5>
                    <div class="d-flex flex-wrap gap-2 justify-content-center">
                      <button 
                        v-for="widget in availableWidgets" 
                        :key="widget.id"
                        class="btn btn-outline-primary"
                        @click="addWidget(widget.id)"
                        :disabled="isWidgetActive(widget.id)"
                        :title="isWidgetActive(widget.id) ? 'Déjà ajouté' : 'Ajouter ce widget'"
                      >
                        <i :class="'fas fa-' + (widget.icon || 'cube') + ' me-2'"></i>
                        {{ widget.name }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Configuration du tableau de bord -->
        <div class="row mt-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Personnaliser le tableau de bord</h5>
                <button class="btn btn-sm btn-outline-primary" @click="showWidgetSelector = !showWidgetSelector">
                  <i class="fas fa-plus me-1"></i> Ajouter un widget
                </button>
              </div>
              <div class="card-body" v-if="showWidgetSelector">
                <div class="row">
                  <div class="col-md-4 mb-3" v-for="widget in availableWidgets" :key="widget.id">
                    <div class="card h-100">
                      <div class="card-body">
                        <h6 class="card-title">{{ widget.name }}</h6>
                        <p class="card-text small text-muted">{{ widget.description }}</p>
                        <button 
                          class="btn btn-sm btn-outline-primary"
                          @click="addWidget(widget.id)"
                          :disabled="isWidgetActive(widget.id)"
                        >
                          {{ isWidgetActive(widget.id) ? 'Ajouté' : 'Ajouter' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

// Import des composants de widgets
import CoverageMapWidget from '@/components/dashboard/widgets/CoverageMapWidget.vue';
import PerformanceMetricsWidget from '@/components/dashboard/widgets/PerformanceMetricsWidget.vue';
import RecentSimulationsWidget from '@/components/dashboard/widgets/RecentSimulationsWidget.vue';
import UsageStatisticsWidget from '@/components/dashboard/widgets/UsageStatisticsWidget.vue';

// Configuration des widgets disponibles
const WIDGETS_CONFIG = {
  'coverage-map': {
    name: 'Carte de couverture',
    component: 'CoverageMapWidget',
    icon: 'map-marked-alt'
  },
  'performance-metrics': {
    name: 'Métriques de performance',
    component: 'PerformanceMetricsWidget',
    icon: 'chart-line'
  },
  'recent-simulations': {
    name: 'Dernières simulations',
    component: 'RecentSimulationsWidget',
    icon: 'history'
  },
  'usage-statistics': {
    name: 'Statistiques d\'utilisation',
    component: 'UsageStatisticsWidget',
    icon: 'chart-pie'
  }
};

export default {
  name: 'Dashboard',
  components: {
    CoverageMapWidget,
    PerformanceMetricsWidget,
    RecentSimulationsWidget,
    UsageStatisticsWidget
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // État local
    const filters = ref({
      period: '7days',
      technology: 'all',
      areaType: 'all'
    });
    
    const editMode = ref(false);
    const isLoading = ref(true);
    
    // Récupération des données du store
    const dashboardState = computed(() => store.state.dashboard || {});
    const simulationState = computed(() => ({
      simulations: store.state.simulations || [],
      loading: store.state.loading || false,
      currentSimulation: store.state.currentSimulation
    }));
    
    // Données calculées
    const recentSimulations = computed(() => {
      if (!simulationState.value.simulations) return [];
      return [...simulationState.value.simulations]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5);
    });
    
    // Filtrage des simulations
    const filteredSimulations = computed(() => {
      let result = [...(simulationState.value.simulations || [])];
      
      // Filtrage par période
      if (filters.value.period !== 'all') {
        const now = new Date();
        let fromDate = new Date();
        
        switch (filters.value.period) {
          case '7days':
            fromDate.setDate(now.getDate() - 7);
            break;
          case '30days':
            fromDate.setDate(now.getDate() - 30);
            break;
          case '90days':
            fromDate.setDate(now.getDate() - 90);
            break;
          default:
            break;
        }
        
        if (filters.value.period !== 'all') {
          result = result.filter(sim => new Date(sim.created_at) >= fromDate);
        }
      }
      
      // Filtrage par technologie
      if (filters.value.technology !== 'all') {
        result = result.filter(sim => 
          sim.parameters && sim.parameters.technology === filters.value.technology
        );
      }
      
      // Filtrage par type de zone
      if (filters.value.areaType !== 'all') {
        result = result.filter(sim => 
          sim.parameters && sim.parameters.terrain_type === filters.value.areaType
        );
      }
      
      return result;
    });
    
    // État pour le sélecteur de widgets
    const showWidgetSelector = ref(false);
    
    // Méthodes
    const applyFilters = async () => {
      try {
        isLoading.value = true;
        await store.dispatch('dashboard/updateFilters', filters.value);
        await store.dispatch('fetchSimulations');
      } catch (error) {
        console.error('Erreur lors de l\'application des filtres:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    const toggleEditMode = () => {
      editMode.value = !editMode.value;
    };
    
    const toggleWidget = async (widgetId) => {
      try {
        await store.dispatch('dashboard/toggleWidget', widgetId);
      } catch (error) {
        console.error('Erreur lors de la gestion du widget:', error);
      }
    };
    
    const isWidgetActive = (widgetId) => {
      return dashboardState.value.activeWidgets.includes(widgetId);
    };
    
    const getWidgetTitle = (widgetId) => {
      const widget = dashboardState.value.availableWidgets.find(w => w.id === widgetId);
      return widget ? widget.name : widgetId;
    };
    
    const getWidgetComponent = (widgetId) => {
      switch (widgetId) {
        case 'coverage-map':
          return CoverageMapWidget;
        case 'performance-metrics':
          return PerformanceMetricsWidget;
        case 'recent-simulations':
          return RecentSimulationsWidget;
        case 'usage-statistics':
          return UsageStatisticsWidget;
        default:
          return null;
      }
    };
    
    // Cycle de vie du composant
    onMounted(async () => {
      try {
        // Initialisation du tableau de bord
        await store.dispatch('dashboard/initializeDashboard');
        
        // Chargement des simulations
        await store.dispatch('fetchSimulations');
        
        // Application des filtres par défaut
        await applyFilters();
      } catch (error) {
        console.error('Erreur lors du chargement du tableau de bord:', error);
        // Redirection vers la page d'accueil en cas d'erreur
        router.push('/');
      } finally {
        isLoading.value = false;
      }
    });
    
    // Surveillance des changements de filtres
    watch(
      () => filters.value,
      async (newFilters) => {
        if (!isLoading.value) {
          await applyFilters();
        }
      },
      { deep: true }
    );
    
    return {
      // État
      filters,
      editMode,
      isLoading: computed(() => isLoading.value || store.state.loading || (dashboardState.value && dashboardState.value.loading)),
      
      // Données
      simulations: computed(() => simulationState.value.simulations || []),
      currentSimulation: computed(() => simulationState.value.currentSimulation),
      recentSimulations,
      activeWidgets: computed(() => dashboardState.value.activeWidgets || []),
      availableWidgets: computed(() => dashboardState.value.availableWidgets || []),
      
      // Méthodes
      applyFilters,
      toggleEditMode,
      addWidget: toggleWidget,
      removeWidget: toggleWidget,
      isWidgetActive,
      getWidgetTitle,
      getWidgetComponent,
      
      // Propriétés calculées
      filteredSimulations,
      showWidgetSelector
    };
  }
};
</script>

<style scoped>
.dashboard {
  padding: 1rem 0;
}

.card {
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: all 0.3s ease;
  height: 100%;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
  padding: 1rem 1.25rem;
}

.card-body {
  padding: 1.25rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Styles pour les écrans mobiles */
@media (max-width: 768px) {
  .card {
    margin-bottom: 1rem;
  }
  
  .btn {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}

/* Animation pour les transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style scoped>
.dashboard {
  padding: 1.5rem 0;
  background-color: #f8f9fa;
  min-height: calc(100vh - 56px);
}

.card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1rem 1.25rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.btn-outline-primary {
  border-color: #0d6efd;
  color: #0d6efd;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  color: #fff;
}
</style>
