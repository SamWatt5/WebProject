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

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

const { user } = useUser();

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
            <div class="w-full display-inline">
                <img src="/TrackMates.png" class="rounded-full w-auto h-[300px] hover:animate-spin" />
            </div>
            
            <UserCard>
                
            </UserCard>

            <div class="w-full col-span-3 flex flex-col h-full">
                <ScrollArea class="border rounded-md col-span-3 w-[95%] mt-4 whitespace-nowrap mt-auto">
                <div class="flex p-4 space-x-4 w-max mt-auto">
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