<script setup lang="ts">
/**
 * AdminView.vue
 *
 * A component for managing users in the admin dashboard.
 *
 * Features:
 * - Displays a list of all users with the ability to search for a specific user.
 * - Allows admins to promote, demote, or delete users.
 * - Provides detailed information about a selected user.
 * - Includes a sidebar for navigation and a mobile-friendly sidebar alternative.
 * - Displays toast notifications for actions like searching, promoting, demoting, and deleting users.
 *
 * Dependencies:
 * - Pinia: For state management (user store).
 * - Custom UI components: Sidebar, ScrollArea, Separator, Card, Button, Input, Dialog.
 * - Vue composables: `onMounted`, `ref`.
 *
 * State:
 * - `user` (ref<User | null>): Stores the current admin user's information.
 * - `foundUser` (ref<User | undefined>): Stores the currently selected user.
 * - `users` (ref<User[]>): Stores the list of all users.
 * - `isLoading` (ref<boolean>): Indicates whether the user data is being loaded.
 *
 * Methods:
 * - `searchUser()`: Searches for a user by username.
 * - `promoteUser()`: Promotes a user to admin.
 * - `demoteUser()`: Demotes an admin to a regular user.
 * - `deleteUser()`: Deletes a user from the system.
 * - `clickedUser(user: User)`: Loads the selected user's details.
 */

import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { type User, useUser } from '@/stores/user';
import { toast } from 'vue-sonner';
import { onMounted, ref } from 'vue';
import { Button } from '@/components/ui/button';
import { Card, CardDescription, CardTitle, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { RouterLink } from "vue-router";
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import DialogHeader from '@/components/ui/dialog/DialogHeader.vue';
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from '@/components/MobileSidebar.vue';

// State variables
let { user, setUser } = useUser();
let foundUser = ref<User>();
let users = ref<User[]>([]);
const isLoading = ref(true);

// Show a loading toast while user data is being fetched
toast.loading("Loading user data...", {
  duration: Infinity,
  id: "loading-data",
  dismissible: false
});

/**
 * Searches for a user by username.
 *
 * Displays a toast notification for the search process and updates `foundUser` with the result.
 */
const searchUser = async () => {
  const userInput = document.getElementById("username") as HTMLInputElement;
  if (userInput.value.length === 0) {
    toast.error("Please enter a username", {
      duration: 5000,
      id: "search-user"
    });
    return;
  }

  toast.loading("Searching for user...", {
    duration: Infinity,
    id: "search-user",
    dismissible: false
  });

  const res = await fetch(`/api/admin/users/${userInput.value}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });

  const data = await res.json();
  if (data.error) {
    toast.error("Failed to find user", {
      description: data.error,
      duration: 5000,
      id: "search-user",
      dismissible: true
    });
  } else {
    toast.success("Found user", {
      duration: 2000,
      id: "search-user",
      dismissible: true
    });
    foundUser.value = data;
  }

  userInput.value = "";
};

/**
 * Promotes a user to admin.
 *
 * Updates the `foundUser` state and displays a toast notification for the action.
 */
const promoteUser = async () => {
  toast.loading("Promoting user...", {
    duration: Infinity,
    id: "promoting-user",
    dismissible: false
  });

  const res = await fetch(`/api/admin/permissions/${foundUser.value?.["_id"]}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    }
  });

  const data = await res.json();
  if (data.error) {
    toast.error("Failed to promote user", {
      description: data.error,
      duration: 5000,
      id: "promoting-user",
      dismissible: true
    });
  } else {
    if (foundUser.value) {
      foundUser.value.admin = true;
    }
    toast.success("Promoted user", {
      duration: 2000,
      id: "promoting-user",
      dismissible: true
    });
  }
};

/**
 * Demotes an admin to a regular user.
 *
 * Updates the `foundUser` state and displays a toast notification for the action.
 */
const demoteUser = async () => {
  toast.loading("Demoting user...", {
    duration: Infinity,
    id: "demoting-user",
    dismissible: false
  });

  const res = await fetch(`/api/admin/permissions/${foundUser.value?.["_id"]}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json"
    }
  });

  const data = await res.json();
  if (data.error) {
    toast.error("Failed to demote user", {
      description: data.error,
      duration: 5000,
      id: "demoting-user",
      dismissible: true
    });
  } else {
    if (foundUser.value) {
      foundUser.value.admin = false;
    }
    toast.success("Demoted user", {
      duration: 2000,
      id: "demoting-user",
      dismissible: true
    });
  }
};

/**
 * Deletes a user from the system.
 *
 * Removes the user from the `users` list and displays a toast notification for the action.
 */
const deleteUser = async () => {
  toast.loading("Deleting user...", {
    duration: Infinity,
    id: "deleting-user",
    dismissible: false
  });

  const res = await fetch(`/api/admin/users/${foundUser.value?.username}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json"
    }
  });

  const data = await res.json();
  if (data.error) {
    toast.error("Failed to delete user", {
      description: data.error,
      duration: 5000,
      id: "deleting-user",
      dismissible: true
    });
  } else {
    toast.success("Deleted user", {
      duration: 2000,
      id: "deleting-user",
      dismissible: true
    });
    users.value = users.value.filter(u => u.username !== foundUser.value?.username);
    foundUser.value = undefined;
  }
};

