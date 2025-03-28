/**
 * index.ts
 *
 * The main router configuration file for the application.
 *
 * Features:
 * - Defines routes for all views in the application.
 * - Uses Vue Router's `createRouter` and `createWebHistory` for navigation.
 * - Supports lazy loading of components for improved performance.
 *
 * Dependencies:
 * - vue-router: For routing and navigation.
 */

import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

// Create the router instance
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Use HTML5 history mode
  routes: [
    {
      path: '/', // Home route
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login', // Login route
      name: 'login',
      component: () => import('../views/LoginView.vue'), // Lazy-loaded
    },
    {
      path: '/register', // Registration route
      name: 'register',
      component: () => import('../views/RegisterView.vue'), // Lazy-loaded
    },
    {
      path: '/friends', // Friends management route
      name: 'friends',
      component: () => import('../views/FriendsView.vue'), // Lazy-loaded
    },
    {
      path: '/playlists', // Playlists management route
      name: 'playlists',
      component: () => import('../views/PlaylistsView.vue'), // Lazy-loaded
    },
    {
      path: '/admin', // Admin dashboard route
      name: 'admin',
      component: () => import('../views/AdminView.vue'), // Lazy-loaded
    },
    {
      path: '/recommend', // Recommendations route
      name: 'recommend',
      component: () => import('../views/RecommendView.vue'), // Lazy-loaded
    },
    {
      path: '/settings', // User settings route
      name: 'settings',
      component: () => import('../views/SettingView.vue'), // Lazy-loaded
    },
  ],
});

export default router;
