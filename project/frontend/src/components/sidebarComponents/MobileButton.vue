<script setup lang="ts">
import { Button } from '../ui/button';

const clicked = (page: string) => {
    location.href = page;
}

defineProps<{
    page: string,
    text: string
}>();
</script>

<template>
    <div class="bg-accent rounded-lg p-4 my-2 pointer-cursor text-center">
        <h1 class="text-4xl" @click="clicked(page)">{{ text }}</h1>
    </div>
</template>