<script setup lang="ts">
import { Dialog, DialogTitle, DialogContent, DialogTrigger, DialogHeader, DialogFooter, DialogClose } from './ui/dialog';
import { Button } from './ui/button';
import { ref } from "vue"
import { Input } from './ui/input';
import { toast } from 'vue-sonner';
import { type User } from '@/stores/user';
import { Loader2 } from 'lucide-vue-next';
import { useFriends } from '@/stores/friends';
import { storeToRefs } from 'pinia';

let open = ref(false);
let user = ref<User>();
const store = useFriends();
const { friends } = storeToRefs(store);
const { setFriends } = store;

const acceptFriendship = async() => {
    toast.loading("Making friends...", {
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
    if(data.message) {
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
        }, 5000)
    } else {
        toast.error("Failed to make friend", {
            description: data.error,
            duration: 5000,
            id: "accepting-friendship"
        });
        setTimeout(() => {
            toast.dismiss("accepting-friendship");
        }, 5000)
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