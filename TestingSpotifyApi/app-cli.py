import requests
import json
import base64
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests


load_dotenv()

CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:5000/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope="user-library-read"))


def filter_popular(track):
    return track["popularity"] > 0 and "GB" in track["availableCountries"]


def recommend():
    # Prompt user for seed parameters
    # seed_artists = input("Enter seed artists (comma-separated): ")
    # seed_genres = input("Enter seed genres (comma-separated): ")
    # seed_tracks = input("Enter seed tracks (comma-separated): ")
    seed_artists = "4NHQUGzhtTLFvgF5SZesLK"
    seed_genres = "classical,country"  # Valid genre
    seed_tracks = "0c6xIDDpzE81m2q797ordA"
    # Ensure at least one seed is provided
    if not (seed_artists or seed_genres or seed_tracks):
        print("Error: At least one seed parameter (artist, genre, or track) is required.")
        return
    try:

        url = "https://api.reccobeats.com/v1/track/recommendation?size=100&seeds=0PWgAyoxsjwGRuFSO0fyya,1qrpoAMXodY6895hGKoUpA,1j6gmK6u4WNI33lMZ8dC1s,5enxwA8aAbwZbf5qCHORXi"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_data = response.json()
        response_data_popular = list(
            filter(filter_popular, response_data["content"]))
        response_data_popular_sorted = sorted(
            response_data_popular, key=lambda x: int(x["popularity"]), reverse=True
        )

        track_titles = [[track["trackTitle"], track["artists"][0]["name"], track["popularity"]]
                        for track in response_data_popular_sorted]

        print(track_titles)
        # recommendations = sp.recommendations(
        #     seed_artists=seed_artists.split(","),
        #     seed_genres=seed_genres.split(","),
        #     seed_tracks=seed_tracks.split(",")
        #     # seed_artists=seed_artists.split(",") if seed_artists else [],
        #     # seed_genres=seed_genres.split(",") if seed_genres else [],
        #     # seed_tracks=seed_tracks.split(",") if seed_tracks else []
        # )
        # print(json.dumps(recommendations, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}")


# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results["items"]):
#     track = item["track"]
#     print(idx, track["artists"][0]["name"], " - ", track["name"])
recommend()
