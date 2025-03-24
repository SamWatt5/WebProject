<script setup lang="ts">
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { useUser } from '@/stores/user';
import { toast } from 'vue-sonner';
import { onMounted, ref } from 'vue';

const music: string[] = Array.from({ length: 50 }).map(
  (_, i) => `Song ${i + 1}`
);

let { user, setUser } = useUser();
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
        <h1 class="text-4xl text-center mb-4">Your Music</h1>
        <ScrollArea class="w-80 h-[75vh] border rounded-lg">
          <div class="p-4">
            <div v-for="song in music" :key="song">
              {{ song }}
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
  <div v-else-if="!isLoading && !user?.admin">
    <h1 class="text-4xl text-center">You are not authorized to view this page.</h1>
  </div>
</template>