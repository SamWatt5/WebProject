<script setup lang="ts">
/**
 * App.vue
 *
 * The root component of the application.
 *
 * Features:
 * - Integrates Vue Router for navigation using `RouterView`.
 * - Includes a global toast notification system using `Toaster`.
 * - Supports dark mode using `@vueuse/core`'s `useColorMode` composable.
 *
 * Dependencies:
 * - vue-router: For routing and navigation.
 * - vue-sonner: For toast notifications.
 * - @vueuse/core: For managing color mode (dark/light theme).
 */

import { RouterLink, RouterView } from 'vue-router';
import { Toaster } from './components/ui/sonner';
import { useColorMode } from '@vueuse/core';

// Initialize color mode (dark/light theme)
const mode = useColorMode();
</script>

<template>
  <div class="app">
    <!-- Global toast notification system -->
    <Toaster theme="dark" richColors :expand="false" />
    <!-- Router view for rendering matched components -->
    <RouterView />
  </div>
</template>

<style scoped>
/* Prevent scrolling on the body */
body {
  overflow: hidden;
}
</style>
