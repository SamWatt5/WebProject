<script setup lang="ts">
import { ref } from "vue";

// Define the structure of a track based on the response
interface Track {
    id: string;
    trackTitle: string;
    href: string;
    artists: { href: string; name: string }[];
    popularity: number;
    durationMs: number;
}

const seedTracks = ref(""); // Input for seed tracks
const friendId = ref(""); // Input for friend's ID
const recommendations = ref<Track[]>([]); // Store recommendations
const errorMessage = ref(""); // Store error messages
const successMessage = ref(""); // Store success messages

const fetchRecommendations = async () => {
    errorMessage.value = "";
    successMessage.value = "";
    recommendations.value = [];

    try {
        const response = await fetch(
            `/api/spotify/recommend?seed_tracks=${seedTracks.value}`, // Query parameter for seed tracks
            {
                method: "GET",
                credentials: "include",
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
        // Map the response to match the Track interface
        recommendations.value = data.recommendations.map((track: any) => ({
            id: track.href.split("/").pop(),
            trackTitle: track.trackTitle,
            href: track.href,
            artists: track.artists,
            popularity: track.popularity,
            durationMs: track.durationMs,
        }));
    } catch (error) {
        errorMessage.value = "An error occurred while fetching recommendations.";
        console.error(error);
    }
};

const fetchBlend = async () => {
    errorMessage.value = "";
    successMessage.value = "";
    recommendations.value = [];

    try {
        const response = await fetch(
            `/api/spotify/blend?friend_id=${friendId.value}`, // Query parameter for friend's ID
            {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if (!response.ok) {
            const errorData = await response.json();
            errorMessage.value = errorData.error || "Failed to fetch blended playlist.";
            return;
        }

        const data = await response.json();
        // Map the response to match the Track interface
        recommendations.value = data.playlist.map((track: any) => ({
            id: track.id,
            trackTitle: track.title,
            href: track.link,
            artists: [{ href: "", name: track.artist }], // Assuming a single artist for simplicity
            popularity: 0, // Popularity is not provided in the response
            durationMs: 0, // Duration is not provided in the response
        }));
    } catch (error) {
        errorMessage.value = "An error occurred while fetching the blended playlist.";
        console.error(error);
    }
}

const createPlaylist = async () => {
    errorMessage.value = "";
    successMessage.value = "";

    // Extract the track IDs from the recommendations
    const trackIds = recommendations.value.map((track) => track.id);

    try {
        const response = await fetch("/api/spotify/create_playlist", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ track_ids: trackIds }), // Send track IDs in the request body
        });

        if (!response.ok) {
            const errorData = await response.json();
            errorMessage.value = errorData.error || "Failed to create playlist.";
            return;
        }

        successMessage.value = "Playlist created successfully!";
    } catch (error) {
        errorMessage.value = "An error occurred while creating the playlist.";
        console.error(error);
    }
};

const redirectToSpotifyLogin = () => {
    window.location.href = "/api/spotify/login"; // Redirect to Spotify login endpoint
};
</script>

<template>
    <div class="p-4">
        <h1 class="text-2xl font-bold mb-4">Spotify Recommendations</h1>

        <!-- Button to login to Spotify -->
        <button @click="redirectToSpotifyLogin" class="bg-green-500 text-white px-4 py-2 rounded mb-4">
            Login to Spotify
        </button>

        <form @submit.prevent="fetchBlend" class="space-y-4">
            <div>
                <label for="seedTracks" class="block font-medium">Friend ID:</label>
                <input id="seedTracks" v-model="friendId" type="text" class="border rounded p-2 w-full"
                    placeholder="Enter Friend ID" />
            </div>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
                Get Blended Playlist
            </button>
        </form>

        <div v-if="errorMessage" class="mt-4 text-red-500">
            {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="mt-4 text-green-500">
            {{ successMessage }}
        </div>

        <div v-if="recommendations.length" class="mt-4">
            <h2 class="text-xl font-semibold">Blended Playlist:</h2>
            <ul class="list-disc pl-5">
                <li v-for="track in recommendations" :key="track.id" class="mb-4">
                    <div class="flex flex-col space-y-2">
                        <p class="font-medium text-lg">{{ track.trackTitle }}</p>
                        <p class="text-sm text-gray-600">
                            By:
                            <span v-for="(artist, index) in track.artists" :key="artist.href">
                                <a :href="artist.href" target="_blank" class="text-blue-500 underline">
                                    {{ artist.name }}
                                </a>
                                <span v-if="index < track.artists.length - 1">, </span>
                            </span>
                        </p>
                        <p class="text-sm text-gray-600">Popularity: {{ track.popularity }}</p>
                        <p class="text-sm text-gray-600">Duration: {{ (track.durationMs / 60000).toFixed(2) }} minutes
                        </p>
                        <a :href="track.href" target="_blank" class="text-blue-500 underline">
                            Listen on Spotify
                        </a>
                    </div>
                </li>
            </ul>

            <!-- Button to create a playlist -->
            <button @click="createPlaylist" class="bg-green-500 text-white px-4 py-2 rounded mt-4">
                Create Playlist
            </button>
        </div>
    </div>
</template>