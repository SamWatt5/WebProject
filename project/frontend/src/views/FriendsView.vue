<script lang="ts" setup>
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Card, CardHeader, CardDescription, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
// import UserCard from '@/components/UserCard.vue';
import FriendManage from '@/components/FriendManage.vue';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);


const friendClick = (friend: string) => {
    console.log("Friend clicked");
}

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
        </main>
        <div class="flex flex-col pt-10 gap-4 mr-4">
            <Card class="mt-4">
                <CardHeader>
                    <CardTitle class="text-4xl">Friends</CardTitle>
                    <CardDescription>Here is some management settings for friends</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="flex flex-row items-center">
                        <Input placeholder="Search for friend" />
                        <Button class="ml-2">Search</Button>
                    </div>
                </CardContent>
                <CardFooter>
                    <CardDescription>To manage a friend, just click on their tile</CardDescription>
                </CardFooter>
            </Card>
                <ScrollArea class="border rounded-md whitespace-nowrap h-[60vh] p-4">
                    <div class="grid grid-cols-3 grid-flow-row gap-4">
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                        <FriendManage />
                    </div>
                </ScrollArea>
        </div>
    </div>
</template>