<template>
  <GridLayout>
    <SpotifyModule />
    <WeatherModule />
    <LedModule />
  </GridLayout>
</template>

<script>
import SpotifyModule from '@/components/modules/SpotifyModule.vue'
import WeatherModule from '@/components/modules/WeatherModule.vue'
import LedModule from '@/components/modules/LedModule.vue'
import GridLayout from '@/components/Layout/GridLayout.vue'

export default {
  components: {
    SpotifyModule,
    WeatherModule,
    LedModule,
    GridLayout,
  },
}
</script>
