<script lang="ts" setup>
/**
 * PlaylistCard.vue
 *
 * A component for displaying a playlist card with track details and additional options in a dialog.
 *
 * Features:
 * - Displays the track title, artist name, and cover image.
 * - Provides a clickable card that opens a dialog for additional options.
 * - Includes a link to the track's external page.
 *
 * Props:
 * - `title` (String, required): The title of the track.
 * - `artist` (String, required): The name of the artist(s).
 * - `coverImage` (String, required): The URL of the track's cover image.
 * - `link` (String, required): The URL to the track's external page.
 *
 * Dependencies:
 * - SongCard: A reusable component for displaying track details.
 * - Dialog: A UI component for displaying additional options in a modal.
 */

import SongCard from './SongCard.vue';
import { Dialog, DialogContent, DialogHeader, DialogTrigger } from './ui/dialog';
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
    <Dialog>
        <!-- Trigger for opening the dialog -->
        <DialogTrigger asChild>
            <!-- Display the track details using the SongCard component -->
            <SongCard :title="props.title" :artist="props.artist" :coverImage="props.coverImage" :link="props.link" />
        </DialogTrigger>

        <!-- Dialog content -->
        <DialogContent>
            <DialogHeader>
                <!-- Placeholder for additional dialog content -->
                TEST
            </DialogHeader>
        </DialogContent>
    </Dialog>
</template>