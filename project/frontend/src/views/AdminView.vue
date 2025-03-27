<script setup lang="ts">
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
import { isWorker } from '@vueuse/core';
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import DialogHeader from '@/components/ui/dialog/DialogHeader.vue';

let { user, setUser } = useUser();
let foundUser = ref<User>();
let users = ref<User[]>([]);
const isLoading = ref(true);
toast.loading("Loading user data...", {
  duration: Infinity,
  id: "loading-data",
  dismissible: false
});

const searchUser = async () => {
  const user = document.getElementById("username") as HTMLInputElement;
  if(user.value.length == 0) {
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

  const res = await fetch(`/api/admin/users/${user.value}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });

  const data = await res.json();
  if(data.error) {
    toast.error("Failed to find user", {
      description: data.error,
      duration: 5000,
      id: "search-user",
      dismissible: true
    });
    setTimeout(() => {
      toast.dismiss("search-user");
    }, 2000);
  } else {
    toast.success("Found user", {
      description: "",
      duration: 2000,
      id: "search-user",
      dismissible: true
    });

    setTimeout(() => {
      toast.dismiss("search-user");
    }, 2000);
    foundUser.value = data;
  }

  user.value = "";
}

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

const clickedUser = (user: User) => {
  toast.loading("Loading user data...", {
    duration: 100,
    id: "loading-data",
  });
  setTimeout(() => {
    foundUser.value = user;
    toast.dismiss("loading-data");
  }, 400)
}

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
  console.log(data);
  if(data.error) {
    toast.error("Failed to promote user", {
      description: data.error,
      duration: 5000,
      id: "promoting-user",
      dismissible: true
    });
    setTimeout(() => {
      toast.dismiss("promoting-user");
    }, 5000);
  } else {
    if (foundUser.value) {
      foundUser.value.admin = true;
    }
    toast.success("Promoted user", {
      description: "",
      duration: 2000,
      id: "promoting-user",
      dismissible: true
    });
    setTimeout(() => {
      toast.dismiss("promoting-user");
    }, 2000);
  }
}

const demoteUser = async() => {
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
  if(data.error) {
    toast.error("Failed to demote user", {
      description: data.error,
      duration: 5000,
      id: "demoting-user",
      dismissible: true
    });
    setTimeout(() => {
      toast.dismiss("demoting-user");
    }, 5000);
  } else {
    if (foundUser.value) {
      foundUser.value.admin = false;
    }
    toast.success("Demoted user", {
      description: "",
      duration: 2000,
      id: "demoting-user",
      dismissible: true
    });
    setTimeout(() => {
      toast.dismiss("demoting-user");
    }, 2000);
  }
}

const deleteUser = async() => {
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
  if(data.error) {
    toast.error("Failed to delete user", {
      description: data.error,
      duration: 5000,
      id: "deleting-user",
      dismissible: true
    });
    setTimeout(() => {
      toast.dismiss("deleting-user");
    }, 5000);
  } else {
    toast.success("Deleted user", {
      description: "",
      duration: 2000,
      id: "deleting-user",
      dismissible: true
    });
    users.value = users.value.filter(u => u.username !== foundUser.value?.username);
    foundUser.value = undefined;
    setTimeout(() => {
      toast.dismiss("deleting-user");
    }, 2000);
  }
}
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
            <div v-for="user in users" :key="user.username" @click="clickedUser(user)" class="cursor-pointer">
              {{ (user.first_name + " " + user.last_name) }} ({{ user?.username }})
              <Separator class="my-2" />
            </div>
          </div>
        </ScrollArea>
      </div>
      <Separator orientation="vertical" class="mx-10" />
    </main>
    <div class="flex flex-col pt-10 pr-10">
      <Card class="w-full col-span-3 my-4">
        <CardHeader>
          <CardTitle class="text-3xl">Admin Dashboard</CardTitle>
          <CardDescription>To load a user, please enter their username in below.</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="flex flex-row">
            <Input class="mr-2" id="username" placeholder="Username"/>
            <Button @click="searchUser">Search</Button>
          </div>
        </CardContent>
      </Card>
      <Card class="w-full" v-if="foundUser">
        <CardHeader>
          <CardTitle class="text-2xl">Found <span class="text-cyan-500 font-semibold">{{ foundUser?.username }}</span></CardTitle>
          <CardDescription class="text-lg">{{ foundUser?.first_name }} {{ foundUser?.last_name }}</CardDescription>
        </CardHeader>
        <CardContent>
          <h1>User ID: <span class="text-cyan-500 font-semibold">{{ foundUser?.["_id"] }}</span></h1>
          <h1>Email: <span class="text-cyan-500 font-semibold">{{ foundUser?.email }}</span></h1>
          <h1 v-if="foundUser?.spotify_token">Spotify ID: <span class="text-cyan-500 font-semibold">{{ foundUser?.spotify_id }}</span></h1>
          <h1 v-if="foundUser?.spotify_token">Spotify Token: <span class="text-cyan-500 font-semibold">{{ foundUser?.spotify_token }}</span></h1>
          <h1 v-else class="text-cyan-500 underline">User hasn't linked spotify</h1>

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
                  <DialogTitle>Are you sure you want to delete <span class="text-cyan-500 font-semibold">{{ foundUser?.username }}</span>?</DialogTitle>
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