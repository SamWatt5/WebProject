<script setup lang="ts">
import { ref } from "vue";

const seedArtists = ref("");
const seedGenres = ref("");
const seedTracks = ref("");
interface Track {
    id: string;
    name: string;
    album: {
        images: { url: string }[];
    };
    artists: { name: string }[];
    external_urls: { spotify: string };
}

const recommendations = ref<Track[]>([]);
const errorMessage = ref("");

const fetchRecommendations = async () => {
    errorMessage.value = "";
    recommendations.value = [];

    try {
        const response = await fetch(
            `/api/spotify/recommend?seed_artists=${seedArtists.value}&seed_genres=${seedGenres.value}&seed_tracks=${seedTracks.value}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if (!response.ok) {
            const errorData = await response.json();
            errorMessage.value = errorData.error || "Failed to fetch recommendations.";
            return;
        }

        const data = await response.json();
        recommendations.value = data.tracks || [];
    } catch (error) {
        errorMessage.value = "An error occurred while fetching recommendations.";
        console.error(error);
    }
};
</script>

<template>
    <div class="p-4">
        <h1 class="text-2xl font-bold mb-4">Spotify Recommendations</h1>
        <form @submit.prevent="fetchRecommendations" class="space-y-4">
            <div>
                <label for="seedArtists" class="block font-medium">Seed Artists (comma-separated IDs):</label>
                <input id="seedArtists" v-model="seedArtists" type="text" class="border rounded p-2 w-full"
                    placeholder="e.g., artist1,artist2" />
            </div>
            <div>
                <label for="seedGenres" class="block font-medium">Seed Genres (comma-separated):</label>
                <input id="seedGenres" v-model="seedGenres" type="text" class="border rounded p-2 w-full"
                    placeholder="e.g., pop,rock" />
            </div>
            <div>
                <label for="seedTracks" class="block font-medium">Seed Tracks (comma-separated IDs):</label>
                <input id="seedTracks" v-model="seedTracks" type="text" class="border rounded p-2 w-full"
                    placeholder="e.g., track1,track2" />
            </div>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
                Get Recommendations
            </button>
        </form>

        <div v-if="errorMessage" class="mt-4 text-red-500">
            {{ errorMessage }}
        </div>

        <div v-if="recommendations.length" class="mt-4">
            <h2 class="text-xl font-semibold">Recommendations:</h2>
            <ul class="list-disc pl-5">
                <li v-for="track in recommendations" :key="track.id" class="mb-4">
                    <div class="flex items-center space-x-4">
                        <img :src="track.album.images[0]?.url" alt="Album Art" class="w-16 h-16 rounded" />
                        <div>
                            <p class="font-medium">{{ track.name }}</p>
                            <p class="text-sm text-gray-600">
                                By {{track.artists.map(artist => artist.name).join(", ")}}
                            </p>
                            <a :href="track.external_urls.spotify" target="_blank" class="text-blue-500 underline">
                                Listen on Spotify
                            </a>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>