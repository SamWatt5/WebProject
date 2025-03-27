<script lang="ts" setup>
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import PlaylistCard from '@/components/PlaylistCard.vue';
import { toast } from 'vue-sonner';

// Extra imports for the friends components
import UserCard from '@/components/UserCard.vue';
import { Avatar } from '@/components/ui/avatar';
import { useFriends } from '@/stores/friends';
import { storeToRefs } from 'pinia';
import { ref, onMounted } from "vue";


const music = ref<string[]>([]); // Reactive array to store music tracks
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

// Using the friends store to get and set friends data
const store = useFriends();
const { friends } = storeToRefs(store);
// Define the structure of a track based on the response
interface Track {
    id: string;
    trackTitle: string;
    href: string;
    artists: { href: string; name: string }[];
    cover: string;
}

const friendId = ref(""); // Input for friend's ID
const recommendations = ref<Track[]>([]); // Store recommendations
const errorMessage = ref(""); // Store error messages
const successMessage = ref(""); // Store success messages
const isPlaylistCreated = ref(false)


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
        // Map the response to match the Track interface
        recommendations.value = data.playlist.map((track: any) => ({
            id: track.id,
            trackTitle: track.title,
            href: track.link,
            artists: [{ href: "", name: track.artist }], // Assuming a single artist for simplicity
            cover: track.cover
        }));
    } catch (error) {
        errorMessage.value = "An error occurred while fetching the blended playlist.";
        console.error(error);
    }
}

const createPlaylist = async () => {
    errorMessage.value = "";
    successMessage.value = "";

    // Extract the track IDs from the recommendations
    const trackIds = recommendations.value.map((track) => track.id);

    try {
        const response = await fetch("/api/spotify/create_playlist", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ track_ids: trackIds }), // Send track IDs in the request body
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

const redirectToSpotifyLogin = () => {
    window.location.href = "/api/spotify/login"; // Redirect to Spotify login endpoint
};

// Fetch top tracks when the component is mounted
onMounted(() => {
    fetchTopTracks();
});
</script>

<template>
    <!-- Left side -->
    <div class="flex flex-row">
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <div class="flex flex-col ml-10">
                <ScrollArea class="w-80 h-[75vh] border rounded-lg">
                    <div class="p-4">
                        <div v-for="(song, index) in music" :key="index">
                            <div class="flex items-center">
                                <span class="font-bold mr-2">{{ index + 1 }}.</span> <!-- Display the rank -->
                                <span>{{ song }}</span> <!-- Display the track name -->
                            </div>
                            <Separator class="my-2" />
                        </div>
                    </div>
                </ScrollArea>
            </div>
            <Separator orientation="vertical" class="mx-10" />
        </main>

        <!-- Choose friend area to display their playlist -->
        <ScrollArea class="border rounded-md min-w-[500px] h-[100vh] p-4 flex-grow pt-10">
            <div class="flex flex-col gap-4">
                <div v-for="(friend, index) in friends" :key="index" class="flex-grow">
                    <Card class="cursor-pointer">
                        <CardHeader class="flex flex-row">
                            <Avatar class="w-20 h-20 mt-2">
                                <AvatarFallback class="text-3xl">{{ (friend.first_name[0] + friend.last_name[0]) }}
                                </AvatarFallback>
                            </Avatar>
                            <div class="flex flex-col pl-3">
                                <CardTitle class="text-4xl">@{{ friend.username }}</CardTitle>
                                <CardDescription class="flex flex-row">
                                    <CalendarDays class="h-8 w-8 mt-1" /><span class="mt-[3px] text-lg ml-1"> Joined
                                        December 991</span>
                                </CardDescription>
                                <!-- <<RouterLink as-child :href="`https://open.spotify.com/user/${name}`">
                <Spotify class="mt-2 cursor-pointer" />
            </RouterLink>> -->
                                <div class="flex flex-row justify-between mt-2">
                                    <a :href="`https://open.spotify.com/user/${friend.spotify_id}`" target="_blank">
                                        <Spotify class="cursor-pointer mt-2" />
                                    </a>
                                    <DialogTrigger as-child>
                                        <Button class="mt-2" @click="() => {
                                            friendId = friend._id || '';
                                            fetchBlend();
                                        }">
                                            MixPlaylists
                                        </Button>
                                    </DialogTrigger>
                                </div>
                            </div>
                        </CardHeader>
                    </Card>
                </div>
            </div>
            <!-- Displaying a message when there are no friends -->
            <div class="flex flex-col gap-4" v-if="friends.length === 0">
                <UserCard :name="'No friends'" :avatar="'NA'" :joined="'Never'" />
            </div>
        </ScrollArea>

        <div class="flex flex-col w-full min-w-[500px] pt-10 gap-4 mr-4 ml-4">
            <Card class="w-full">
                <CardHeader class="w-full">
                    <CardTitle class="text-4xl text-center">Playlists</CardTitle>
                    <CardDescription></CardDescription>
                </CardHeader>
                <CardContent>
                    <button v-if="recommendations.length > 0 && !isPlaylistCreated" @click="createPlaylist"
                        class="bg-green-500 text-white px-4 py-2 rounded mb-4 mx-auto block">
                        Create Playlist
                    </button>
                    <button v-if="isPlaylistCreated" @click=""
                        class="bg-green-500 text-white px-4 py-2 rounded mb-4 mx-auto block">
                        Playlist Created Successfully!
                    </button>
                    <div v-if="errorMessage" class="text-red-500 text-center mb-4">
                        {{ errorMessage }}
                    </div>
                    <ScrollArea class="h-[80vh]">
                        <div v-for="(track, index) in recommendations" :key="index">
                            <PlaylistCard :title="track.trackTitle"
                                :artist="track.artists.map(artist => artist.name).join(', ')"
                                :coverImage="track.cover" />
                        </div>
                        <ScrollBar />
                    </ScrollArea>
                </CardContent>
            </Card>
        </div>
    </div>
</template>