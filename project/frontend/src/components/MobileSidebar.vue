<script setup lang="ts">
/**
 * MobileSidebar.vue
 *
 * A component for displaying a mobile-friendly sidebar with navigation options and user account management.
 *
 * Features:
 * - Provides navigation buttons for different pages (Home, Playlists, Friends, Settings, Admin).
 * - Displays the user's avatar, username, and account options in a dropdown menu.
 * - Includes a dark mode toggle using the `Darkmode` component.
 * - Allows the user to log out, which clears the session and redirects to the home page.
 *
 * Dependencies:
 * - Pinia: For state management (user store).
 * - Custom UI components: MobileButton, Sheet, DropdownMenu, Avatar, Darkmode.
 * - Vue composables: `storeToRefs` for reactive state management.
 *
 * State:
 * - `user` (ref<User | null>): Stores the current user's information.
 *
 * Methods:
 * - `handleLogout()`: Logs the user out and redirects to the home page.
 */

import { storeToRefs } from 'pinia';
import MobileButton from './sidebarComponents/MobileButton.vue';
import { Sheet, SheetContent, SheetDescription, SheetFooter, SheetHeader, SheetTitle, SheetTrigger } from './ui/sheet';
import { Menu } from "lucide-vue-next";
import { useUser } from '@/stores/user';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Skeleton } from './ui/skeleton';
import Darkmode from './Darkmode.vue';

// Access the user store
const { user } = storeToRefs(useUser());
const { setUser } = useUser();

/**
 * Logs the user out by sending a POST request to the API.
 *
 * Clears the user state and redirects to the home page upon successful logout.
 */
const handleLogout = async () => {
    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });
        if (response.ok) {
            setUser(null);
            window.location.href = '/'; // Reload the page to let the backend handle the redirection
        } else {
            console.error('Logout failed');
        }
    } catch (error) {
        console.error('Error during logout:', error);
    }
};
</script>

<template>
    <Sheet>
        <!-- Trigger button for opening the sidebar -->
        <SheetTrigger as-child>
            <div class="absolute top-5 left-5">
                <Menu />
            </div>
        </SheetTrigger>

        <!-- Sidebar content -->
        <SheetContent side="left" class="flex flex-col h-full">
            <!-- Header with the application title -->
            <SheetHeader>
                <SheetTitle class="text-5xl">TrackMates</SheetTitle>
                <SheetDescription></SheetDescription>
            </SheetHeader>

            <!-- Navigation buttons -->
            <ul class="flex-1">
                <MobileButton page="/" text="Home" />
                <MobileButton page="/playlists" text="Playlists" />
                <MobileButton page="/friends" text="Friends" />
                <MobileButton page="/settings" text="Settings" />
                <MobileButton page="/admin" text="Admin" v-if="user?.admin" />
            </ul>

            <!-- Footer with user account options and dark mode toggle -->
            <SheetFooter class="mt-auto">
                <DropdownMenu>
                    <DropdownMenuTrigger>
                        <!-- User avatar and username -->
                        <div class="flex flex-row items-center space-x-2 bg-accent p-4 mt-2">
                            <Avatar v-if="user?.email">
                                <AvatarFallback class="text-3xl">
                                    {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
                                </AvatarFallback>
                            </Avatar>
                            <Avatar v-else>
                                <AvatarFallback>
                                    <Skeleton class="w-12 h-12 rounded-full" />
                                </AvatarFallback>
                            </Avatar>
                            <h1 class="text-3xl">{{ user?.username }}</h1>
                        </div>
                    </DropdownMenuTrigger>

                    <!-- Dropdown menu for account options -->
                    <DropdownMenuContent>
                        <DropdownMenuLabel>My account</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem v-if="user" @click="handleLogout">Logout</DropdownMenuItem>
                        <RouterLink v-else to="/login">
                            <DropdownMenuItem>Login</DropdownMenuItem>
                        </RouterLink>
                    </DropdownMenuContent>
                </DropdownMenu>

                <!-- Dark mode toggle -->
                <Darkmode />
            </SheetFooter>
        </SheetContent>
    </Sheet>
</template>