<script lang="ts" setup>
/**
 * SettingView.vue
 *
 * A component for managing user account settings.
 *
 * Features:
 * - Displays the user's account information (first name, last name, email, username, and password).
 * - Allows users to edit and save their account information.
 * - Provides a "Show Password" toggle for the password input field.
 * - Allows users to delete their account.
 * - Includes a button to link the user's Spotify account.
 * - Redirects unauthorized users to the login page.
 *
 * Dependencies:
 * - vee-validate: For form validation.
 * - zod: For schema-based validation.
 * - vue-sonner: For toast notifications.
 * - Custom UI components: Sidebar, Card, Input, Button, Darkmode.
 *
 * Methods:
 * - `onSubmit()`: Handles the form submission and updates the user's account information.
 * - `showPassword()`: Toggles the visibility of the password input field.
 * - `deleteAccount()`: Deletes the user's account.
 * - `redirectToSpotifyLogin()`: Redirects the user to Spotify login.
 */

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
import { onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useUser } from '@/stores/user';
import { useIsMobile } from '@/hooks/use-mobile';
import MobileSidebar from '@/components/MobileSidebar.vue';
import router from '@/router';

// Access the user store
const { user } = storeToRefs(useUser());

// Define the form schema using zod
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

// Initialize the form with validation schema and default values
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

// Reactive state for read-only mode
const isReadonly = ref(true);

/**
 * Handles the form submission and updates the user's account information.
 */
const onSubmit = form.handleSubmit(async (values) => {
    toast.loading('Saving user data...', {
        id: 'loadingMessage',
        dismissible: false
    });
    const res = await fetch("/api/auth/update", {
        method: "POST",
        body: JSON.stringify(values),
        headers: {
            "Content-Type": "application/json"
        }
    });
    const body = await res.json();
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

/**
 * Toggles the visibility of the password input field.
 */
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

/**
 * Deletes the user's account.
 */
const deleteAccount = async () => {
    const res = await fetch("/api/user/me", {
        method: "DELETE",
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

/**
 * Redirects the user to Spotify login.
 */
const redirectToSpotifyLogin = () => {
    window.location.href = "/api/spotify/login"; // Redirect to Spotify login endpoint
};

// Redirect unauthorized users to the login page
onMounted(() => {
    if (!user.value) {
        router.push("/login");
    }
});
</script>

<template>
    <main class="flex h-screen items-center place-self-start">
        <!-- Sidebar -->
        <SidebarProvider v-if="!useIsMobile()" :default-open="false" :open="false">
            <Sidebar />
        </SidebarProvider>
        <MobileSidebar v-else />

        <!-- Account settings card -->
        <Card class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 sm:w-1/2 w-[95%]">
            <CardHeader>
                <CardTitle>
                    <h1 class="text-3xl text-center">Your account info</h1>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <form @submit="onSubmit">
                    <!-- First Name field -->
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

                    <!-- Last Name field -->
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

                    <!-- Email field -->
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

                    <!-- Username field -->
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

                    <!-- Password field -->
                    <FormField class="mb-4" v-slot="{ componentField }" name="password">
                        <FormItem class="pb-4">
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input id="password" type="password" placeholder="Password" v-bind="componentField"
                                    :readonly="isReadonly" />
                            </FormControl>
                            <FormDescription>
                                <Button id="password-button" @click="showPassword" type="button" variant="outline">
                                    Show Password
                                </Button>
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Edit and Save buttons -->
                    <Button type="button" class="mt-4" @click="isReadonly = false">Edit</Button>
                    <Button type="submit" class="mt-4" variant="link">Confirm & Save</Button>
                </form>

                <!-- Spotify login and account deletion buttons -->
                <Button @click="redirectToSpotifyLogin"
                    class="float-right mt-4 bg-green-500 text-white px-4 py-2 rounded mb-4">
                    Login to Spotify
                </Button>
                <Button @click="deleteAccount" class="float-left mt-4 bg-red-500 text-white px-4 py-2 rounded mb-4">
                    Delete Account
                </Button>
            </CardContent>
            <CardFooter></CardFooter>
        </Card>
    </main>
</template>
