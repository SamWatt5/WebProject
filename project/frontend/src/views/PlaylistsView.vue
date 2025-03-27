<script lang="ts" setup>
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import PlaylistCard from '@/components/PlaylistCard.vue';

// Extra imports for the friends components
import FriendCreate from '@/components/FriendCreate.vue';
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
    <!-- Left side -->
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
        </main>

        <!-- Choose friend area to display their playlist -->
        <ScrollArea class="border rounded-md min-w-[500px] h-[100vh] p-4 flex-grow pt-10">
            <div class="flex flex-col gap-4">
                <div v-for="(friend, index) in friends" :key="index" class="flex-grow">
                    <!-- Friend manage component for each friend -->
                    <!-- <FriendCreate :userName="friend.username" :userAvatar="friend.first_name?.[0] + friend.last_name?.[0]" :userJoined="'December 2021'" /> -->
                    <Card class="cursor-pointer">
                <CardHeader class="flex flex-row">
                    <Avatar class="w-20 h-20 mt-2">
                        <AvatarFallback class="text-3xl">{{ (friend.first_name[0] + friend.last_name[0]) }}</AvatarFallback>
                    </Avatar>
                    <div class="flex flex-col pl-3">
                        <CardTitle class="text-4xl">@{{ friend.username }}</CardTitle>
                        <CardDescription class="flex flex-row">
                            <CalendarDays class="h-8 w-8 mt-1" /><span class="mt-[3px] text-lg ml-1"> Joined December 991</span>
                        </CardDescription>
                        <!-- <<RouterLink as-child :href="`https://open.spotify.com/user/${name}`">
                <Spotify class="mt-2 cursor-pointer" />
            </RouterLink>> -->
                       <div class="flex flex-row justify-between mt-2">
                        <a :href="`https://open.spotify.com/user/${spotify_id}`" target="_blank">
                            <Spotify class="cursor-pointer mt-2" />
                        </a>
                        <DialogTrigger as-child>
                            <Button class="mt-2">Mix Playlists</Button>
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