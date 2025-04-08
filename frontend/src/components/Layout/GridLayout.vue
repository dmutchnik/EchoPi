<template>
    <div class="grid-container">
      <slot />
    </div>
  </template>
  
  <style scoped>
  .grid-container {
    display: grid;
    gap: 24px;
    padding: 32px;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
  </style>
  