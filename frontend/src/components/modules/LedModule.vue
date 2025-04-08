<template>
    <div class="module-card">
      <h2>💡 LED Controller</h2>
      <p>Placeholder for LED controls</p>
      <button class="led-button" @click="toggleLED">Toggle LED</button>
    </div>
  </template>
  
  <script>
  export default {
    name: "LedModule",
    methods: {
      toggleLED() {
        // Placeholder: Call backend endpoint for LED toggle
        console.log("LED toggle clicked");
      },
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
  .led-button {
    margin-top: 16px;
    padding: 8px 16px;
    background: #1db954;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
  }
  .led-button:hover {
    background: #1ed760;
  }
  </style>
  