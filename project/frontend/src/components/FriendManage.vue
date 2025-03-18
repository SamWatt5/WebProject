<script type="ts" setup>
import { Dialog, DialogTrigger, DialogContent, DialogClose, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import UserCard from "./UserCard.vue";
import { Button } from "./ui/button";
import { defineComponent } from 'vue';

defineProps({
    name: String,
    avatar: String,
    joined: String
})

defineComponent({
  name: 'FriendManage',
});
</script>

<template>
    <Dialog>
        <DialogTrigger as-child>
            <UserCard name="Cameron" avatar="CL" joined="2021-10-01" />
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Friend Management</DialogTitle>
                <DialogDescription>Here you can manage your friend</DialogDescription>
            </DialogHeader>
            

            <DialogFooter>
                <DialogClose as-child>
                    <Button>Close</Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>