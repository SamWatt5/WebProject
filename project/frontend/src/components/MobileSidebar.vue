<script setup lang="ts">
import { storeToRefs } from 'pinia';
import MobileButton from './sidebarComponents/MobileButton.vue';
import { Sheet, SheetContent, SheetDescription, SheetFooter, SheetHeader, SheetTitle, SheetTrigger } from './ui/sheet';
import { Menu } from "lucide-vue-next";
import { useUser } from '@/stores/user';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from './ui/dropdown-menu';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Skeleton } from './ui/skeleton';
import Darkmode from './Darkmode.vue';

const { user } = storeToRefs(useUser());
const { setUser } = useUser();

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
        <SheetTrigger as-child>
            <div class="absolute top-5 left-5">
                <Menu></Menu>
            </div>
        </SheetTrigger>
        <SheetContent side="left" class="flex flex-col h-full">
            <SheetHeader>
                <SheetTitle class="text-5xl">TrackMates</SheetTitle>
                <SheetDescription></SheetDescription>
            </SheetHeader>
            <ul class="flex-1">
                <MobileButton page="/" text="Home" />
                <MobileButton page="/playlist" text="Playlist" />
                <MobileButton page="/friends" text="Friends" />
                <MobileButton page="/settings" text="Settings" />
                <MobileButton page="/admin" text="Admin" v-if="user?.admin" />
            </ul>

            <SheetFooter class="mt-auto">
                <DropdownMenu>
                    <DropdownMenuTrigger>
                        <div class="flex flex-row items-center space-x-2 bg-accent p-4 mt-2">
                            <Avatar class="" v-if="user?.email">
                                <AvatarFallback class="text-3xl">{{ user.first_name?.[0] }}{{ user.last_name?.[0] }}</AvatarFallback>
                            </Avatar>
                            <Avatar v-else>
                                <AvatarFallback>
                                    <Skeleton class="w-12 h-12 rounded-full" />
                                </AvatarFallback>
                            </Avatar>
                            <h1 class="text-3xl">{{ user?.username }}</h1>
                        </div>
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
                <Darkmode class="" />
            </SheetFooter>
        </SheetContent>
    </Sheet>
</template>