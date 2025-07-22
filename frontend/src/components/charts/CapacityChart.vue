<template>
    <div class="capacity-chart">
      <Bar 
        :chart-data="chartData"
        :chart-options="chartOptions"
      />
    </div>
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
  
  ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
  
  export default {
    name: 'CapacityChart',
    components: {
      Bar
    },
    props: {
      data: {
        type: Array,
        required: true
      },
      title: {
        type: String,
        default: 'Capacité du réseau'
      }
    },
    computed: {
      chartData() {
        return {
          labels: this.data.map(item => item.label),
          datasets: [
            {
              label: 'Capacité (Mbps)',
              backgroundColor: this.data.map(item => item.color || '#3498db'),
              data: this.data.map(item => item.value)
            }
          ]
        }
      },
      chartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            title: {
              display: true,
              text: this.title,
              font: {
                size: 16
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Capacité (Mbps)'
              }
            }
          }
        }
      }
    }
  }
  </script>