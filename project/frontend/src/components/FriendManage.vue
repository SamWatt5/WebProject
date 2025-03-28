<script type="ts" setup>
/**
 * FriendManage.vue
 *
 * A component for managing a user's friends, including displaying friend details
 * and providing options to manage or unfriend a user.
 *
 * Features:
 * - Displays a friend's avatar, username, and Spotify profile link.
 * - Allows users to unfriend a friend with confirmation.
 * - Provides a "Manage" button to open a dialog for managing the friend.
 * - Uses Pinia for state management and `vue-sonner` for toast notifications.
 *
 * Props:
 * - userName (String): The friend's username.
 * - userAvatar (String): The friend's avatar or fallback text.
 * - userJoined (String): The date the friend joined.
 * - spotify_id (String): The friend's Spotify user ID.
 *
 * Dependencies:
 * - Pinia: For state management.
 * - vue-sonner: For toast notifications.
 * - Custom UI components: Dialog, Button, Card, Avatar, etc.
 */

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

// Define props for the component
defineProps({
    userName: String,
    userAvatar: String,
    userJoined: String,
    spotify_id: String
});

// Initialize the friends store
let store = useFriends();
let { friends } = storeToRefs(store); // Ensure `friends` is reactive
let { setFriends } = store;

/**
 * Unfriends a user by sending a DELETE request to the API.
 *
 * Args:
 * - username (String): The username of the friend to unfriend.
 *
 * Returns:
 * - None
 */
const unfriend = async (username) => {
    toast.loading("Unfriending...", {
        duration: Infinity,
        id: "unfriending",
        dismissible: false
    });

    const res = await fetch(`/api/user/friends/${username}`, {
        method: "DELETE",
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
};
</script>

<template>
    <Dialog>
        <!-- Friend card displaying user details -->
        <Card class="cursor-pointer w-full">
            <CardHeader class="flex flex-row">
                <Avatar class="w-20 h-20 mt-2">
                    <AvatarFallback class="text-3xl">{{ userAvatar }}</AvatarFallback>
                </Avatar>
                <div class="flex flex-col pl-3 w-full">
                    <CardTitle class="text-2xl">@{{ userName }}</CardTitle>
                    <CardDescription class="flex flex-row">
                        <!-- Placeholder for additional details -->
                    </CardDescription>
                    <div class="flex flex-row justify-between mt-2">
                        <!-- Spotify profile link -->
                        <a :href="`https://open.spotify.com/user/${spotify_id}`" target="_blank">
                            <Spotify class="cursor-pointer mt-2" />
                        </a>
                        <!-- Manage button -->
                        <DialogTrigger as-child>
                            <Button class="mt-2">Manage</Button>
                        </DialogTrigger>
                    </div>
                </div>
            </CardHeader>
        </Card>

        <!-- Dialog content for managing the friend -->
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Manage <span class="text-cyan-500 font-semibold">{{ userName }}</span></DialogTitle>
                <DialogDescription>All buttons pressed on this menu are final and can't be reversed</DialogDescription>
            </DialogHeader>

            <DialogFooter>
                <!-- Unfriend button -->
                <DialogClose asChild>
                    <Button variant="destructive" @click="unfriend(userName)">Unfriend</Button>
                </DialogClose>
                <!-- Close button -->
                <DialogClose as-child>
                    <Button>Close</Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>