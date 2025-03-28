<script lang="ts" setup>
/**
 * FriendsView.vue
 *
 * A component for managing and viewing the user's friends and their top tracks.
 *
 * Features:
 * - Displays the user's top tracks in a scrollable list.
 * - Allows users to search for and manage their friends.
 * - Provides a sidebar for navigation and a mobile-friendly sidebar alternative.
 * - Displays a list of friends with options to manage each friend.
 * - Shows a message if the user has no friends.
 *
 * Dependencies:
 * - Pinia: For state management (user and friends stores).
 * - Custom UI components: Sidebar, ScrollArea, Separator, Card, Button, Input, FriendManage, FriendSearch.
 * - Vue composables: `onMounted`, `ref`.
 *
 * State:
 * - `music` (ref<string[]>): Stores the user's top tracks.
 * - `user` (ref<User | null>): Stores the current user's information.
 * - `friends` (ref<User[]>): Stores the list of the user's friends.
 * - `isLoading` (ref<boolean>): Indicates whether the user and friends data is being loaded.
 *
 * Methods:
 * - `fetchTopTracks()`: Fetches the user's top tracks from the API.
 * - `refresh()`: Refreshes the user and friends data from the API.
 */

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
import MobileSidebar from '@/components/MobileSidebar.vue';
import { useIsMobile } from '@/hooks/use-mobile';
import router from '@/router';

// Reactive array to store the user's top tracks
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

// Access the user store
let { user, setUser } = useUser();

// Access the friends store
let store = useFriends();
const { friends } = storeToRefs(store);
const { setFriends } = store;

// Ref to track loading state
const isLoading = ref(true);

// Display a loading toast message
toast.loading("Loading user data...", {
    duration: Infinity,
    id: "loading-data",
    dismissible: false
});

/**
 * Refreshes the user and friends data from the API.
 *
 * Updates the `user` and `friends` state with the fetched data.
 */
const refresh = async () => {
    try {
        // Fetch user data
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

            // Fetch friends data
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

// Fetch user and friends data when the component is mounted
onMounted(async () => {
    refresh();

    if (!user) {
        router.push("/login");
    }
});

// Fetch top tracks when the component is mounted
onMounted(() => {
    fetchTopTracks();
});
</script>

<template>
    <div class="flex flex-row">
        <!-- Sidebar -->
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <MobileSidebar v-else />

            <!-- Top tracks section -->
            <div class="sm:flex flex-col hidden ml-10">
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

        <!-- Friends management section -->
        <div class="flex flex-col pt-10 gap-4 mr-4 flex-1">
            <Card class="mt-4 overflow-hidden">
                <CardHeader>
                    <CardTitle class="text-4xl">Friends</CardTitle>
                    <CardDescription>Here is some management settings for friends</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="flex flex-row items-center">
                        <FriendSearch />
                    </div>
                </CardContent>
            </Card>

            <!-- Friends list -->
            <ScrollArea class="border rounded-md whitespace-nowrap h-[60vh] p-4">
                <div class="grid sm:grid-cols-2 grid-cols-1 grid-flow-row gap-4 w-full">
                    <div v-for="(friend, index) in friends" :key="index">
                        <FriendManage :spotify_id="friend.spotify_id" :userName="friend.username"
                            :userAvatar="friend.first_name?.[0] + friend.last_name?.[0]" />
                    </div>
                </div>
                <div class="flex align-center justify-center" v-if="friends.length === 0">
                    <h1 class="text-3xl">
                        It appears you have <span class="text-red-500 font-bold">0</span> friends. Unlucky "mate"
                    </h1>
                </div>
            </ScrollArea>
        </div>
    </div>
</template>