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
import { onMounted, ref } from 'vue';
import { useUser, type User } from '@/stores/user';
import { toast } from 'vue-sonner';
import { useFriends } from '@/stores/friends';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);


const friendClick = (friend: string) => {
    console.log("Friend clicked");
}

let { user, setUser } = useUser();
let { friends, setFriends } = useFriends();
const isLoading = ref(true);
toast.loading("Loading user data...", {
  duration: Infinity,
  id: "loading-data",
  dismissible: false
});

onMounted(async() => {
    try {
        const res = await fetch("/api/user/me", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await res.json();
        
        if(!data.error) {
            setUser(data);
            console.log("Set user successfully", data);
            user = data;
            for(let friend of data.friends) {
                const res = await fetch(`/api/user/find/${friend}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const friendData = await res.json();
                friends.push(friendData);
            }
            setFriends(friends)
        }

      isLoading.value = false;
      toast.dismiss("loading-data");
    } catch(err) {
      console.error(err);
    }
});


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
            <Card class="mt-4 overflow-hidden">
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
                    <div class="grid grid-cols-3 grid-flow-row gap-4" v-for="(friend, index) in friends" :key="index">
                        {{ console.log(friend) }}
                        <FriendManage :userName="friend.username" :userAvatar="friend.first_name?.[0] + friend.last_name?.[0]" :userJoined="'December 2021'" />
                    </div>
                </ScrollArea>
        </div>
    </div>
</template>