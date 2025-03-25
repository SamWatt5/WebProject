<script lang="ts" setup>
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import PlaylistCard from '@/components/PlaylistCard.vue';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);



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