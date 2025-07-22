<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">Métriques de performance</h5>
    </div>
    <div class="card-body">
      <div v-if="!hasSimulations" class="h-100 d-flex flex-column justify-content-center align-items-center text-muted">
        <i class="fas fa-chart-bar fa-3x mb-3"></i>
        <p class="mb-0 text-center">Aucune donnée de simulation à afficher</p>
      </div>
      <div v-else>
        <div class="row g-3 mb-4">
          <div class="col-6 col-md-6">
            <div class="metric-card">
              <div class="metric-value">{{ metrics.averageCoverage }}%</div>
              <div class="metric-label">Couverture moyenne</div>
              <div class="metric-change" :class="getChangeClass(metrics.coverageChange)">
                <i :class="getChangeIcon(metrics.coverageChange)"></i>
                {{ Math.abs(metrics.coverageChange) }}% vs période précédente
              </div>
            </div>
          </div>
          <div class="col-6 col-md-6">
            <div class="metric-card">
              <div class="metric-value">{{ metrics.totalSimulations }}</div>
              <div class="metric-label">Simulations</div>
              <div class="metric-change" :class="getChangeClass(metrics.simulationsChange)">
                <i :class="getChangeIcon(metrics.simulationsChange)"></i>
                {{ Math.abs(metrics.simulationsChange) }}% vs période précédente
              </div>
            </div>
          </div>
          <div class="col-6 col-md-6">
            <div class="metric-card">
              <div class="metric-value">{{ metrics.avgSignalStrength }} dBm</div>
              <div class="metric-label">Signal moyen</div>
              <div class="metric-change" :class="getChangeClass(metrics.signalChange)">
                <i :class="getChangeIcon(metrics.signalChange)"></i>
                {{ Math.abs(metrics.signalChange) }}% vs période précédente
              </div>
            </div>
          </div>
          <div class="col-6 col-md-6">
            <div class="metric-card">
              <div class="metric-value">{{ metrics.successRate }}%</div>
              <div class="metric-label">Taux de réussite</div>
              <div class="metric-change" :class="getChangeClass(metrics.successRateChange)">
                <i :class="getChangeIcon(metrics.successRateChange)"></i>
                {{ Math.abs(metrics.successRateChange) }}% vs période précédente
              </div>
            </div>
          </div>
        </div>

        <div class="chart-container" style="height: 200px;">
          <canvas ref="coverageTrendChart"></canvas>
        </div>
      </div>
    </div>
    <div class="card-footer bg-transparent text-end">
      <small class="text-muted">Mis à jour à {{ lastUpdated }}</small>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

export default {
  name: 'PerformanceMetricsWidget',
  props: {
    simulations: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  data() {
    return {
      chart: null,
      metrics: {
        averageCoverage: 0,
        coverageChange: 0,
        totalSimulations: 0,
        simulationsChange: 0,
        avgSignalStrength: 0,
        signalChange: 0,
        successRate: 0,
        successRateChange: 0
      },
      lastUpdated: new Date().toLocaleTimeString()
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
        this.calculateMetrics();
        this.updateChart();
      },
      deep: true
    }
  },
  mounted() {
    if (this.hasSimulations) {
      this.calculateMetrics();
      this.initChart();
    }
  },
  methods: {
    calculateMetrics() {
      if (!this.hasSimulations) return;
      
      // Calculer les métriques de base
      const totalCoverage = this.simulations.reduce((sum, sim) => 
        sum + (sim.coverage_percentage || 0), 0);
      
      const totalSignal = this.simulations.reduce((sum, sim) => 
        sum + (sim.avg_signal_strength || -80), 0);
      
      const successfulSims = this.simulations.filter(sim => 
        sim.status === 'completed' && sim.coverage_percentage >= 50).length;
      
      this.metrics = {
        averageCoverage: Math.round(totalCoverage / this.simulations.length * 10) / 10,
        coverageChange: this.getRandomChange(),
        totalSimulations: this.simulations.length,
        simulationsChange: this.getRandomChange(),
        avgSignalStrength: Math.round(totalSignal / this.simulations.length * 10) / 10,
        signalChange: this.getRandomChange(),
        successRate: Math.round((successfulSims / this.simulations.length) * 1000) / 10,
        successRateChange: this.getRandomChange()
      };
      
      this.lastUpdated = new Date().toLocaleTimeString();
    },
    
    initChart() {
      if (!this.hasSimulations) return;
      
      // Enregistrer les composants nécessaires de Chart.js
      Chart.register(...registerables);
      
      // Créer le graphique de tendance
      const ctx = this.$refs.coverageTrendChart.getContext('2d');
      
      // Données factices pour la démo
      const labels = Array.from({ length: 12 }, (_, i) => {
        const date = new Date();
        date.setMonth(date.getMonth() - (11 - i));
        return date.toLocaleString('default', { month: 'short' });
      });
      
      const data = {
        labels,
        datasets: [
          {
            label: 'Couverture moyenne',
            data: labels.map(() => Math.floor(Math.random() * 30) + 70),
            borderColor: '#1e88e5',
            backgroundColor: 'rgba(30, 136, 229, 0.1)',
            tension: 0.3,
            fill: true
          }
        ]
      };
      
      const config = {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              min: 50,
              max: 100,
              grid: {
                drawBorder: false
              },
              ticks: {
                callback: function(value) {
                  return value + '%';
                }
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          },
          elements: {
            point: {
              radius: 0
            }
          }
        }
      };
      
      this.chart = new Chart(ctx, config);
    },
    
    updateChart() {
      if (!this.chart || !this.hasSimulations) return;
      
      // Mettre à jour les données du graphique
      // Dans une vraie application, vous récupéreriez ces données de votre API
      this.chart.data.datasets[0].data = this.chart.data.labels.map(() => 
        Math.floor(Math.random() * 30) + 70
      );
      
      this.chart.update();
    },
    
    getChangeClass(change) {
      if (change > 0) return 'text-success';
      if (change < 0) return 'text-danger';
      return 'text-muted';
    },
    
    getChangeIcon(change) {
      if (change > 0) return 'fas fa-arrow-up';
      if (change < 0) return 'fas fa-arrow-down';
      return 'fas fa-equals';
    },
    
    getRandomChange() {
      // Générer un changement aléatoire entre -15 et 15
      return Math.floor(Math.random() * 30 - 15);
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
};
</script>

<style scoped>
.metric-card {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
  height: 100%;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.05);
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.75rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.metric-change {
  font-size: 0.7rem;
  font-weight: 500;
}

.metric-change i {
  font-size: 0.6rem;
  margin-right: 0.25rem;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.chart-container {
  position: relative;
  width: 100%;
}
</style>
