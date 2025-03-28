<script lang="ts" setup>
/**
 * PlaylistsView.vue
 *
 * A component for managing and creating playlists, as well as blending playlists with friends.
 *
 * Features:
 * - Displays the user's top tracks in a scrollable list.
 * - Allows users to blend playlists with their friends.
 * - Provides options to create a new playlist from blended recommendations.
 * - Displays a list of friends with options to blend playlists.
 * - Shows a message if the user has no friends.
 * - Includes a sidebar for navigation and a mobile-friendly sidebar alternative.
 *
 * Dependencies:
 * - Pinia: For state management (user and friends stores).
 * - Custom UI components: Sidebar, ScrollArea, Separator, Card, Button, PlaylistCard, UserCard.
 * - Vue composables: `onMounted`, `ref`.
 * - vue-sonner: For toast notifications.
 *
 * State:
 * - `music` (ref<string[]>): Stores the user's top tracks.
 * - `friends` (ref<User[]>): Stores the list of the user's friends.
 * - `recommendations` (ref<Track[]>): Stores the blended playlist recommendations.
 * - `friendId` (ref<string>): Stores the selected friend's ID for blending playlists.
 * - `errorMessage` (ref<string>): Stores error messages for API calls.
 * - `successMessage` (ref<string>): Stores success messages for API calls.
 * - `isPlaylistCreated` (ref<boolean>): Indicates whether a playlist has been successfully created.
 * - `isLoading` (ref<boolean>): Indicates whether the user and friends data is being loaded.
 *
 * Methods:
 * - `fetchTopTracks()`: Fetches the user's top tracks from the API.
 * - `refresh()`: Refreshes the user and friends data from the API.
 * - `fetchBlend()`: Fetches a blended playlist with a selected friend.
 * - `createPlaylist()`: Creates a new playlist from the blended recommendations.
 */

import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Separator } from '@/components/ui/separator';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import PlaylistCard from '@/components/PlaylistCard.vue';
import { toast } from 'vue-sonner';
import UserCard from '@/components/UserCard.vue';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { useFriends } from '@/stores/friends';
import { storeToRefs } from 'pinia';
import { ref, onMounted } from "vue";
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from '@/components/MobileSidebar.vue';
import { useUser } from '@/stores/user';
import { Button } from '@/components/ui/button';
import Spotify from '@/components/icons/Spotify.vue';
import CardFooter from '@/components/ui/card/CardFooter.vue';
import router from '@/router';

// Reactive state variables
const music = ref<string[]>([]); // Stores the user's top tracks
const recommendations = ref<Track[]>([]); // Stores blended playlist recommendations
const friendId = ref(""); // Stores the selected friend's ID
const errorMessage = ref(""); // Stores error messages
const successMessage = ref(""); // Stores success messages
const isPlaylistCreated = ref(false); // Indicates if a playlist has been created
const isLoading = ref(true); // Tracks loading state

// Access the user and friends stores
let { user, setUser } = useUser();
const store = useFriends();
const { friends } = storeToRefs(store);
const { setFriends } = store;

// Display a loading toast message
toast.loading("Loading user data...", {
    duration: Infinity,
    id: "loading-data",
    dismissible: false
});

/**
 * Fetches the user's top tracks from the API.
 */
const fetchTopTracks = async () => {
    try {
        const response = await fetch('/api/spotify/top-tracks', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error('Failed to fetch top tracks:', response.statusText);
            return;
        }

        const data = await response.json();
        music.value = data.tracks.map((track: any) => track.name);
    } catch (error) {
        console.error('Error fetching top tracks:', error);
    }
};

/**
 * Refreshes the user and friends data from the API.
 */
