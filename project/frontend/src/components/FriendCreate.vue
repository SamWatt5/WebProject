<script type="ts" setup>
import { Dialog, DialogTrigger, DialogContent, DialogClose, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import UserCard from "./UserCard.vue";
import { Button } from "./ui/button";
import { toast } from "vue-sonner";
import { useFriends } from "@/stores/friends";
import { storeToRefs } from "pinia";
import { Card, CardHeader, CardTitle, CardDescription } from "./ui/card";
import { CalendarDays } from "lucide-vue-next";
import { Avatar, AvatarFallback } from "./ui/avatar";
import Spotify from "./icons/Spotify.vue";
import { defineProps } from "vue";

defineProps({
    userName: String,
    userAvatar: String,
    userJoined: String,
    spotify_id: String
})

let store = useFriends();
let { friends } = storeToRefs(store); // Ensure `friends` is reactive
let { setFriends } = store;

const unfriend = async (username) => {
    toast.loading("Unfriending...", {
        duration: Infinity,
        id: "unfriending",
        dismissible: false
    });
    
    const res = await fetch(`/api/user/remove-friend/${username}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const data = await res.json();
    if (data.message) {
        toast.success("Unfriended successfully", {
            duration: 5000,
            id: "unfriending",
            closeButton: true,
            dismissible: true
        });
        setFriends(friends.value.filter(friend => friend.username !== username));

        setTimeout(() => {
            toast.dismiss("unfriending");
        }, 5000);
    } else {
        toast.error("Failed to unfriend", {
            description: data.error,
            duration: 5000,
            dismissible: true,
            id: "unfriending",
            closeButton: true
        });
        setTimeout(() => {
            toast.dismiss("unfriending");
        }, 5000);
    }
}
</script>


<template>
    <Dialog>
        <!-- <DialogTrigger as-child> -->
            <!-- <UserCard :spotify_id="spotify_id" :name="userName" :avatar="userAvatar" :joined="userJoined" /> -->
            <Card class="cursor-pointer">
                <CardHeader class="flex flex-row">
                    <Avatar class="w-20 h-20 mt-2">
                        <AvatarFallback class="text-3xl">{{ userAvatar }}</AvatarFallback>
                    </Avatar>
                    <div class="flex flex-col pl-3">
                        <CardTitle class="text-4xl">@{{ userName }}</CardTitle>
                        <CardDescription class="flex flex-row">
                            <CalendarDays class="h-8 w-8 mt-1" /><span class="mt-[3px] text-lg ml-1"> Joined {{ userJoined
                                }}</span>
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
        <!-- </DialogTrigger> -->
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Manage <span class="text-cyan-500 font-semibold">{{ userName }}</span></DialogTitle>
                <DialogDescription>All buttons pressed on this menu are final and can't be reversed</DialogDescription>
            </DialogHeader>

            <DialogFooter>
                <DialogClose asChild>
                    <Button variant="destructive" @click="unfriend(userName)">Unfriend</Button>
                </DialogClose>
                <DialogClose as-child>
                    <Button>Close</Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>