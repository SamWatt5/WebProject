<script lang="ts" setup>
import ListeningToCard from './SongCard.vue';
import SongCard from './SongCard.vue';
import { Dialog, DialogContent, DialogHeader, DialogTrigger } from './ui/dialog';


</script>

<template>
    <Dialog>
        <DialogTrigger asChild>
            <SongCard />
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>TEST</DialogHeader>
        </DialogContent>
    </Dialog>
</template>