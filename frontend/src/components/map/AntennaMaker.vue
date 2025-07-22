<template>
    <div class="antenna-marker">
      <i class="fas fa-broadcast-tower" :style="{ color: color }"></i>
      <div class="antenna-label" v-if="label">{{ label }}</div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AntennaMarker',
    props: {
      color: {
        type: String,
        default: 'red'
      },
      label: {
        type: String,
        default: ''
      }
    }
  }
  </script>
  
  <style scoped>
  .antenna-marker {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .antenna-marker i {
    font-size: 24px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  }
  
  .antenna-label {
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 12px;
    margin-top: 2px;
    white-space: nowrap;
  }
  </style>