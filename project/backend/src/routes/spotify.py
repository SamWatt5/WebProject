from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask
from flask_cors import CORS
from flask import Blueprint, request, jsonify


load_dotenv()

spotify_bp = Blueprint('spotify', __name__)

CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"

scopes = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope=scopes))


@spotify_bp.route("/")
def hello_world():
    return "hello world! :)"


@spotify_bp.route("/me_playlists")
def me_playlists():
    results = sp.current_user_playlists()
    return results


@spotify_bp.route("/playlist/<playlist_id>/tracks")
def playlist(playlist_id):
    results = sp.playlist_items(playlist_id)
    return results
