<script setup lang="ts">
import ProfilePic from './ProfilePic.vue';
</script>

<template>
    <div class="bg-black h-24 flex items-center">
        <img src="/TrackMates.png" alt="logo" class="h-full object-cover ml-4" />
        <div class="flex-grow"></div>
        <div class="mr-4">
            <ProfilePic />
        </div>
    </div>
</template>

<style scoped></style>