<script lang="ts" setup>
import { Card, CardTitle, CardHeader, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import PeopleWatching from "./images/PeopleWatching.vue";

// Define props for the component
defineProps({
    title: {
        type: String,
        required: true, // The track title is required
    },
    artist: {
        type: String,
        required: true, // The artist name is required
    },
    coverImage: {
        type: String,
        required: false, // The cover image URL is optional
        default: "", // Default to an empty string if not provided
    },
    link: {
        type: String,
        required: false,
        default: ""
    },
    label: {
        type: Boolean,
        default: true,
        required: false,
    }
});
</script>

<template>
    <div>
        <a :href="link">
            <Card>
                <CardHeader>
                    <CardTitle v-if="label">
                        Recently Listened to
                    </CardTitle>
                </CardHeader>
                <CardContent class="flex flex-row items-center">
                    <!-- Display the cover image if provided -->
                    <img v-if="coverImage" :src="coverImage" alt="Cover Art"
                        class="w-16 h-16 rounded-md object-cover" />
                    <PeopleWatching v-else /> <!-- Fallback icon if no cover image is provided -->
                    <div class="ml-4">
                        <!-- Display the track title -->
                        <p class="font-bold">{{ title }}</p>
                        <!-- Display the artist name -->
                        <CardDescription>{{ artist }}</CardDescription>
                    </div>
                </CardContent>
                <CardFooter v-if="!label"></CardFooter>
            </Card>
        </a>
    </div>
</template>