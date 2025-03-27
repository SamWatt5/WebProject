<script lang="ts" setup>
// Importing necessary components and libraries
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Card, CardHeader, CardDescription, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import FriendManage from '@/components/FriendManage.vue';
import { onMounted, ref } from 'vue';
import { useUser, type User } from '@/stores/user';
import { toast } from 'vue-sonner';
import { useFriends } from '@/stores/friends';
import FriendSearch from '@/components/FriendSearch.vue';
import { storeToRefs } from 'pinia';
import UserCard from '@/components/UserCard.vue';
import MobileSidebar from '@/components/MobileSidebar.vue';
import { useIsMobile } from '@/hooks/use-mobile';


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

// Using the user store to get and set user data
let { user, setUser } = useUser();
// Using the friends store to get and set friends data
let store = useFriends();
const { friends } = storeToRefs(store);
const { setFriends } = store;
// Ref to track loading state
const isLoading = ref(true);

// Displaying a loading toast message
toast.loading("Loading user data...", {
    duration: Infinity,
    id: "loading-data",
    dismissible: false
});

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

// Fetch top tracks when the component is mounted
onMounted(() => {
    fetchTopTracks();
});
</script>

<template>
    <div class="flex flex-row">
        <main class="flex h-screen items-center place-self-start">
            <!-- Sidebar component -->
            <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <MobileSidebar v-else />
            <div class="sm:flex flex-col hidden ml-10">
                <h1 class="text-4xl text-center mb-4">Your Music</h1>
                <!-- Scroll area for displaying the list of songs -->
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
            <Separator orientation="vertical" class="hidden sm:inline mx-10" />
        </main>
        <div class="flex flex-col pt-10 gap-4 mr-4 flex-1">
            <!-- Card component for managing friends -->
            <Card class="mt-4 overflow-hidden">
                <CardHeader>
                    <CardTitle class="text-4xl">Friends</CardTitle>
                    <CardDescription>Here is some management settings for friends</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="flex flex-row items-center">
                        <!-- Friend search component -->
                        <FriendSearch />
                    </div>
                </CardContent>
                <CardFooter>
                    <!-- <CardDescription>To manage a friend, just click on their tile</CardDescription> -->
                </CardFooter>
            </Card>
            <!-- Scroll area for displaying the list of friends -->
            <ScrollArea class="border rounded-md whitespace-nowrap h-[60vh] p-4">
                <div class="grid sm:grid-cols-2 grid-cols-1 grid-flow-row gap-4 w-full">
                    <div v-for="(friend, index) in friends" :key="index">
                        <!-- Friend manage component for each friend -->
                        <FriendManage :spotify_id="friend.spotify_id" :userName="friend.username"
                            :userAvatar="friend.first_name?.[0] + friend.last_name?.[0]"" />
                    </div>
                </div>
                <!-- Displaying a message when there are no friends -->
                <div class=" grid grid-cols-3 grid-flow-row gap-4" v-if="friends.length === 0">
                            <UserCard :name="'No friends'" :avatar="'NA'" :joined="'Never'" />
                    </div>
            </ScrollArea>
        </div>
    </div>
</template>