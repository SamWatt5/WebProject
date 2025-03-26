<script setup lang="ts">
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { CalendarDays } from "lucide-vue-next";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import Spotify from "@/components/icons/Spotify.vue";
import { string } from "zod";

defineProps({
    name: String,
    avatar: String,
    joined: String,
    spotify_id: String
})
</script>

<template>
    <Card class="cursor-pointer">
        <CardHeader class="flex flex-row">
        <Avatar class="w-20 h-20 mt-2">
            <AvatarFallback class="text-3xl">{{ avatar }}</AvatarFallback>
        </Avatar>
        <div class="flex flex-col pl-3">
            <CardTitle class="text-4xl">@{{ name }}</CardTitle>
            <CardDescription class="flex flex-row"><CalendarDays class="h-8 w-8 mt-1" /><span class="mt-[3px] text-lg ml-1"> Joined {{ joined }}</span></CardDescription>
            <!-- <<RouterLink as-child :href="`https://open.spotify.com/user/${name}`">
                <Spotify class="mt-2 cursor-pointer" />
            </RouterLink>> -->
            <a :href="`https://open.spotify.com/user/${spotify_id}`" target="_blank" class="mt-2">
                <Spotify class="cursor-pointer mt-2" />
            </a>
        </div>
        </CardHeader>
    </Card>
</template>