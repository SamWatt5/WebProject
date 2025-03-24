<script setup lang="ts">
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { CalendarDays } from "lucide-vue-next";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import Spotify from "@/components/icons/Spotify.vue";
import { string } from "zod";

const spotifyClick = () => {
    console.log("Spotify clicked");
}

defineProps({
    name: String,
    avatar: String,
    joined: String
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
            <Spotify class="mt-2 cursor-pointer" @click="spotifyClick" />
        </div>
        </CardHeader>
    </Card>
</template>