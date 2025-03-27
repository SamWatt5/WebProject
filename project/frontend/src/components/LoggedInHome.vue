<script setup lang="ts">
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Card, CardDescription, CardTitle, CardHeader, CardContent } from '@/components/ui/card';
import { CalendarDays } from "lucide-vue-next";
import UserCard from './UserCard.vue';
import ListeningToCard from './ListeningToCard.vue';
import { useUser } from '@/stores/user';
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from './MobileSidebar.vue';
import { ref, onMounted } from 'vue';

const music = ref<string[]>([]); // Reactive array to store music tracks
const { user } = useUser();

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

// Fetch top tracks when the component is mounted
onMounted(() => {
    fetchTopTracks();
});
</script>

<template>
    <div class="flex flex-row">
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
            <MobileSidebar v-else />

            <div class="flex flex-col ml-10">
                <h1 class="text-4xl text-center mb-4">Your Music</h1>
                <ScrollArea class="w-80 h-[75vh] border rounded-lg">
                    <div class="p-4">
                        <div v-for="song in music" :key="song">
                            {{ song }}
                            <Separator class="my-2" />
                        </div>
                    </div>
                </ScrollArea>
            </div>
            <Separator orientation="vertical" class="mx-10" />
        </main>
        <div class="grid grid-cols-3 pt-10 gap-4">
            <div class="w-full">
                <UserCard :spotify_id="user?.spotify_id" :name="user?.username ?? 'Guest'" :avatar="(user?.first_name?.substring(0, 1) ?? '') + (user?.last_name?.substring(0, 1) ?? '')" joined="January 2021" />
            </div>
            <div class="w-full col-span-3">
                <ListeningToCard class="w-1/3" />

                <ScrollArea class="border rounded-md col-span-3 w-[95%] mt-4 whitespace-nowrap">
                    <div class="flex p-4 space-x-4 w-max">
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                        <ListeningToCard />
                    </div>
                    <ScrollBar orientation="horizontal" />
                </ScrollArea>
            </div>
        </div>
    </div>
</template>