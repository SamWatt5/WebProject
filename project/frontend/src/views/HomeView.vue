<script setup lang="ts">
/**
 * HomeView.vue
 *
 * The main home view component that dynamically displays either the logged-in or logged-out home page
 * based on the user's authentication status.
 *
 * Features:
 * - Displays the logged-in home page (`LoggedInHome`) if the user is authenticated.
 * - Displays the logged-out home page (`LoggedOutHome`) if the user is not authenticated.
 * - Fetches the current user's data from the backend API on component mount.
 * - Shows a loading toast while user data is being fetched.
 *
 * Dependencies:
 * - Pinia: For state management (user store).
 * - Custom UI components: Sidebar, LoggedInHome, LoggedOutHome.
 * - Vue composables: `onMounted`, `ref`.
 * - vue-sonner: For toast notifications.
 *
 * State:
 * - `user` (ref<User | null>): Stores the current user's information.
 * - `isLoading` (ref<boolean>): Indicates whether the user data is being loaded.
 *
 * Methods:
 * - `spotifyClick()`: Placeholder method for handling Spotify-related actions.
 */

import Sidebar from "@/components/Sidebar.vue";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import SidebarProvider from "@/components/ui/sidebar/SidebarProvider.vue";
import { Separator } from "@/components/ui/separator";
import { Card, CardDescription, CardTitle, CardHeader, CardContent } from "@/components/ui/card";
import { CalendarDays } from "lucide-vue-next";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import Spotify from "@/components/icons/Spotify.vue";
import { Button } from "@/components/ui/button";
import UserCard from "@/components/UserCard.vue";
import ListeningToCard from "@/components/ListeningToCard.vue";
import { useUser } from "@/stores/user";
import { onMounted, ref } from "vue";
import LoggedInHome from "@/components/LoggedInHome.vue";
import LoggedOutHome from "@/components/LoggedOutHome.vue";
import { toast } from "vue-sonner";

// Mock data for top tracks
const music: string[] = Array.from({ length: 50 }).map((_, i) => `Song ${i + 1}`);

// Access the user store
let { user, setUser } = useUser();

// Ref to track loading state
const isLoading = ref(true);

// Display a loading toast message
toast.loading("Loading user data...", {
  duration: Infinity,
  id: "loading-data",
  dismissible: false,
});

/**
 * Fetches the current user's data from the backend API.
 *
 * Updates the `user` state with the fetched data and dismisses the loading toast.
 */
onMounted(async () => {
  try {
    const res = await fetch("/api/user/me", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();

    if (!data.error) {
      setUser(data);
      console.log("Set user successfully", data);
      user = data;
    }
    isLoading.value = false;
    toast.dismiss("loading-data");
  } catch (err) {
    console.error(err);
  }
});

/**
 * Placeholder method for handling Spotify-related actions.
 */
const spotifyClick = () => {
  console.log("Spotify clicked");
};
</script>

<template>
  <div>
    <!-- Display the logged-in home page if the user is authenticated -->
    <LoggedInHome v-if="!isLoading && user" />
    <!-- Display the logged-out home page if the user is not authenticated -->
    <LoggedOutHome v-if="!isLoading && !user" />
  </div>
</template>
