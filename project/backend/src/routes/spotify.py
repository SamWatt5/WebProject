from dotenv import load_dotenv
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, session, request, jsonify, Blueprint
from flask_cors import CORS

from ..middleware import auth
from ..models import get_user_from_token
from flask_restx import Namespace, Resource

from ..models import add_jwt, link_spotify

load_dotenv()

# spotify_bp = Blueprint('spotify', __name__)
spotify_ns = Namespace("spotify", description="Spotify API routes")

CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://localhost:8000/api/spotify/callback"

scopes = "user-read-email playlist-read-private playlist-read-collaborative"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=redirect_uri, scope=scopes)


@spotify_bp.route("/")
def hello_world():
    return "hello world! :)"


@spotify_ns.route("/recommend")
class recommend_route(Resource):
    @auth
    def get(user, self):
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


@spotify_bp.route("/me_playlists")
def me_playlists():
    token = session.get("token")
    user = get_user_from_token(token)
    access_token = user["spotify_token"]
    if not access_token:
        return jsonify({"msg": "Token not found"}), 401

    sp = spotipy.Spotify(auth=access_token)
    results = sp.current_user_playlists()
    return jsonify(results)


@spotify_bp.route("/playlist/<playlist_id>/tracks")
def playlist(playlist_id):
    access_token = session.get("spotify_access_token")
    if not access_token:
        return jsonify({"msg": "Token not found"}), 401

    sp = spotipy.Spotify(auth=access_token)
    results = sp.playlist_items(playlist_id)
    return jsonify(results)


@spotify_bp.route("/login")
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@spotify_bp.route("/callback")
def spotify_callback():
    code = request.args.get("code")
    print(code)
    if not code:
        return jsonify({"msg": "Authorization failed"}), 400

    token_info = sp_oauth.get_access_token(code)
    print(token_info)
    access_token = token_info["access_token"]

    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.current_user()
    spotify_id = user_info.get("id")
    # Assuming email is passed as a query parameter
    token = session.get("token")

    # session["email"] = email
    # session["spotify_access_token"] = access_token

    link_spotify(token, spotify_id, access_token)

    # Redirect to your frontend profile page with the JWT token
    return redirect(f"http://localhost:5500/project/backend/profile.html")


@spotify_bp.route("/link-spotify")
@jwt_required()
def link_spotify_route():
    return redirect("/api/spotify/login")
