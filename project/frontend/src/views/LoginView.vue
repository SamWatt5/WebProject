<script lang="ts" setup>
/**
 * LoginView.vue
 *
 * A component for handling user login functionality.
 *
 * Features:
 * - Provides a form for users to enter their username and password.
 * - Validates the form inputs using `vee-validate` and `zod`.
 * - Displays toast notifications for successful or failed login attempts.
 * - Includes a "Show Password" toggle for the password input field.
 * - Redirects the user to the appropriate page upon successful login.
 * - Includes a dark mode toggle for theme switching.
 *
 * Dependencies:
 * - vee-validate: For form validation.
 * - zod: For schema-based validation.
 * - vue-sonner: For toast notifications.
 * - Custom UI components: Card, Input, Button, Darkmode.
 *
 * Methods:
 * - `onSubmit()`: Handles the form submission and login logic.
 * - `showPassword()`: Toggles the visibility of the password input field.
 */

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from 'vee-validate';
import Darkmode from '@/components/Darkmode.vue';
import { toast } from 'vue-sonner';

// Define the form schema using zod
const formSchema = toTypedSchema(z.object({
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
        username: '',
        password: ''
    }
});

/**
 * Handles the form submission and login logic.
 *
 * Sends the username and password to the backend API for authentication.
 * Displays toast notifications for success or failure.
 */
const onSubmit = form.handleSubmit(async (values) => {
    let res = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(values)
    });
    let body = await res.json();
    if (body.code) {
        toast.success('Login successful', {
            description: 'Redirecting...',
            duration: 5000
        });
        setTimeout(() => {
            location.href = "/api/auth/callback?code=" + body.code;
        }, 2000);
    } else {
        toast.error('Login attempt failed', {
            description: body.error,
            duration: 5000
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
</script>

<template>
    <main>
        <!-- Login card -->
        <Card class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 sm:w-1/2 w-[95%]">
            <CardHeader>
                <CardTitle>
                    <h1 class="text-3xl text-center">Login</h1>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <form @submit="onSubmit">
                    <!-- Username field -->
                    <FormField v-slot="{ componentField }" name="username">
                        <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Username" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Password field -->
                    <FormField class="mb-4" v-slot="{ componentField }" name="password">
                        <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input id="password" type="password" placeholder="Password" v-bind="componentField" />
                            </FormControl>
                            <FormDescription>
                                <Button id="password-button" @click="showPassword" type="button" variant="outline">
                                    Show Password
                                </Button>
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Submit and Register buttons -->
                    <Button type="submit" class="mt-4">Login</Button>
                    <Button type="button" class="mt-4" variant="link"
                        @click="$router.push('/register')">Register</Button>
                </form>
            </CardContent>
            <CardFooter></CardFooter>
        </Card>

        <!-- Dark mode toggle -->
        <div class="absolute bottom-4 right-4">
            <Darkmode />
        </div>
    </main>
</template>