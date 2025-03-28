<script setup lang="ts">
/**
 * UserCard.vue
 *
 * A component for displaying a user's profile card with details such as their name, avatar, join date, and Spotify profile link.
 *
 * Features:
 * - Displays the user's avatar, username, and join date.
 * - Provides a clickable Spotify icon that links to the user's Spotify profile.
 *
 * Props:
 * - `name` (String, required): The username of the user.
 * - `avatar` (String, required): The user's avatar or fallback text.
 * - `joined` (String, required): The date the user joined.
 * - `spotify_id` (String, required): The user's Spotify ID for linking to their Spotify profile.
 *
 * Dependencies:
 * - Custom UI components: Card, CardHeader, CardTitle, CardDescription, Avatar, AvatarFallback.
 * - Spotify.vue: A custom icon component for the Spotify logo.
 */

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { CalendarDays } from "lucide-vue-next";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import Spotify from "@/components/icons/Spotify.vue";

defineProps({
    name: {
        type: String,
        required: true,
    },
    avatar: {
        type: String,
        required: true,
    },
    joined: {
        type: String,
        required: true,
    },
    spotify_id: {
        type: String,
        required: true,
    },
});
</script>

<template>
    <Card class="cursor-pointer">
        <!-- Card header with user details -->
        <CardHeader class="flex flex-row">
            <!-- User avatar -->
            <Avatar class="w-20 h-20 mt-2">
                <AvatarFallback class="text-3xl">{{ avatar }}</AvatarFallback>
            </Avatar>
            <div class="flex flex-col pl-3">
                <!-- Username -->
                <CardTitle class="text-4xl">@{{ name }}</CardTitle>
                <!-- Join date -->
                <CardDescription class="flex flex-row">
                    <CalendarDays class="h-8 w-8 mt-1" />
                    <span class="mt-[3px] text-lg ml-1">Joined {{ joined }}</span>
                </CardDescription>
                <!-- Spotify profile link -->
                <a :href="`https://open.spotify.com/user/${spotify_id}`" target="_blank" class="mt-2">
                    <Spotify class="cursor-pointer mt-2" />
                </a>
            </div>
        </CardHeader>
    </Card>
</template>