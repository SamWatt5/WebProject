<script type="ts" setup>
import { Dialog, DialogTrigger, DialogContent, DialogClose, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import UserCard from "./UserCard.vue";
import { Button } from "./ui/button";
import { defineComponent } from 'vue';
import { toast } from "vue-sonner";
import { useUser } from "@/stores/user";
import { useFriends } from "@/stores/friends";
import { ref } from "vue";

defineProps({
    userName: String,
    userAvatar: String,
    userJoined: String
})

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
    if(data.message) {
        toast.success("Unfriended successfully", {
            duration: 5000,
            id: "unfriending"
        });
    } else {
        toast.error("Failed to unfriend", {
            description: data.error,
            duration: 5000,
            id: "unfriending"
        });
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
                <DialogTitle>Friend Management</DialogTitle>
                <DialogDescription>All buttons pressed on this menu are final and can't be reversed</DialogDescription>
            </DialogHeader>
            
            <DialogFooter>
                <DialogClose asChild>
                    <Button variant="destructive" @click="unfriend(userName)">Unfriend</Button>
                </DialogClose>
                <DialogClose asChild>
                    <Button variant="secondary">Block</Button>
                </DialogClose>
                <DialogClose as-child>
                    <Button>Close</Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>