<script lang="ts" setup>
/**
 * ListeningToCard.vue
 *
 * A component for displaying a card with information about a recently listened-to track.
 *
 * Features:
 * - Displays the track title, artist name, and cover image (if provided).
 * - Provides a fallback icon if no cover image is available.
 * - Includes a clickable link to the track's external page.
 * - Optionally displays a label ("Recently Listened to") above the card.
 *
 * Props:
 * - `title` (String, required): The title of the track.
 * - `artist` (String, required): The name of the artist.
 * - `coverImage` (String, optional): The URL of the track's cover image.
 * - `link` (String, optional): The URL to the track's external page.
 * - `label` (Boolean, optional): Whether to display the "Recently Listened to" label.
 *
 * Dependencies:
 * - Custom UI components: Card, CardTitle, CardHeader, CardDescription, CardContent, CardFooter.
 * - PeopleWatching.vue: A fallback icon for when no cover image is provided.
 */

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
        required: false, // The link to the track's external page is optional
        default: ""
    },
    label: {
        type: Boolean,
        default: true, // Whether to display the label is optional
        required: false,
    }
});
</script>

<template>
    <div>
        <!-- Link to the track's external page -->
        <a :href="link">
            <Card>
                <!-- Card header with optional label -->
                <CardHeader>
                    <CardTitle v-if="label">
                        Recently Listened to
                    </CardTitle>
                </CardHeader>
                <!-- Card content displaying track details -->
                <CardContent class="flex flex-row items-center">
                    <!-- Display the cover image if provided -->
                    <img v-if="coverImage" :src="coverImage" alt="Cover Art"
                        class="w-16 h-16 rounded-md object-cover" />
                    <!-- Fallback icon if no cover image is provided -->
                    <PeopleWatching v-else />
                    <div class="ml-4">
                        <!-- Display the track title -->
                        <p class="font-bold">{{ title }}</p>
                        <!-- Display the artist name -->
                        <CardDescription>{{ artist }}</CardDescription>
                    </div>
                </CardContent>
                <!-- Optional footer (currently unused) -->
                <CardFooter v-if="!label"></CardFooter>
            </Card>
        </a>
    </div>
</template>