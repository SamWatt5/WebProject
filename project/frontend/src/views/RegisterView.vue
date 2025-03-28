<script lang="ts" setup>
/**
 * RegisterView.vue
 *
 * A component for handling user registration functionality.
 *
 * Features:
 * - Provides a form for users to enter their first name, last name, email, username, and password.
 * - Validates the form inputs using `vee-validate` and `zod`.
 * - Displays toast notifications for successful or failed registration attempts.
 * - Automatically logs in the user upon successful registration.
 * - Includes a "Show Password" toggle for the password input field.
 * - Includes a dark mode toggle for theme switching.
 *
 * Dependencies:
 * - vee-validate: For form validation.
 * - zod: For schema-based validation.
 * - vue-sonner: For toast notifications.
 * - Custom UI components: Card, Input, Button, Darkmode.
 *
 * Methods:
 * - `onSubmit()`: Handles the form submission, registration, and login logic.
 * - `showPassword()`: Toggles the visibility of the password input field.
 */

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from 'vee-validate';
import Darkmode from '@/components/Darkmode.vue';
import { toast } from 'vue-sonner';

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
        fname: '',
        lname: '',
        email: '',
        username: '',
        password: ''
    }
});

/**
 * Handles the form submission, registration, and login logic.
 *
 * Sends the registration data to the backend API.
 * Automatically logs in the user upon successful registration.
 * Displays toast notifications for success or failure.
 */
const onSubmit = form.handleSubmit(async (values) => {
    const res = await fetch("/api/auth/signup", {
        method: "POST",
        body: JSON.stringify(values),
        headers: {
            "Content-Type": "application/json"
        }
    });
    let body = await res.json();
    if (res.ok) {
        toast.success('Registration successful', {
            description: 'Logging in...',
            duration: 5000
        });

        // Automatically log in the user
        const loginRes = await fetch("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({ username: values.username, password: values.password }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        let loginBody = await loginRes.json();
        if (loginRes.ok) {
            toast.success('Login successful', {
                description: 'Redirecting...',
                duration: 5000
            });
            setTimeout(() => {
                location.href = "/api/auth/callback?code=" + loginBody.code;
            }, 2000);
        } else {
            toast.error('Login attempt failed', {
                description: loginBody.error,
                duration: 5000
            });
        }
    } else {
        toast.error('Register attempt failed', {
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
        <!-- Registration card -->
        <Card class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 sm:w-1/2 w-[95%]">
            <CardHeader>
                <CardTitle>
                    <h1 class="text-3xl text-center">Register</h1>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <form @submit="onSubmit">
                    <!-- First Name field -->
                    <FormField v-slot="{ componentField }" name="fname">
                        <FormItem class="pb-4">
                            <FormLabel>First Name</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="First Name" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Last Name field -->
                    <FormField v-slot="{ componentField }" name="lname">
                        <FormItem class="pb-4">
                            <FormLabel>Last Name</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Last Name" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Email field -->
                    <FormField v-slot="{ componentField }" name="email">
                        <FormItem class="pb-4">
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input type="email" placeholder="Email" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Username field -->
                    <FormField v-slot="{ componentField }" name="username">
                        <FormItem class="pb-4">
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Username" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>

                    <!-- Password field -->
                    <FormField class="mb-4" v-slot="{ componentField }" name="password">
                        <FormItem class="pb-4">
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

                    <!-- Submit and Login buttons -->
                    <Button type="submit" class="mt-4">Register</Button>
                    <Button type="button" class="mt-4" variant="link" @click="$router.push('/login')">Login</Button>
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