/**
 * Loads the selected user's details.
 *
 * Updates the `foundUser` state and displays a loading toast.
 */
const clickedUser = (user: User) => {
  toast.loading("Loading user data...", {
    duration: 100,
    id: "loading-data",
  });
  setTimeout(() => {
    foundUser.value = user;
    toast.dismiss("loading-data");
  }, 400);
};

// Fetch user and admin data on component mount
onMounted(async () => {
  try {
    const res = await fetch("/api/user/me", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });
    const data = await res.json();

    const usersRes = await fetch("/api/admin/users", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });
    const usersData = await usersRes.json();
    users.value = usersData;

    if (!data.error) {
      setUser(data);
    }
    isLoading.value = false;
    toast.dismiss("loading-data");
  } catch (err) {
    console.error(err);
  }
});
</script>

<template>
  <div class="flex flex-row" v-if="!isLoading && user && user.admin">
    <!-- Sidebar -->
    <main class="flex h-screen items-center place-self-start">
      <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
        <Sidebar />
      </SidebarProvider>
      <MobileSidebar v-else />

      <!-- User list -->
      <div class="hidden sm:flex flex-col ml-10">
        <h1 class="text-4xl text-center mb-4">Users</h1>
        <ScrollArea class="w-80 h-[75vh] border rounded-lg">
          <div class="p-4">
            <div v-for="user in users" :key="user.username" @click="clickedUser(user)" class="cursor-pointer">
              {{ (user.first_name + " " + user.last_name) }} ({{ user?.username }})
              <Separator class="my-2" />
            </div>
          </div>
        </ScrollArea>
      </div>
      <Separator orientation="vertical" class="hidden sm:inline mx-10" />
    </main>

    <!-- Admin dashboard -->
    <div class="flex flex-col pt-10 pr-10">
      <Card class="w-full col-span-3 my-4">
        <CardHeader>
          <CardTitle class="text-3xl">Admin Dashboard</CardTitle>
          <CardDescription>To load a user, please enter their username below.</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="flex flex-row">
            <Input class="mr-2" id="username" placeholder="Username" />
            <Button @click="searchUser">Search</Button>
          </div>
        </CardContent>
      </Card>

      <!-- User details -->
      <Card class="max-w-[100vw] min-w-[100vw] w-[100vw]" v-if="foundUser">
        <CardHeader>
          <CardTitle class="text-2xl">Found <span class="text-cyan-500 font-semibold">{{ foundUser?.username }}</span>
          </CardTitle>
          <CardDescription class="text-lg">{{ foundUser?.first_name }} {{ foundUser?.last_name }}</CardDescription>
        </CardHeader>
        <CardContent class="w-screen text-wrap">
          <h1>User ID: <span class="text-cyan-500 font-semibold">{{ foundUser?.["_id"] }}</span></h1>
          <h1>Email: <span class="text-cyan-500 font-semibold">{{ foundUser?.email }}</span></h1>
          <h1 v-if="foundUser?.spotify_id">Spotify ID: <span class="text-cyan-500 font-semibold">{{
            foundUser?.spotify_id }}</span></h1>
          <h1 v-else class="text-cyan-500 underline">User hasn't linked Spotify</h1>
        </CardContent>
        <CardFooter>
          <div class="flex flex-row">
            <Button class="mr-2" @click="promoteUser" variant="success" v-if="!foundUser.admin">Promote</Button>
            <Button class="mr-2" @click="demoteUser" variant="warning" v-else>Demote</Button>
            <Dialog>
              <DialogTrigger as-child>
                <Button class="mr-2" variant="destructive">Delete</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Are you sure you want to delete <span class="text-cyan-500 font-semibold">{{
                      foundUser?.username }}</span>?</DialogTitle>
                  <DialogDescription>This action cannot be undone</DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <DialogClose as-child>
                    <Button @click="deleteUser" variant="destructive">Yes</Button>
                  </DialogClose>
                  <DialogClose as-child>
                    <Button variant="success">No</Button>
                  </DialogClose>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </CardFooter>
      </Card>
    </div>
  </div>

  <!-- Unauthorized access -->
  <div class="flex flex-row" v-else-if="!isLoading && !user?.admin">
    <div class="flex h-screen items-center place-self-start">
      <SidebarProvider :default-open="false" :open="false">
        <Sidebar />
      </SidebarProvider>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 items-center place-self-center">
        <h1 class="text-4xl text-nowrap">You are not <span class="text-red-500 font-semibold">authorized</span> to visit
          this page</h1>
        <Button as-child class="relative left-1/2 -translate-x-1/2 mt-4 text-2xl" size="lg">
          <RouterLink to="/">Back</RouterLink>
        </Button>
      </div>
    </div>
  </div>
</template>