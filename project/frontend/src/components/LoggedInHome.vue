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
import SongCard from './SongCard.vue';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

const { user } = useUser();

</script>

<template>
    <div class="flex flex-row max-w-[100vw]">
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
        <div class="flex flex-col">
            <div class="flex flex-row">
                <div class="">
                    <img src="/TrackMates.png" class="rounded-full w-auto h-[300px] hover:animate-spin col-span-2" />
                </div>
                
                <Card class="mt-4">
                    <CardHeader>
                        <CardTitle class="text-4xl">Hey there, @<span class="text-cyan-500 font-semibold">{{ user?.username }}</span></CardTitle>
                        
                    </CardHeader>
                    <CardContent>
                        <!-- <UserCard :user="user" /> -->
                    </CardContent>
                </Card>
                <Card class="mt-4 ml-4">
                    <CardHeader>
                        <CardTitle class="text-4xl">Friend 1 @<span class="text-cyan-500 font-semibold">{{ user?.username }}</span></CardTitle>
                        <CardDescription></CardDescription>
                    </CardHeader>
                    <CardContent>
                        <!-- <UserCard :user="user" /> -->
                    </CardContent>
                </Card>
            </div>
            
            <Card class="w-12">
                <CardHeader>
                    <CardTitle>HE</CardTitle>
                </CardHeader>
            </Card>

            <div class="w-[37%] mt-auto mb-12">
                <ScrollArea class="border rounded-md w-full whitespace-nowrap">
                <div class="flex p-4 w-full space-x-4 mt-auto">
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