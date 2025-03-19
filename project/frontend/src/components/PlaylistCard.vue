<script lang="ts" setup>
import ListeningToCard from './ListeningToCard.vue';
import { Dialog, DialogContent, DialogHeader, DialogTrigger } from './ui/dialog';


</script>

<template>
    <Dialog>
        <DialogTrigger asChild>
            <ListeningToCard />
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>TEST</DialogHeader>
        </DialogContent>
    </Dialog>
</template>