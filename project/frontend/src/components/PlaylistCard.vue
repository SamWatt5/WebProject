<script lang="ts" setup>
import ListeningToCard from './SongCard.vue';
import SongCard from './SongCard.vue';
import { Dialog, DialogContent, DialogHeader, DialogTrigger } from './ui/dialog';
import { defineProps } from "vue";

interface Props {
    title: string,
    artist: string,
    coverImage: string
}

const props = defineProps<Props>()

</script>

<template>
    <Dialog>
        <DialogTrigger asChild>
            <SongCard :title="props.title" :artist="props.artist" :coverImage="props.coverImage" />
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>TEST</DialogHeader>
        </DialogContent>
    </Dialog>
</template>