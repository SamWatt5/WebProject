<script lang="ts" setup>
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from 'vee-validate';
import Darkmode from '@/components/Darkmode.vue';

const formSchema = toTypedSchema(z.object({
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
                <CardTitle><h1 class="text-3xl text-center">Login</h1></CardTitle>
                <!-- <CardDescription>Enter your credentials to login</CardDescription> -->
            </CardHeader>
            <CardContent>
                <form @submit="onSubmit">
                    <FormField v-slot="{ componentField }" name="username">
                        <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input type="text" placeholder="Username" v-bind="componentField" />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <FormField class="mb-4" v-slot="{ componentField }" name="password">
                        <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                                <Input id="password" type="password" placeholder="Password" v-bind="componentField" />
                            </FormControl>
                            <FormDescription><Button id="password-button" @click="showPassword" type="button" variant="outline">Show Password</Button></FormDescription>
                            <FormMessage />
                        </FormItem>
                    </FormField>
                    <Button type="submit" class="mt-4">Login</Button>
                </form>
            </CardContent>
            <CardFooter></CardFooter>
        </Card>
        <div class="absolute bottom-4 right-4">
            <Darkmode />
        </div>
    </main>
</template>