<script setup lang="ts">
/**
 * LoggedOutHome.vue
 *
 * A component for displaying the home page for logged-out users.
 *
 * Features:
 * - Displays a welcome message and a brief introduction to the application.
 * - Provides buttons for users to register or log in.
 * - Includes a sidebar for navigation and a mobile-friendly sidebar alternative.
 * - Uses a visually appealing background with a blurred circular effect.
 *
 * Dependencies:
 * - Custom UI components: Sidebar, Card, Button.
 * - Vue composables: `useIsMobile` for responsive design.
 *
 * State:
 * - None.
 *
 * Methods:
 * - None.
 */

import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { SidebarProvider } from './ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Button } from './ui/button';
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from './MobileSidebar.vue';
</script>

<template>
    <div class="grid grid-cols-[auto_1fr] max-h-full overflow-hidden max-w-full h-screen">
        <!-- Sidebar for navigation -->
        <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
            <Sidebar />
        </SidebarProvider>
        <MobileSidebar v-else />

        <!-- Main content area -->
        <div class="flex items-center justify-center flex-col">
            <!-- Background effect -->
            <div class="-z-10">
                <div
                    class="-translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500 opacity-50 blur-3xl rounded-full absolute top-1/2 left-1/2">
                </div>
            </div>

            <!-- Welcome card -->
            <Card>
                <CardHeader>
                    <CardTitle class="text-4xl text-center">
                        Welcome to <span class="text-cyan-500 text-5xl font-bold">TrackMates</span>
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <h1 class="text-xl text-center">
                        To begin, please login or create an account using the buttons below.
                    </h1>
                    <div class="flex flex-row justify-center gap-4 mt-4">
                        <!-- Register button -->
                        <Button size="lg" class="bg-green-500 text-primary-foreground shadow hover:bg-green-600"
                            asChild>
                            <RouterLink to="/register">Register</RouterLink>
                        </Button>
                        <!-- Login button -->
                        <Button size="lg" class="bg-blue-500 hover:bg-blue-600 text-primary-foreground shadow" asChild>
                            <RouterLink to="/login">Login</RouterLink>
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
</template>