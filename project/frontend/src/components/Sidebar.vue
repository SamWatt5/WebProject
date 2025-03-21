<script setup lang="ts">
import { Sidebar, SidebarContent, SidebarMenuButton, SidebarFooter, SidebarHeader } from './ui/sidebar';
import { House, ListMusic, Users, Settings } from 'lucide-vue-next';
import Tooltips from './sidebarComponents/Tooltips.vue';
import { Avatar, AvatarFallback } from './ui/avatar';
import Darkmode from './Darkmode.vue';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
import { Skeleton } from './ui/skeleton';

import { useUser } from '@/stores/user';
import { storeToRefs } from 'pinia';

const { user } = storeToRefs(useUser()); // Ensure reactivity
const { setUser } = useUser();
</script>

<template>
    <Sidebar collapsible="icon">
        <SidebarHeader className="p-1">
            <img src="/TrackMates.png" class="rounded-full" />
        </SidebarHeader>
        <SidebarContent class="p-1 pt-4">
            <SidebarMenuButton><RouterLink to="/"><Tooltips item="Home"><House /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="/playlists"><Tooltips item="Playlists"><ListMusic /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="/friends"><Tooltips item="Friends"><Users /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="#"><Tooltips item="Settings"><Settings /></Tooltips></RouterLink></SidebarMenuButton>
        </SidebarContent>
        <SidebarFooter className="p-1">
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
                    <RouterLink v-if="user" to="/api/auth/logout" @click="setUser(null)">
                        <DropdownMenuItem>Logout</DropdownMenuItem>
                    </RouterLink>
                    <RouterLink v-else to="/login">
                        <DropdownMenuItem>Login</DropdownMenuItem>
                    </RouterLink>
                </DropdownMenuContent>
            </DropdownMenu>
        </SidebarFooter>
    </Sidebar>
</template>
