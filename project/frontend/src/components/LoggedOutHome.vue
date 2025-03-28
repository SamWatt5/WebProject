<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { SidebarProvider } from './ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Button } from './ui/button';
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from './MobileSidebar.vue';

</script>

<template>
    <div class="grid grid-cols-[auto_1fr] max-h-full overflow-hidden max-w-full h-screen">
        <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
            <Sidebar />
        </SidebarProvider>
        <MobileSidebar v-else />

        <div class="flex items-center justify-center flex-col">
            <div class="-z-10">
                <div class="-translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute top-1/2 left-1/2"></div>
            </div>
            <Card class="">
                <CardHeader>
                    <CardTitle class="text-4xl text-center">Welcome to <span class="text-cyan-500 text-5xl font-bold">TrackMates</span></CardTitle>
                </CardHeader>
                <CardContent>
                    <h1 class="text-xl text-center">To begin, please login or create an account using the buttons below.</h1>
                    <div class="flex flex-row justify-center gap-4 mt-4">
                        <Button size="lg" class="bg-green-500 text-primary-foreground shadow hover:bg-green-600" asChild><RouterLink to="/register">Register</RouterLink></Button>
                        <Button size="lg" class="bg-blue-500 hover:bg-blue-600 text-primary-foreground shadow" asChild><RouterLink to="/login">Login</RouterLink></Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
</template>