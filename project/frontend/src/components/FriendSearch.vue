<script setup lang="ts">
/**
 * FriendSearch.vue
 *
 * A component for searching and adding friends by username.
 *
 * Features:
 * - Allows users to search for other users by username.
 * - Displays a confirmation dialog to add the searched user as a friend.
 * - Uses Pinia for state management and `vue-sonner` for toast notifications.
 *
 * Dependencies:
 * - Pinia: For state management.
 * - vue-sonner: For toast notifications.
 * - Custom UI components: Dialog, Button, Input, etc.
 *
 * State:
 * - `open` (ref<boolean>): Controls the visibility of the confirmation dialog.
 * - `user` (ref<User | undefined>): Stores the user data of the searched friend.
 *
 * Methods:
 * - `search()`: Searches for a user by username.
 * - `acceptFriendship()`: Sends a request to add the searched user as a friend.
 */

import { Dialog, DialogTitle, DialogContent, DialogTrigger, DialogHeader, DialogFooter, DialogClose } from './ui/dialog';
import { Button } from './ui/button';
import { ref } from "vue";
import { Input } from './ui/input';
import { toast } from 'vue-sonner';
import { type User } from '@/stores/user';
import { Loader2 } from 'lucide-vue-next';
import { useFriends } from '@/stores/friends';
import { storeToRefs } from 'pinia';

// State variables
let open = ref(false); // Controls the dialog visibility
let user = ref<User>(); // Stores the searched user's data

// Initialize the friends store
const store = useFriends();
const { friends } = storeToRefs(store); // Reactive reference to the friends list
const { setFriends } = store;

/**
 * Sends a request to add the searched user as a friend.
 *
 * Displays a loading toast while the request is in progress.
 * Updates the friends list and shows a success or error toast based on the response.
 */
const acceptFriendship = async () => {
    toast.loading("Making friends...", {
        duration: Infinity,
        id: "accepting-friendship",
        dismissible: false
    });

    const res = await fetch(`/api/user/friends/${user.value?.username}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });
    const data = await res.json();

    if (data.message) {
        const userData = await fetch(`/api/user/find/${user.value?.username}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const userDataJson = await userData.json();
        setFriends([...friends.value, userDataJson]);
        open.value = false;

        toast.success("You are now friends", {
            duration: 5000,
            id: "accepting-friendship"
        });

        setTimeout(() => {
            toast.dismiss("accepting-friendship");
        }, 5000);
    } else {
        toast.error("Failed to make friend", {
            description: data.error,
            duration: 5000,
            id: "accepting-friendship"
        });

        setTimeout(() => {
            toast.dismiss("accepting-friendship");
        }, 5000);
    }
};

/**
 * Searches for a user by username.
 *
 * Displays a loading toast while the search is in progress.
 * Shows a success or error toast based on the search result.
 */
const search = async () => {
    const input = document.getElementById("search-prompt") as HTMLInputElement;
    if (input.value.length === 0) {
        toast.error("Please enter a username to search for", {
            duration: 5000
        });
        return;
    }

    toast.loading("Searching for user...", {
        duration: Infinity,
        id: "searching-user",
        dismissible: false
    });

    const res = await fetch(`/api/user/find/${input.value}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    const data = await res.json();

    if (data.error) {
        toast.error("Failed to find user", {
            description: data.error,
            duration: 5000,
            id: "searching-user",
            dismissible: true
        });

        setTimeout(() => {
            toast.dismiss("searching-user");
        }, 5000);
    } else {
        user.value = data;
        open.value = true;

        toast.success("Found user", {
            description: "",
            duration: 2000,
            id: "searching-user",
            dismissible: true
        });

        setTimeout(() => {
            toast.dismiss("searching-user");
        }, 2000);
    }

    input.value = "";
};
</script>

<template>
    <div class="flex flex-row items-center">
        <!-- Input field for searching a friend -->
        <Input placeholder="Search for friend" id="search-prompt" />
        <!-- Search button -->
        <Button class="ml-2" @click="search" id="search-button">Search</Button>

        <!-- Dialog for confirming friendship -->
        <Dialog :open="open" @update:open="open = $event">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>
                        Do you want to add <span class="text-cyan-500 font-semibold">{{ user?.username }}</span> as a
                        friend?
                    </DialogTitle>
                </DialogHeader>

                <DialogFooter>
                    <!-- Cancel button -->
                    <DialogClose as-child>
                        <Button variant="destructive">No</Button>
                    </DialogClose>
                    <!-- Confirm button -->
                    <DialogClose as-child class="mb-2">
                        <Button @click="acceptFriendship" variant="success">Yes</Button>
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>