<script lang="ts" setup>
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card";
import PeopleWatching from "./images/PeopleWatching.vue";
import { defineProps } from "vue";

interface Props {
    title: string,
    artist: string,
    coverImage: string,
    link: string
}

const props = defineProps<Props>()
</script>


<template>
    <div>
        <a :href="props.link">
            <Card>
                <CardHeader>

                </CardHeader>
                <CardContent class="flex flex-row items-center">
                    <img :src="props.coverImage" alt="Cover" class="w-16 h-16" />
                    <div class="ml-4">
                        {{ props.title }}
                        <CardDescription>{{ props.artist }}</CardDescription>
                    </div>
                </CardContent>
            </Card>
        </a>
    </div>
</template>