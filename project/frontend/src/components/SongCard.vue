<script lang="ts" setup>
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card";
import PeopleWatching from "./images/PeopleWatching.vue";
</script>


<template>
    <div>
        <Card>
            <CardHeader>
                
            </CardHeader>
            <CardContent class="flex flex-row items-center">
                <PeopleWatching />
                <div class="ml-4">
                    Rein Me In
                    <CardDescription>Sam Fender</CardDescription>
                </div>
            </CardContent>
        </Card>
    </div>
</template>