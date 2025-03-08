<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import SidebarProvider from "@/components/ui/sidebar/SidebarProvider.vue";
</script>

<template>
  <main>
    <SidebarProvider :default-open="false" :open="false">
      <Sidebar />
    </SidebarProvider>
  </main>
</template>