<script setup lang="ts">
import Nav from '../components/NavBar.vue'
import SidePanel from '@/components/SidePanel.vue';
import LogoBar from '@/components/logoBar.vue';
</script>

<template>
    <LogoBar />
    <div class="flex h-screen">
        <div class="w-1/3 bg-gray-100">
            <SidePanel />
        </div>
        <div class="flex-1 bg-white p-5">
            <Nav />
            <slot />
        </div>
    </div>
</template>

<style scoped>
body {
    font-family: "Carlito", sans-serif;
}
</style>