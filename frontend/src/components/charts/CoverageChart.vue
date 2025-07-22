<template>
  <div class="coverage-chart">
    <div v-if="!hasData" class="no-data-message">
      Aucune donnée de signal disponible
    </div>
    <Pie 
      v-else
      :data="chartData"
      :options="chartOptions"
    />

  </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

export default {
  name: 'CoverageChart',
  components: {
    Pie
  },
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  computed: {
    hasData() {
      return Array.isArray(this.data) && this.data.length > 0 && this.data.some(item => item.value > 0);
    },
    chartData() {
      if (!Array.isArray(this.data) || this.data.length === 0 || !this.data.some(item => item.value > 0)) {
        return {
          labels: ['Aucune donnée'],
          datasets: [{
            backgroundColor: ['#ccc'],
            data: [1]
          }]
        };
      }

    return {
      labels: this.data.map(item => item.label || 'Inconnu'),
      datasets: [
        {
          backgroundColor: this.data.map(item => item.color || '#000'),
          data: this.data.map(item => item.value || 0)
        }
      ]
    };
  },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              boxWidth: 12,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || '';
                const value = context.raw || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        }
      };
    }
  },
  mounted() {
    try {
      console.log('CoverageChart monté avec les données:', this.data);
    } catch (error) {
      console.error("Error in mounted hook:", error);
    }
    
  }
}
</script>

<style scoped>
.coverage-chart {
  height: 250px;
  position: relative;
}

.no-data-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-style: italic;
}
</style>