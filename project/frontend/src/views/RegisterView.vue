<script lang="ts" setup>
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from 'vee-validate';
import Darkmode from '@/components/Darkmode.vue';
import { use } from 'react';


const formSchema = toTypedSchema(z.object({
    firstName: z.string().nonempty({
        message: "First Name is required"
    }),
    lastName: z.string().nonempty({
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
        firstName: '',
        lastName: '',
        email: '',
        username: '',
        password: ''
    }
})

const onSubmit = form.handleSubmit(async (values) => {
    console.log(values);
})

const showPassword = () => {
    const passwordInput = document.getElementById("password") as HTMLInputElement;
    const passwordButton = document.getElementById("password-button") as HTMLButtonElement;
    if(passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordButton.textContent = "Hide Password";
    } else {
        passwordInput.type = "password";
        passwordButton.textContent = "Show Password";
    }
}
</script>

<template>
    <main>
        <Card class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 sm:w-1/2 w-[95%]">
            <CardHeader>
                <CardTitle><h1 class="text-3xl text-center">Register</h1></CardTitle>
                <!-- <CardDescription>Enter your credentials to Register</CardDescription> -->
            </CardHeader>
            <CardContent>
                <form @submit="onSubmit">
                    <FormField v-slot="{ componentField }" name="firstName">
                        <FormItem class="pb-4">
                            <FormLabel>First Name</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="First Name" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField v-slot="{ componentField }" name="lastName">
                        <FormItem class="pb-4">
                            <FormLabel>Last Name</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Last Name" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField v-slot="{ componentField }" name="email">
                        <FormItem class="pb-4">
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input type="email" placeholder="Email" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField v-slot="{ componentField }" name="username">
                        <FormItem class="pb-4">
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Username" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField class="mb-4" v-slot="{ componentField }" name="password">
                        <FormItem class="pb-4">
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input id="password" type="password" placeholder="Password" v-bind="componentField" />
                            </FormControl>
                            <FormDescription><Button id="password-button" @click="showPassword" type="button" variant="outline">Show Password</Button></FormDescription>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <Button type="submit" class="mt-4">Register</Button>
                    <Button type="button" class="mt-4" variant="link" @click="$router.push('/login')">Login</Button>
                </form>
            </CardContent>
            <CardFooter></CardFooter>
        </Card>
        <div class="absolute bottom-4 right-4">
            <Darkmode />
        </div>
    </main>
</template>
