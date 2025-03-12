<script setup lang="ts">
import { Sidebar, SidebarContent, SidebarGroup, SidebarGroupLabel, SidebarGroupContent, SidebarMenuItem, SidebarMenuButton, SidebarFooter, SidebarHeader } from './ui/sidebar';
import { House, ListMusic, Users, Settings } from 'lucide-vue-next';
import Tooltips from './sidebarComponents/Tooltips.vue';
import { Avatar, AvatarFallback } from './ui/avatar';
import Darkmode from './Darkmode.vue';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
</script>

<template>
    <Sidebar collapsible="icon">
        <SidebarHeader className="p-1">
            <img src="/TrackMates.png" class="rounded-full" />
        </SidebarHeader>
        <SidebarContent class="p-1 pt-4">
            <SidebarMenuButton><RouterLink to="/"><Tooltips item="Home"><House /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="#"><Tooltips item="Playlists"><ListMusic /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="/friends"><Tooltips item="Friends"><Users /></Tooltips></RouterLink></SidebarMenuButton>
            <SidebarMenuButton><RouterLink to="#"><Tooltips item="Settings"><Settings /></Tooltips></RouterLink></SidebarMenuButton>
        </SidebarContent>
        <SidebarFooter className="p-1">
            <Darkmode />
            <DropdownMenu>
                <DropdownMenuTrigger>
                    <Avatar>
                        <AvatarFallback>CL</AvatarFallback>
                    </Avatar>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                    <DropdownMenuLabel>My account</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Logout</DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </SidebarFooter>
    </Sidebar>
</template>