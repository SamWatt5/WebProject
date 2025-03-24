import requests
import json
import base64
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:3000/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope="user-library-read"))


def recommend():
    # Prompt user for seed parameters
    seed_artists = input("Enter seed artists (comma-separated): ")
    seed_genres = input("Enter seed genres (comma-separated): ")
    seed_tracks = input("Enter seed tracks (comma-separated): ")

    # Ensure at least one seed is provided
    if not (seed_artists or seed_genres or seed_tracks):
        print("Error: At least one seed parameter (artist, genre, or track) is required.")
        return

    # Call Spotify's recommendations endpoint
    try:
        recommendations = sp.recommendations(
            seed_artists=seed_artists.split(",") if seed_artists else [],
            seed_genres=seed_genres.split(",") if seed_genres else [],
            seed_tracks=seed_tracks.split(",") if seed_tracks else []
        )
        print(json.dumps(recommendations, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}")


results = sp.current_user_saved_tracks()
for idx, item in enumerate(results["items"]):
    track = item["track"]
    print(idx, track["artists"][0]["name"], " - ", track["name"])
