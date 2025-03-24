<script type="ts" setup>
import { Dialog, DialogTrigger, DialogContent, DialogClose, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import UserCard from "./UserCard.vue";
import { Button } from "./ui/button";
import { toast } from "vue-sonner";
import { useFriends } from "@/stores/friends";
import { storeToRefs } from "pinia";

defineProps({
    userName: String,
    userAvatar: String,
    userJoined: String
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
        <DialogTrigger as-child>
            <UserCard :name="userName" :avatar="userAvatar" :joined="userJoined" />
        </DialogTrigger>
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