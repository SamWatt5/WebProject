// filepath: /Users/mwaka/Documents/WebProject/project/frontend/src/components/Sidebar.vue
<script setup lang="ts">
/**
 * Sidebar.vue
 *
 * A component for displaying a collapsible sidebar with navigation options and user account management.
 *
 * Features:
 * - Provides navigation buttons for different pages (Home, Playlists, Friends, Settings, Admin).
 * - Displays the user's avatar, username, and account options in a dropdown menu.
 * - Includes a dark mode toggle using the `Darkmode` component.
 * - Shows a toast notification if the user hasn't linked their Spotify account.
 * - Allows the user to log out, which clears the session and redirects to the home page.
 *
 * Dependencies:
 * - Pinia: For state management (user store).
 * - Custom UI components: Sidebar, Tooltips, DropdownMenu, Avatar, Darkmode.
 * - Vue composables: `storeToRefs` for reactive state management, `onMounted` for lifecycle hooks.
 *
 * State:
 * - `user` (ref<User | null>): Stores the current user's information.
 *
 * Methods:
 * - `handleLogout()`: Logs the user out and redirects to the home page.
 */

import { Sidebar, SidebarContent, SidebarMenuButton, SidebarFooter, useSidebar } from './ui/sidebar';
import { House, ListMusic, Users, Settings, ShieldUser } from 'lucide-vue-next';
import Tooltips from './sidebarComponents/Tooltips.vue';
import { Avatar, AvatarFallback } from './ui/avatar';
import Darkmode from './Darkmode.vue';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
import { Skeleton } from './ui/skeleton';
import { useUser } from '@/stores/user';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { toast } from 'vue-sonner';

// Access the sidebar state
const { openMobile, state, setOpenMobile } = useSidebar();

// Access the user store
const { user } = storeToRefs(useUser()); // Ensure reactivity
const { setUser } = useUser();
const router = useRouter();

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

// Show a toast notification if the user hasn't linked their Spotify account
if (user.value && !user.value?.spotify_id) {
    toast.info("You haven't linked your Spotify Account yet!", {
        duration: Infinity,
        id: "spotify-info",
        dismissible: false,
        action: {
            label: "Link Spotify",
            onClick: () => {
                router.push("/settings");
            }
        }
    });
}
</script>

<template>
    <Sidebar collapsible="icon">
        <!-- Sidebar header with the application logo -->
        <SidebarHeader class="p-1">
            <img src="/TrackMates.png" class="rounded-full hover:animate-spin" />
        </SidebarHeader>

        <!-- Sidebar content with navigation buttons -->
        <SidebarContent class="p-1 pt-4">
            <SidebarMenuButton>
                <RouterLink to="/">
                    <Tooltips item="Home">
                        <House />
                    </Tooltips>
                </RouterLink>
            </SidebarMenuButton>
            <SidebarMenuButton>
                <RouterLink to="/playlists">
                    <Tooltips item="Playlists">
                        <ListMusic />
                    </Tooltips>
                </RouterLink>
            </SidebarMenuButton>
            <SidebarMenuButton>
                <RouterLink to="/friends">
                    <Tooltips item="Friends">
                        <Users />
                    </Tooltips>
                </RouterLink>
            </SidebarMenuButton>
            <SidebarMenuButton>
                <RouterLink to="/settings">
                    <Tooltips item="Settings">
                        <Settings />
                    </Tooltips>
                </RouterLink>
            </SidebarMenuButton>
            <SidebarMenuButton v-if="user?.admin">
                <RouterLink to="/admin">
                    <Tooltips item="Admin">
                        <ShieldUser />
                    </Tooltips>
                </RouterLink>
            </SidebarMenuButton>
        </SidebarContent>

        <!-- Sidebar footer with dark mode toggle and user account options -->
        <SidebarFooter class="p-1">
            <Darkmode />
            <DropdownMenu>
                <DropdownMenuTrigger>
                    <!-- User avatar -->
                    <Avatar v-if="user?.email">
                        <AvatarFallback>
                            {{ user.first_name?.[0].toUpperCase() }}{{ user.last_name?.[0].toUpperCase() }}
                        </AvatarFallback>
                    </Avatar>
                    <Avatar v-else>
                        <AvatarFallback>
                            <Skeleton class="w-12 h-12 rounded-full" />
                        </AvatarFallback>
                    </Avatar>
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
        </SidebarFooter>
    </Sidebar>
</template>