const refresh = async () => {
    try {
        const res = await fetch("/api/user/me", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await res.json();

        if (!data.error) {
            setUser(data);
            user = data;

            for (let friend of data.friends) {
                const res = await fetch(`/api/user/find/${friend}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const friendData = await res.json();
                if (!friendData.error) {
                    if (friends.value.length === data.friends.length) {
                        toast.dismiss("loading-data");
                        isLoading.value = false;
                        return;
                    }
                    setFriends([...friends.value, friendData]);
                }
            }
        }

        isLoading.value = false;
        toast.dismiss("loading-data");
    } catch (err) {
        console.error(err);
    }
};

/**
 * Fetches a blended playlist with a selected friend.
 */
const fetchBlend = async () => {
    errorMessage.value = "";
    successMessage.value = "";
    recommendations.value = [];
    isPlaylistCreated.value = false;

    try {
        toast.loading('Loading blended playlist...', {
            id: 'loadingMessage',
            dismissible: false
        });

        const response = await fetch(
            `/api/spotify/blend?friend_id=${friendId.value}`,
            {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if (!response.ok) {
            const errorData = await response.json();
            errorMessage.value = errorData.error || "Failed to fetch blended playlist.";
            toast.error('Update failed', {
                duration: 5000,
                id: 'loadingMessage'
            });
        } else {
            toast.success('Playlists Blended', {
                duration: 5000,
                id: 'loadingMessage'
            });
        }

        const data = await response.json();
        recommendations.value = data.playlist.map((track: any) => ({
            id: track.id,
            trackTitle: track.title,
            href: track.link,
            artists: [{ href: "", name: track.artist }],
            cover: track.cover
        }));
    } catch (error) {
        errorMessage.value = "An error occurred while fetching the blended playlist.";
        console.error(error);
    }
};

/**
 * Creates a new playlist from the blended recommendations.
 */
const createPlaylist = async () => {
    errorMessage.value = "";
    successMessage.value = "";

    const trackIds = recommendations.value.map((track) => track.id);

    try {
        const response = await fetch("/api/spotify/create_playlist", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ track_ids: trackIds }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            errorMessage.value = errorData.error || "Failed to create playlist.";
            return;
        }

        successMessage.value = "Playlist created successfully!";
        isPlaylistCreated.value = true;
    } catch (error) {
        errorMessage.value = "An error occurred while creating the playlist.";
        console.error(error);
    }
};

// Fetch user and friends data on component mount
onMounted(() => {
    refresh();
    fetchTopTracks();
    if (!user) {
        router.push('/login');
    }
});
</script>

<template>
    <div class="flex flex-col sm:flex-row">
        <!-- Sidebar -->
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <MobileSidebar v-else />

            <!-- Top tracks section -->
            <div class="hidden sm:flex flex-col ml-10">
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

        <!-- Friends and playlists section -->
        <ScrollArea
            class="border sm:translate-y-0 -translate-y-[90%] rounded-md min-w-[500px] h-[100vh] p-4 flex-grow pt-10">
            <div class="flex flex-col gap-4">
                <div v-for="(friend, index) in friends" :key="index" class="flex-grow">
                    <Card>
                        <CardHeader class="flex flex-row">
                            <Avatar class="w-20 h-20 mt-2">
                                <AvatarFallback class="text-3xl">{{ (friend.first_name[0] + friend.last_name[0]) }}
                                </AvatarFallback>
                            </Avatar>
                            <div class="flex flex-col pl-3">
                                <CardTitle class="text-4xl">@{{ friend.username }}</CardTitle>
                            </div>
                        </CardHeader>
                        <CardFooter class="flex flex-row justify-between mt-2">
                            <a :href="`https://open.spotify.com/user/${friend.spotify_id}`" target="_blank">
                                <Spotify class="cursor-pointer mt-2" />
                            </a>
                            <Button class="mt-2" @click="() => { friendId.value = friend._id || ''; fetchBlend(); }">
                                MixPlaylists
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            </div>
            <div class="flex flex-col gap-4" v-if="friends.length === 0">
                <UserCard :name="'No friends'" :avatar="'NA'" :joined="'Never'" :spotify_id="'N/A'" />
            </div>
        </ScrollArea>

        <!-- Playlist recommendations -->
        <div class="flex flex-col w-full min-w-[500px] pt-10 gap-4 mr-4 ml-4">
            <Card class="w-full">
                <CardHeader class="w-full">
                    <CardTitle class="text-4xl text-center">Playlists</CardTitle>
                </CardHeader>
                <CardContent>
                    <button v-if="recommendations.length > 0 && !isPlaylistCreated" @click="createPlaylist"
                        class="bg-green-500 text-white px-4 py-2 rounded mb-4 mx-auto block">
                        Create Playlist
                    </button>
                    <button v-if="isPlaylistCreated"
                        class="bg-green-500 text-white px-4 py-2 rounded mb-4 mx-auto block">
                        Playlist Created Successfully!
                    </button>
                    <div v-if="errorMessage" class="text-red-500 text-center mb-4">
                        {{ errorMessage }}
                    </div>
                    <ScrollArea class="h-[80vh]">
                        <div v-for="(track, index) in recommendations" :key="index">
                            <PlaylistCard :title="track.trackTitle"
                                :artist="track.artists.map(artist => artist.name).join(', ')" :coverImage="track.cover"
                                :link="track.href" />
                        </div>
                        <ScrollBar />
                    </ScrollArea>
                </CardContent>
            </Card>
        </div>
    </div>
</template>