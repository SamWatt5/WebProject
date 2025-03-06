<script setup lang="ts">
import LogoBar from '../components/logoBar.vue'
import SidePanel from '../components/SidePanel.vue'
import Content from '../components/mainContent.vue'
</script>

<template>
    <body class="bg-blue-400 text-white grid gap-0">
        <LogoBar />
        <SidePanel />
        <Content />
        <slot />
    </body>
</template>

<style scoped>
    body {
        font-family: "Carlito", san-serif;
        min-height: 100vh;
        }
</style>