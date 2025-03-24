<script setup lang="ts">
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { User, useUser } from '@/stores/user';
import { toast } from 'vue-sonner';
import { onMounted, ref } from 'vue';
import { Button } from '@/components/ui/button';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

let { user, setUser } = useUser();
let users = ref<User[]>([]);
const isLoading = ref(true);
toast.loading("Loading user data...", {
  duration: Infinity,
  id: "loading-data",
  dismissible: false
});

onMounted(async() => {
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
      console.log("Users", usersData);

      if(!data.error) {
        setUser(data);
        console.log("Set user successfully", data);
        user = data;
      }
      isLoading.value = false;
      toast.dismiss("loading-data");
    } catch(err) {
      console.error(err);
    }
});
</script>

<template>
  <div class="flex flex-row" v-if="!isLoading && user && user.admin">
    <main class="flex h-screen items-center place-self-start">
      <SidebarProvider :default-open="false" :open="false">
        <Sidebar />
      </SidebarProvider>

      <div class="flex flex-col ml-10">
        <h1 class="text-4xl text-center mb-4">Users</h1>
        <ScrollArea class="w-80 h-[75vh] border rounded-lg">
          <div class="p-4">
            <div v-for="user in users" :key="user.username">
              {{ (user.first_name + " " + user.last_name) }} ({{ user?.username }})
              <Separator class="my-2" />
            </div>
          </div>
        </ScrollArea>
      </div>
      <Separator orientation="vertical" class="mx-10" />
    </main>
    <div class="grid grid-cols-3 grid-rows-10 pt-10 gap-4">
      
    </div>
  </div>
  <div class="flex flex-row" v-else-if="!isLoading && !user?.admin">
    <div class="flex h-screen items-center place-self-start">
      <SidebarProvider :default-open="false" :open="false">
        <Sidebar />
      </SidebarProvider>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 items-center place-self-center">
        <h1 class="text-4xl text-nowrap">You are not <span class="text-red-500 font-semibold">authorised</span> to visit this page</h1>
        <Button as-child  class="relative left-1/2 -translate-x-1/2 mt-4 text-2xl" size="lg"><RouterLink to="/">Back</RouterLink></Button>
      </div>
    </div>
  </div>
</template>