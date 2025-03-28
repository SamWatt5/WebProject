<script setup lang="ts">
/**
 * LoggedInHome.vue
 *
 * A component for displaying the logged-in user's home page, including their music data.
 *
 * Features:
 * - Displays the user's top tracks and recently played tracks.
 * - Shows a personalized greeting with the user's username.
 * - Includes a sidebar for navigation and a mobile-friendly sidebar alternative.
 * - Uses `ListeningToCard` to display track details.
 * - Fetches data from the backend API for top tracks and recently played tracks.
 *
 * Dependencies:
 * - Pinia: For state management (user store).
 * - Custom UI components: Sidebar, ScrollArea, Separator, Card, ListeningToCard.
 * - Vue composables: `onMounted`, `ref`.
 *
 * State:
 * - `recentlyPlayed` (ref<RecentlyPlayedTrack[]>): Stores recently played tracks.
 * - `music` (ref<string[]>): Stores the user's top tracks.
 *
 * Methods:
 * - `fetchTopTracks()`: Fetches the user's top tracks from the API.
 * - `fetchRecentlyPlayed()`: Fetches the user's recently played tracks from the API.
 */

import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import ListeningToCard from './ListeningToCard.vue';
import { useUser } from '@/stores/user';
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from './MobileSidebar.vue';
import { ref, onMounted } from 'vue';

// Define the structure of a recently played track
interface RecentlyPlayedTrack {
    title: string;
    artist: string;
    coverImage: string;
    link: string;
}

// Reactive array to store recently played tracks
const recentlyPlayed = ref<RecentlyPlayedTrack[]>([]);

// Reactive array to store top tracks
const music = ref<string[]>([]);

/**
 * Fetches the user's top tracks from the API.
 *
 * Updates the `music` array with the track names.
 */
const fetchTopTracks = async () => {
    try {
        const response = await fetch('/api/spotify/top-tracks', {
            method: 'GET',
            credentials: 'include', // Include cookies for authentication
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error('Failed to fetch top tracks:', response.statusText);
            return;
        }

        const data = await response.json();
        // Map the response to extract track names
        music.value = data.tracks.map((track: any) => track.name);
    } catch (error) {
        console.error('Error fetching top tracks:', error);
    }
};

/**
 * Fetches the user's recently played tracks from the API.
 *
 * Updates the `recentlyPlayed` array with track details.
 */
const fetchRecentlyPlayed = async () => {
    try {
        const response = await fetch('/api/spotify/recently-played', {
            method: 'GET',
            credentials: 'include', // Include cookies for authentication
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error('Failed to fetch recently played tracks:', response.statusText);
            return;
        }

        const data = await response.json();
        // Map the response to extract relevant details
        recentlyPlayed.value = data.recently_played.map((track: any) => ({
            title: track.name, // Match the prop name expected by ListeningToCard
            artist: track.artist,
            coverImage: track.cover_art, // Match the prop name expected by ListeningToCard
            link: track.link || '', // Optional link to the track
        }));
        console.log('Recently played tracks:', recentlyPlayed.value);
    } catch (error) {
        console.error('Error fetching recently played tracks:', error);
    }
};

// Access the user store
const { user } = useUser();

// Fetch data when the component is mounted
onMounted(() => {
    fetchTopTracks();
    fetchRecentlyPlayed();
});
</script>

<template>
    <div class="flex flex-row">
        <!-- Sidebar for navigation -->
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <MobileSidebar v-else />

            <!-- Top tracks section -->
            <div class="sm:flex hidden flex-col ml-10">
                <h1 class="text-4xl text-center mb-4">Your Music</h1>
                <ScrollArea class="w-80 h-[75vh] border rounded-lg">
                    <div class="p-4">
                        <div v-for="(song, index) in music" :key="index">
                            <div class="flex items-center">
                                <span class="font-bold mr-2">{{ index + 1 }}.</span>
                                <span>{{ song }}</span>
                            </div>
                            <Separator class="my-2" />
                        </div>
                    </div>
                </ScrollArea>
            </div>
            <Separator orientation="vertical" class="hidden sm:inline mx-10" />
        </main>

        <!-- Recently played tracks section -->
        <div class="grid grid-cols-3 pt-10 gap-4">
            <div class="flex flex-col sm:flex-row col-span-3 w-full justify-between">
                <!-- User profile image -->
                <div class="mx-12">
                    <img src="/TrackMates.png" class="rounded-full h-[300px] w-[300px] hover:animate-spin col-span-2" />
                </div>

                <!-- Greeting card -->
                <Card class="flex-1 mr-4">
                    <CardHeader>
                        <CardTitle class="text-4xl">
                            Hey, @<span class="text-cyan-500 font-semibold">{{ user?.username }}</span>
                        </CardTitle>
                    </CardHeader>
                    <CardContent class="flex flex-col space-y-1">
                        <div class="flex flex-row">
                            You've listened to <span class="font-semibold inline">&nbsp;{{ recentlyPlayed.length }}
                            </span>&nbsp;tracks recently. Your most recent song is:
                        </div>
                        <ListeningToCard v-if="recentlyPlayed[0]" :title="recentlyPlayed[0]?.title"
                            :artist="recentlyPlayed[0]?.artist" :cover-image="recentlyPlayed[0]?.coverImage"
                            :link="recentlyPlayed[0].link" :label="false" />
                    </CardContent>
                </Card>
            </div>

            <!-- Scrollable list of recently played tracks -->
            <div class="w-full col-span-3 flex flex-col h-full mb-12">
                <ScrollArea class="border rounded-md col-span-3 w-[95%] mb-12 whitespace-nowrap mt-auto">
                    <div class="flex p-4 space-x-4 w-max mt-auto">
                        <ListeningToCard v-for="(track, index) in recentlyPlayed" :key="index" :title="track.title"
                            :artist="track.artist" :coverImage="track.coverImage" :link="track.link" />
                    </div>
                    <ScrollBar orientation="horizontal" />
                </ScrollArea>
            </div>
        </div>
    </div>
</template>