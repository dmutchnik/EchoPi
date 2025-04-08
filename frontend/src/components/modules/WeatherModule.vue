<template>
    <div class="module-card">
      <h2>🌤️ Weather Module</h2>
      <p>Loading weather data...</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "WeatherModule",
    mounted() {
      // Placeholder: Call weather API here
    },
  }
  </script>
  
  <style scoped>
  .module-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 24px;
    color: white;
    box-shadow: 0 8px 16px rgba(0,0,0,0.4);
    backdrop-filter: blur(6px);
  }
  </style>
  