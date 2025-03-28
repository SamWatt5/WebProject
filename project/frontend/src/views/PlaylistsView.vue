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
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from '@/components/MobileSidebar.vue';
import { useUser } from '@/stores/user';
import { Button } from '@/components/ui/button';
import Spotify from '@/components/icons/Spotify.vue';
import CardFooter from '@/components/ui/card/CardFooter.vue';
import router from '@/router';


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

// Displaying a loading toast message
toast.loading("Loading user data...", {
    duration: Infinity,
    id: "loading-data",
    dismissible: false
});



// Using the user store to get and set user data
let { user, setUser } = useUser();

const { setFriends } = store;
// Ref to track loading state
const isLoading = ref(true);

// Function to refresh user and friends data
const refresh = async () => {
    try {
        // Fetching user data from the API
        const res = await fetch("/api/user/me", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await res.json();

        if (!data.error) {
            // Setting user data
            setUser(data);
            user = data;
            // Fetching friends data for each friend
            for (let friend of data.friends) {
                const res = await fetch(`/api/user/find/${friend}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const friendData = await res.json();
                if (!friendData.error) {
                    // Adding friend data to the friends list
                    if (friends.value.length == data.friends.length) {
                        toast.dismiss("loading-data");
                        isLoading.value = false;
                        return;
                    };
                    setFriends([...friends.value, friendData]);
                }
            }
        }

        // Updating loading state and dismissing the toast
        isLoading.value = false;
        toast.dismiss("loading-data");
    } catch (err) {
        console.error(err);
    }
}

// Calling the refresh function when the component is mounted
onMounted(async () => {
    refresh();
});


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
    if(!user) {
        router.push('/login');
    }
});
</script>

<template>
    <!-- Left side -->
    <div class="flex flex-col sm:flex-row">
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <MobileSidebar v-else />

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

        <!-- Choose friend area to display their playlist -->
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
                                <CardDescription class="flex flex-row">

                                </CardDescription>
                                <!-- <<RouterLink as-child :href="`https://open.spotify.com/user/${name}`">
                <Spotify class="mt-2 cursor-pointer" />
            </RouterLink>> -->
                            </div>
                        </CardHeader>
                        <CardFooter class="flex flex-row justify-between mt-2">
                            <a :href="`https://open.spotify.com/user/${friend.spotify_id}`" target="_blank">
                                <Spotify class="cursor-pointer mt-2" />
                            </a>
                            <Button class="mt-2" @click="() => {
                                friendId = friend._id || '';
                                fetchBlend();
                            }">
                                MixPlaylists
                            </Button>
                        </CardFooter>
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