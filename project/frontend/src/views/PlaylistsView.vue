<script lang="ts" setup>
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import PlaylistCard from '@/components/PlaylistCard.vue';

// Extra imports for the friends components
import FriendManage from '@/components/FriendManage.vue';
import UserCard from '@/components/UserCard.vue';
import { useFriends } from '@/stores/friends';
import { storeToRefs } from 'pinia';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

// Using the friends store to get and set friends data
const store = useFriends();
const { friends } = storeToRefs(store);

</script>

<template>
    <div class="flex flex-row">
        <main class="flex h-screen items-center place-self-start">
            <SidebarProvider :default-open="false" :open="false">
                <Sidebar />
            </SidebarProvider>
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
            
            <!-- Choose friend area to display their playlist -->
            <ScrollArea class="border rounded-md whitespace-nowrap h-[60vh] p-4">
                <div class="grid grid-cols-3 grid-flow-row gap-4">
                    <div v-for="(friend, index) in friends" :key="index">
                        <!-- Friend manage component for each friend -->
                        <FriendManage :userName="friend.username" :userAvatar="friend.first_name?.[0] + friend.last_name?.[0]" :userJoined="'December 2021'" />
                    </div>
                </div>
                <!-- Displaying a message when there are no friends -->
                <div class="grid grid-cols-3 grid-flow-row gap-4" v-if="friends.length === 0">
                    <UserCard :name="'No friends'" :avatar="'NA'" :joined="'Never'" />
                </div>
            </ScrollArea>

        </main>
        <div class="flex flex-col w-full pt-10 gap-4 mr-4">
            <Card class="w-full">
                <CardHeader>
                    <CardTitle class="text-4xl">Playlists</CardTitle>
                    <CardDescription></CardDescription>
                </CardHeader>
                <CardContent>
                    <ScrollArea class="h-[80vh]">
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <PlaylistCard />
                        <ScrollBar />
                    </ScrollArea>
                </CardContent>
            </Card>
        </div>
    </div>
</template>