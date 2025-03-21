<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { SidebarProvider } from './ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Button } from './ui/button';
</script>

<script lang="ts">
    function getRandPos() {
        const windowHeight = window.innerHeight;
        const windowWidth = window.innerWidth;

        const randX = Math.floor(Math.random() * (windowWidth - 200));
        const randY = Math.floor(Math.random() * (windowHeight - 200));

        return { x: randX, y: randY };
    }

    function moveShadow() {
        for(let i = 1; i <= 6; i++) {
            const shadow = document.getElementById(`shadow${i}`) as HTMLElement;
            console.log(i)
            const pos = getRandPos();
            shadow.style.top = `${pos.y}px`;
            shadow.style.left = `${pos.x}px`;
        }
    }

    setInterval(moveShadow, 2000);
</script>

<template>
    <div class="grid grid-cols-[auto_1fr] max-h-full overflow-hidden max-w-full h-screen">
        <SidebarProvider :default-open="false" :open="false">
            <Sidebar />
        </SidebarProvider>

        <div class="flex items-center justify-center flex-col">
            <div class="absolute inset-0 flex justify-center items-center -z-10">
                <div id="shadow1" class="transition-all duration-1000 ease-in-out w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute -top-10 -left-20"></div>
                <div id="shadow2" class="transition-all duration-1000 ease-in-out w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute top-20 right-10"></div>
                <div id="shadow3" class="transition-all duration-1000 ease-in-out w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute -top-10 -left-20"></div>
                <div id="shadow4" class="transition-all duration-1000 ease-in-out w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute top-20 right-10"></div>
                <div id="shadow5" class="transition-all duration-1000 ease-in-out w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute -top-10 -left-20"></div>
                <div id="shadow6" class="transition-all duration-1000 ease-in-out w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute top-20 right-10"></div>
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