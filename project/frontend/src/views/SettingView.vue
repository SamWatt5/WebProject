<script lang="ts" setup>
import { SidebarProvider } from '@/components/ui/sidebar';
import Sidebar from '@/components/Sidebar.vue';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from 'vee-validate';
import Darkmode from '@/components/Darkmode.vue';
import { toast } from 'vue-sonner';
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useUser } from '@/stores/user';
import { ref } from 'vue';

const { user } = storeToRefs(useUser());

const formSchema = toTypedSchema(z.object({
    fname: z.string().nonempty({
        message: "First Name is required"
    }),
    lname: z.string().nonempty({
        message: "Last Name is required"
    }),
    email: z.string().email({
        message: "Email is required"
    }),
    username: z.string().nonempty({
        message: "Username is required"
    }),
    password: z.string().nonempty({
        message: "Password is required"
    })
}));

const form = useForm({
    validationSchema: formSchema,
    initialValues: {
        fname: user.value?.first_name,
        lname: user.value?.last_name,
        email: user.value?.email,
        username: user.value?.username,
        password: ''
    }
});

const isReadonly = ref(true);

const onSubmit = form.handleSubmit(async (values) => {
    toast.loading('Saving user data...', {
        id: 'loadingMessage',
        dismissible: false
    })
    const res = await fetch("/api/auth/update", {
        method: "POST",
        body: JSON.stringify(values),
        headers: {
            "Content-Type": "application/json"
        }
    });
    let body = await res.json();
    if (res.ok) {
        toast.success('Account updated successfully', {
            description: 'Your changes have been saved.',
            duration: 5000,
            id: 'loadingMessage'
        });
    } else {
        toast.error('Update failed', {
            description: body.error,
            duration: 5000,
            id: 'loadingMessage'
        });
    }
});

const showPassword = () => {
    const passwordInput = document.getElementById("password") as HTMLInputElement;
    const passwordButton = document.getElementById("password-button") as HTMLButtonElement;
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordButton.textContent = "Hide Password";
    } else {
        passwordInput.type = "password";
        passwordButton.textContent = "Show Password";
    }
};


const deleteAccount = () => {
    const res = fetch("/api/auth/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });
    if (res.ok) {
        toast.success('Account deleted successfully', {
            description: 'Your account has been deleted.',
            duration: 5000
        });
        setTimeout(() => {
            location.href = "/";
        }, 2000);
    } else {
        toast.error('Delete failed', {
            description: 'An error occurred while deleting your account.',
            duration: 5000
        });
    }
};

const redirectToSpotifyLogin = () => {
    window.location.href = "/api/spotify/login"; // Redirect to Spotify login endpoint
};


</script>

<template>
    <main class="flex h-screen items-center place-self-start">
        <SidebarProvider :default-open="false" :open="false">
            <Sidebar />
        </SidebarProvider>

        <Card class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 sm:w-1/2 w-[95%]">
            <CardHeader>
                <CardTitle>
                    <h1 class="text-3xl text-center">Your account info</h1>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <form @submit="onSubmit">
                    <FormField v-slot="{ componentField }" name="fname">
                        <FormItem class="pb-4">
                            <FormLabel>First Name</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="First Name" v-bind="componentField"
                                    :readonly="isReadonly" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField v-slot="{ componentField }" name="lname">
                        <FormItem class="pb-4">
                            <FormLabel>Last Name</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Last Name" v-bind="componentField"
                                    :readonly="isReadonly" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField v-slot="{ componentField }" name="email">
                        <FormItem class="pb-4">
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input type="email" placeholder="Email" v-bind="componentField"
                                    :readonly="isReadonly" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField v-slot="{ componentField }" name="username">
                        <FormItem class="pb-4">
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Username" v-bind="componentField"
                                    :readonly="isReadonly" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField class="mb-4" v-slot="{ componentField }" name="password">
                        <FormItem class="pb-4">
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input id="password" type="password" placeholder="Password" v-bind="componentField"
                                    :readonly="isReadonly" />
                            </FormControl>
                            <FormDescription><Button id="password-button" @click="showPassword" type="button"
                                    variant="outline">Show Password</Button></FormDescription>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <Button type="submit" class="mt-4" @click="isReadonly = false">Edit</Button>
                    <Button type="button" class="mt-4" variant="link" @click="$router.push('/login')">Confirm & Save</Button>
                    
                </form>
                <Button @click="redirectToSpotifyLogin" class="float-right mt-4 bg-green-500 text-white px-4 py-2 rounded mb-4">
                    Login to Spotify
                </Button>
                <Button @click="deleteAccount" class="float-left  mt-4 bg-red-500 text-white px-4 py-2 rounded mb-4">
                    Delete Account
                </Button>
            </CardContent>
            <CardFooter></CardFooter>
        </Card>
        <div class="absolute bottom-4 right-4">

        </div>
    </main>
</template>
