<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">Statistiques d'utilisation</h5>
    </div>
    <div class="card-body">
      <div v-if="!hasSimulations" class="h-100 d-flex flex-column justify-content-center align-items-center text-muted">
        <i class="fas fa-chart-pie fa-3x mb-3"></i>
        <p class="mb-0 text-center">Aucune donnée à afficher</p>
      </div>
      <div v-else>
        <div class="row g-4">
          <!-- Répartition par technologie -->
          <div class="col-12">
            <h6 class="mb-3">Répartition par technologie</h6>
            <div class="chart-container" style="height: 160px;">
              <canvas ref="techChart"></canvas>
            </div>
            <div class="d-flex justify-content-center flex-wrap mt-3">
              <div v-for="(item, index) in techDistribution" :key="index" class="d-flex align-items-center me-4 mb-2">
                <span class="legend-dot me-2" :style="{ backgroundColor: item.backgroundColor }"></span>
                <span class="small">{{ item.technology }} ({{ item.percentage }}%)</span>
              </div>
            </div>
          </div>
          
          <!-- Répartition par type de zone -->
          <div class="col-12">
            <h6 class="mb-3">Répartition par type de zone</h6>
            <div class="chart-container" style="height: 160px;">
              <canvas ref="areaChart"></canvas>
            </div>
            <div class="d-flex justify-content-center flex-wrap mt-3">
              <div v-for="(item, index) in areaDistribution" :key="index" class="d-flex align-items-center me-4 mb-2">
                <span class="legend-dot me-2" :style="{ backgroundColor: item.backgroundColor }"></span>
                <span class="small">{{ item.area }} ({{ item.percentage }}%)</span>
              </div>
            </div>
          </div>
          
          <!-- Activité récente -->
          <div class="col-12">
            <h6 class="mb-3">Activité récente</h6>
            <div class="activity-timeline">
              <div v-for="(activity, index) in recentActivities" :key="index" class="activity-item">
                <div class="activity-icon" :class="getActivityIconClass(activity.type)">
                  <i :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <div class="d-flex justify-content-between">
                    <span class="fw-semibold">{{ activity.title }}</span>
                    <small class="text-muted">{{ formatTimeAgo(activity.timestamp) }}</small>
                  </div>
                  <p class="small mb-0">{{ activity.description }}</p>
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
import { Chart, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';

export default {
  name: 'UsageStatisticsWidget',
  props: {
    simulations: {
      type: Array,
      required: true,
      default: () => []
    },
    filters: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      techChart: null,
      areaChart: null,
      techDistribution: [],
      areaDistribution: [],
      recentActivities: [
        {
          type: 'simulation',
          title: 'Nouvelle simulation 5G',
          description: 'Simulation de couverture urbaine terminée',
          timestamp: new Date(Date.now() - 3600000) // 1 heure ago
        },
        {
          type: 'update',
          title: 'Mise à jour des paramètres',
          description: 'Paramètres de propagation mis à jour',
          timestamp: new Date(Date.now() - 7200000) // 2 heures ago
        },
        {
          type: 'report',
          title: 'Rapport généré',
          description: 'Rapport de couverture exporté',
          timestamp: new Date(Date.now() - 86400000) // 1 jour ago
        }
      ]
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
        this.calculateDistributions();
        this.initCharts();
      },
      deep: true
    }
  },
  mounted() {
    if (this.hasSimulations) {
      this.calculateDistributions();
      this.initCharts();
    }
  },
  methods: {
    calculateDistributions() {
      if (!this.hasSimulations) return;
      
      // Calculer la distribution par technologie
      const techCounts = {};
      this.simulations.forEach(sim => {
        const tech = sim.technology || 'Inconnu';
        techCounts[tech] = (techCounts[tech] || 0) + 1;
      });
      
      this.techDistribution = Object.entries(techCounts).map(([tech, count]) => ({
        technology: tech,
        count,
        percentage: Math.round((count / this.simulations.length) * 100),
        backgroundColor: this.getTechColor(tech)
      }));
      
      // Calculer la distribution par type de zone
      const areaCounts = {};
      this.simulations.forEach(sim => {
        const area = sim.terrain_type || 'Non spécifié';
        areaCounts[area] = (areaCounts[area] || 0) + 1;
      });
      
      this.areaDistribution = Object.entries(areaCounts).map(([area, count]) => ({
        area,
        count,
        percentage: Math.round((count / this.simulations.length) * 100),
        backgroundColor: this.getAreaColor(area)
      }));
    },
    
    initCharts() {
      if (!this.hasSimulations) return;
      
      // Enregistrer les composants nécessaires de Chart.js
      Chart.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);
      
      // Détruire les graphiques existants
      if (this.techChart) this.techChart.destroy();
      if (this.areaChart) this.areaChart.destroy();
      
      // Graphique des technologies
      const techCtx = this.$refs.techChart.getContext('2d');
      this.techChart = new Chart(techCtx, {
        type: 'doughnut',
        data: {
          labels: this.techDistribution.map(item => item.technology),
          datasets: [{
            data: this.techDistribution.map(item => item.percentage),
            backgroundColor: this.techDistribution.map(item => item.backgroundColor),
            borderWidth: 0,
            cutout: '70%'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.raw}%`;
                }
              }
            }
          },
          cutoutPercentage: 70
        }
      });
      
      // Graphique des types de zone
      const areaCtx = this.$refs.areaChart.getContext('2d');
      this.areaChart = new Chart(areaCtx, {
        type: 'bar',
        data: {
          labels: this.areaDistribution.map(item => item.area),
          datasets: [{
            data: this.areaDistribution.map(item => item.percentage),
            backgroundColor: this.areaDistribution.map(item => item.backgroundColor),
            borderRadius: 4,
            barThickness: 20
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.raw}%`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              grid: {
                display: false,
                drawBorder: false
              },
              ticks: {
                callback: function(value) {
                  return value + '%';
                },
                stepSize: 25
              }
            },
            x: {
              grid: {
                display: false,
                drawBorder: false
              },
              ticks: {
                display: false
              }
            }
          }
        }
      });
    },
    
    getTechColor(tech) {
      const colors = {
        '2G': '#4e73df',
        '3G': '#1cc88a',
        '4G': '#36b9cc',
        '5G': '#f6c23e',
        'Inconnu': '#858796'
      };
      return colors[tech] || '#' + Math.floor(Math.random()*16777215).toString(16);
    },
    
    getAreaColor(area) {
      const colors = {
        'URBAN': '#4e73df',
        'SUBURBAN': '#1cc88a',
        'RURAL': '#f6c23e',
        'OPEN': '#36b9cc',
        'Non spécifié': '#858796'
      };
      return colors[area] || '#' + Math.floor(Math.random()*16777215).toString(16);
    },
    
    getActivityIcon(type) {
      const icons = {
        'simulation': 'fas fa-broadcast-tower',
        'update': 'fas fa-cog',
        'report': 'fas fa-file-alt',
        'user': 'fas fa-user'
      };
      return icons[type] || 'fas fa-circle';
    },
    
    getActivityIconClass(type) {
      return `bg-${type}`;
    },
    
    formatTimeAgo(date) {
      const seconds = Math.floor((new Date() - new Date(date)) / 1000);
      
      let interval = Math.floor(seconds / 31536000);
      if (interval > 1) return `Il y a ${interval} ans`;
      if (interval === 1) return 'Il y a un an';
      
      interval = Math.floor(seconds / 2592000);
      if (interval > 1) return `Il y a ${interval} mois`;
      if (interval === 1) return 'Il y a un mois';
      
      interval = Math.floor(seconds / 86400);
      if (interval > 1) return `Il y a ${interval} jours`;
      if (interval === 1) return 'Hier';
      
      interval = Math.floor(seconds / 3600);
      if (interval >= 1) return `Il y a ${interval} h`;
      
      interval = Math.floor(seconds / 60);
      if (interval >= 1) return `Il y a ${interval} min`;
      
      return 'À l\'instant';
    }
  },
  beforeUnmount() {
    if (this.techChart) this.techChart.destroy();
    if (this.areaChart) this.areaChart.destroy();
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
}

.legend-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.activity-timeline {
  position: relative;
  padding-left: 24px;
}

.activity-timeline::before {
  content: '';
  position: absolute;
  left: 9px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #e3e6f0;
}

.activity-item {
  position: relative;
  padding-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.activity-item:last-child {
  padding-bottom: 0;
}

.activity-icon {
  position: absolute;
  left: -24px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.5rem;
  z-index: 1;
}

.activity-content {
  background-color: #f8f9fc;
  border-radius: 0.35rem;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
}

.bg-simulation {
  background-color: #4e73df;
}

.bg-update {
  background-color: #1cc88a;
}

.bg-report {
  background-color: #f6c23e;
}

.bg-user {
  background-color: #36b9cc;
}

.fw-semibold {
  font-weight: 600;
}

.small {
  font-size: 0.8rem;
}

.text-muted {
  color: #858796 !important;
}
</style>
