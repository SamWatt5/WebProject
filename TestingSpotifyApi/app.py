from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)

CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"

scopes = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope=scopes))


@app.route("/")
def hello_world():
    return "hello world! :)"


@app.route("/callback")
def callback():
    return redirect("http://127.0.0.1:5500/index.html")


@app.route("/recommend")
def recommend():
    # Get seed parameters from query string
    seed_artists = request.args.get("seed_artists", "")
    seed_genres = request.args.get("seed_genres", "")
    seed_tracks = request.args.get("seed_tracks", "")

    # Ensure at least one seed is provided
    if not (seed_artists or seed_genres or seed_tracks):
        return jsonify({"error": "At least one seed parameter (artist, genre, or track) is required"}), 400

    # Call Spotify's recommendations endpoint
    try:
        recommendations = sp.recommendations(
            seed_artists=seed_artists.split(","),
            seed_genres=seed_genres.split(","),
            seed_tracks=seed_tracks.split(",")
        )
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/me_playlists")
def me_playlists():
    results = sp.current_user_playlists()
    return results


@app.route("/playlist/<playlist_id>/tracks")
def playlist(playlist_id):
    results = sp.playlist_items(playlist_id)
    return results
