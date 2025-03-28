<script lang="ts" setup>
/**
 * SongCard.vue
 *
 * A component for displaying a song card with track details.
 *
 * Features:
 * - Displays the track title, artist name, and cover image.
 * - Provides a clickable card that links to the track's external page.
 * - Includes a fallback icon for the cover image if not provided.
 *
 * Props:
 * - `title` (String, required): The title of the track.
 * - `artist` (String, required): The name of the artist(s).
 * - `coverImage` (String, required): The URL of the track's cover image.
 * - `link` (String, required): The URL to the track's external page.
 *
 * Dependencies:
 * - Custom UI components: Card, CardHeader, CardContent, CardDescription.
 * - PeopleWatching.vue: A fallback icon for when no cover image is provided.
 */

import { Card, CardHeader, CardDescription, CardContent } from "@/components/ui/card";
import PeopleWatching from "./images/PeopleWatching.vue";
import { defineProps } from "vue";

// Define props for the component
interface Props {
    title: string;
    artist: string;
    coverImage: string;
    link: string;
}

const props = defineProps<Props>();
</script>

<template>
    <div>
        <!-- Link to the track's external page -->
        <a :href="props.link" target="_blank" rel="noopener noreferrer">
            <Card>
                <!-- Card header (currently unused, can be extended) -->
                <CardHeader></CardHeader>

                <!-- Card content displaying track details -->
                <CardContent class="flex flex-row items-center">
                    <!-- Display the cover image if provided -->
                    <img v-if="props.coverImage" :src="props.coverImage" alt="Cover"
                        class="w-16 h-16 rounded-md object-cover" />
                    <!-- Fallback icon if no cover image is provided -->
                    <PeopleWatching v-else class="w-16 h-16" />
                    <div class="ml-4">
                        <!-- Display the track title -->
                        <p class="font-bold">{{ props.title }}</p>
                        <!-- Display the artist name -->
                        <CardDescription>{{ props.artist }}</CardDescription>
                    </div>
                </CardContent>
            </Card>
        </a>
    </div>
</template>