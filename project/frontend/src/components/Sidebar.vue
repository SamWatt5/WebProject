// filepath: /Users/mwaka/Documents/WebProject/project/frontend/src/components/Sidebar.vue
<script setup lang="ts">
import { Sidebar, SidebarContent, SidebarMenuButton, SidebarFooter, useSidebar } from './ui/sidebar';
import { House, ListMusic, Users, Settings } from 'lucide-vue-next';
import Tooltips from './sidebarComponents/Tooltips.vue';
import { Avatar, AvatarFallback } from './ui/avatar';
import Darkmode from './Darkmode.vue';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
import { Skeleton } from './ui/skeleton';
import { ShieldUser } from 'lucide-vue-next';
import { useUser } from '@/stores/user';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { toast } from 'vue-sonner';
import { Button } from './ui/button';

const { openMobile, state, setOpenMobile } = useSidebar();

const { user } = storeToRefs(useUser()); // Ensure reactivity
const { setUser } = useUser();
const router = useRouter();

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

if(user.value && !user.value?.spotify_id) {
    toast.info("You haven't linked your Spotify Account yet!",{
            duration: Infinity,
            id: "spotify-info",
            dismissible: false,
            action: {
                label: "Link Spotify",
                onClick: () => {
                    router.push("/settings");
                }
            }
    })
}

// onMounted(() => {
    
// })
</script>

<template>
    <Sidebar collapsible="icon">
        <SidebarHeader class="p-1">
            <img src="/TrackMates.png" class="rounded-full hover:animate-spin" />
        </SidebarHeader>
        <SidebarContent class="p-1 pt-4">
            <SidebarMenuButton><RouterLink to="/"><Tooltips item="Home"><House /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="/playlists"><Tooltips item="Playlists"><ListMusic /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="/friends"><Tooltips item="Friends"><Users /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="/settings"><Tooltips item="Settings"><Settings /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton v-if="user?.admin"><RouterLink to="/admin"><Tooltips item="Admin"><ShieldUser /></Tooltips></RouterLink></SidebarMenuButton>
        </SidebarContent>
        <SidebarFooter class="p-1">
            <Darkmode />
            <DropdownMenu>
                <DropdownMenuTrigger>
                    <Avatar v-if="user?.email">
                        <AvatarFallback>{{ user.first_name?.[0] }}{{ user.last_name?.[0] }}</AvatarFallback>
                    </Avatar>
                    <Avatar v-else>
                        <AvatarFallback><Skeleton class="w-12 h-12 rounded-full" /></AvatarFallback>
                    </Avatar>
                </DropdownMenuTrigger>
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