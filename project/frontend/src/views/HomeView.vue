<script setup lang="ts">
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

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

let { user, setUser } = useUser();
const isLoading = ref(true);

onMounted(async() => {
    try {
      const res = await fetch("/api/user/me", {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      const data = await res.json();

      if(!data.error) {
        setUser(data);
        console.log("Set user successfully", data);
        user = data;
      }
      isLoading.value = false;
    } catch(err) {
      console.error(err);
    }
});

const spotifyClick = () => {
  console.log("Spotify clicked");
};
</script>

<template>
  <div class="">
    <LoggedInHome v-if="!isLoading && user" />
    <LoggedOutHome v-if="!isLoading && !user" />
  </div>
</template>
