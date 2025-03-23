<script setup lang="ts">
import { Dialog, DialogTitle, DialogContent, DialogTrigger, DialogHeader, DialogFooter, DialogClose } from './ui/dialog';
import { Button } from './ui/button';
import { ref } from "vue"
import { Input } from './ui/input';
import { toast } from 'vue-sonner';
import { type User } from '@/stores/user';
import { Loader2 } from 'lucide-vue-next';

let open = ref(false);
let user = ref<User>();

const acceptFriendship = async() => {
    toast.loading("Accepting friend request...", {
        duration: Infinity,
        id: "accepting-friendship",
        dismissible: false
    });

    const res = await fetch(`/api/user/add-friend/${user.value?.username}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });
    const data = await res.json();
    console.log(data);
    if(data.message) {
        toast.success("Accepted friend request", {
            duration: 5000,
            id: "accepting-friendship"
        });
    } else {
        toast.error("Failed to accept friend request", {
            description: data.error,
            duration: 5000,
            id: "accepting-friendship"
        });
    }
}

const search = async() => {
    const input = document.getElementById("search-prompt") as HTMLInputElement;
    if(input.value.length == 0) {
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
    if(data.error) {
        toast.error("Failed to find user", {
            description: data.error,
            duration: 5000,
            id: "searching-user",
            dismissible: true
        });
    } else {
        user.value = data;
        open.value = true;
        toast.success("Found user", {
            description: "",
            duration: 2000,
            id: "searching-user",
            dismissible: true
        });

    }

    input.value = "";
}
</script>

<template>
    <div class="flex flex-row items-center">
        <Input placeholder="Search for friend" id="search-prompt" />
        <Button class="ml-2" @click="search" id="search-button">Search</Button>
        <Dialog :open="open" @update:open="open = $event">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Do you want to add <span class="text-cyan-500 font-semibold">{{ user?.username }}</span> as a friend?</DialogTitle>
                </DialogHeader>


                <DialogFooter>
                    <DialogClose as-child>
                        <Button @click="acceptFriendship" variant="default">Yes</Button>
                    </DialogClose>
                    <DialogClose as-child>
                        <Button variant="destructive">No</Button>
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>