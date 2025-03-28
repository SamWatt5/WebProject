<script setup lang="ts">
/**
 * This file is OLD and contains nothing, but removing it causes issues with node, so it stays!
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

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

const playlistClick = () => {
  console.log("playlist clicked");
};
</script>

<template>
  <div class="flex flex-row">
    <main class="flex h-screen items-center place-self-start">
      <SidebarProvider :default-open="false" :open="false">
        <Sidebar />
      </SidebarProvider>

      <div class="flex flex-col ml-10">
        <h1 class="text-4xl text-center mb-4">Your Music</h1>
        <ScrollArea class="w-80 h-[75vh] border rounded-lg">
          <div class="p-4">
            <div v-for="song in music" :key="song">
              {{ song }}
              <Separator class="my-2" />
            </div>
          </div>
        </ScrollArea>
      </div>
      <Separator orientation="vertical" class="mx-10" />
    </main>
    <div class="grid grid-cols-3 grid-rows-10 pt-10 gap-4">
      <div>

      </div>
      <div class="col-span-2"></div>

      <div class="col-span-2"></div>
      <ScrollArea class="border rounded-md col-span-3 w-[95%] whitespace-nowrap">
        <div class="flex p-4 space-x-4 w-max">
          <!-- Add the playlist cards here :) -->
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  </div>
</template>
