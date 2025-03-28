<script setup lang="ts">
/**
 * Darkmode.vue
 *
 * A component that provides a dropdown menu to toggle between light, dark, and system themes.
 *
 * Features:
 * - Allows users to select a theme (light, dark, or system).
 * - Uses VueUse's `useColorMode` for managing the color mode.
 * - Includes a button with icons that dynamically change based on the selected theme.
 *
 * Dependencies:
 * - @vueuse/core: For `useColorMode` composable.
 * - @iconify/vue: For theme icons.
 * - Custom UI components: Button and DropdownMenu.
 */

// Import required components and utilities
import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuTrigger, DropdownMenuSeparator } from '@/components/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import { useColorMode } from '@vueuse/core'

// Initialize the color mode composable
const mode = useColorMode()
</script>

<template>
  <!-- Dropdown menu for theme selection -->
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <!-- Button with dynamic icons for light and dark modes -->
      <Button variant="outline" class="rounded-full p-2 m-1">
        <Icon icon="radix-icons:sun"
          class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
        <Icon icon="radix-icons:moon"
          class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        <span class="sr-only">Toggle theme</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuLabel>Theme Selector</DropdownMenuLabel>
      <DropdownMenuSeparator />
      <!-- Theme options -->
      <DropdownMenuItem @click="mode = 'light'">
        Light
      </DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'dark'">
        Dark
      </DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'auto'">
        System
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>