<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HomeView from './views/HomeView.vue';
import { Toaster } from './components/ui/sonner';
</script>

<template>
  <div class="app">
    <Toaster theme="dark" richColors :expand="false" />
    <RouterView />
  </div>
</template>

<style scoped>
body {
  overflow: hidden;
}
</style>
