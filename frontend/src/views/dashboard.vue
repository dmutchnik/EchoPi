<template>
    <div id="app" class="app-wrapper">
      <Dashboard />
    </div>
  </template>
  
  <script>
  import Dashboard from './views/Dashboard.vue'
  
  export default {
    name: 'App',
    components: {
      Dashboard
    }
  }
  </script>
  
  <style>
  body {
    margin: 0;
    background: #121212;
    font-family: 'Inter', sans-serif;
  }
  
  .app-wrapper {
    min-height: 100vh;
    color: white;
    background: linear-gradient(to bottom, #0f0f0f, #1a1a1a);
  }
  </style>
  