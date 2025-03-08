<script lang="ts" setup>
import { Tooltip, TooltipContent, TooltipTrigger, TooltipProvider } from "../ui/tooltip";

defineProps({
    item: String
});
</script>

<template>
    <TooltipProvider>
        <Tooltip>
            <TooltipTrigger><slot></slot></TooltipTrigger>
            <TooltipContent class="ml-2" side="right">
                <div class="">
                    <p class="text-sm">{{ item }}</p>
                </div>
            </TooltipContent>
        </Tooltip>
    </TooltipProvider>
</template>