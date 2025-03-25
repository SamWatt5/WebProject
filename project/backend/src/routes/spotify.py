from dotenv import load_dotenv
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import redirect, session, request, jsonify
from flask_cors import CORS

from ..middleware import auth
from ..models import get_user_from_token
from flask_restx import Namespace, Resource

from ..models import add_jwt, link_spotify

# Load environment variables from .env file
load_dotenv()

# Define a namespace for Spotify-related routes
spotify_ns = Namespace("spotify", description="Spotify API routes")

# Spotify API credentials and redirect URI
CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://localhost:8000/api/spotify/callback"

# Define the required Spotify API scopes
scopes = "user-read-email playlist-read-private playlist-read-collaborative"

# Initialize Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=redirect_uri, scope=scopes)


@spotify_ns.route("/")
class HelloWorld(Resource):
    # A simple test route to verify the API is working
    def get(self):
        return "hello world! :)"


@spotify_ns.route("/recommend")
class RecommendRoute(Resource):
    @auth
    def get(user, self):
        # Log a debug message
        print("it HAS to work here... right?")

        # Get seed parameters from the query string
        seed_artists = request.args.get("seed_artists", "")
        seed_genres = request.args.get("seed_genres", "")
        seed_tracks = request.args.get("seed_tracks", "")

        print("ok so the error wasnt here then")

        # Ensure at least one seed parameter is provided
        if not (seed_artists or seed_genres or seed_tracks):
            return jsonify({"error": "At least one seed parameter (artist, genre, or track) is required"}), 400

        # Call Spotify's recommendations endpoint
        try:
            # Retrieve the Spotify access token from the session
            access_token = session.get("spotify_access_token")
            sp = spotipy.Spotify(auth=access_token)

            # Fetch recommendations based on the seed parameters
            recommendations = sp.recommendations(
                seed_artists=seed_artists.split(",") if seed_artists else None,
                seed_genres=seed_genres.split(",") if seed_genres else None,
                seed_tracks=seed_tracks.split(",") if seed_tracks else None
            )

            # Format the response to be JSON-serializable
            response = {
                "seeds": recommendations.get("seeds", []),
                "tracks": [
                    {
                        "id": track.get("id"),
                        "name": track.get("name"),
                        "album": {
                            "images": track.get("album", {}).get("images", []),
                            "name": track.get("album", {}).get("name"),
                        },
                        "artists": [
                            {"name": artist.get("name")}
                            for artist in track.get("artists", [])
                        ],
                        "external_urls": track.get("external_urls", {}),
                    }
                    for track in recommendations.get("tracks", [])
                ],
            }

            return jsonify(response)
        except spotipy.exceptions.SpotifyException as e:
            # Handle Spotify API errors
            return jsonify({"error": f"Spotify API error: {str(e)}"}), 500
        except Exception as e:
            # Handle general errors
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@spotify_ns.route("/me_playlists")
class MePlaylists(Resource):
    def get(self):
        # Retrieve the user's token from the session
        token = session.get("token")
        user = get_user_from_token(token)

        # Retrieve the Spotify access token from the user object
        access_token = user["spotify_token"]
        if not access_token:
            return jsonify({"msg": "Token not found"}), 401

        # Fetch the user's playlists from Spotify
        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user_playlists()
        return jsonify(results)


@spotify_ns.route("/playlist/<string:playlist_id>/tracks")
class PlaylistTracks(Resource):
    def get(self, playlist_id):
        # Retrieve the Spotify access token from the session
        access_token = session.get("spotify_access_token")
        if not access_token:
            return jsonify({"msg": "Token not found"}), 401

        # Fetch the tracks in the specified playlist
        sp = spotipy.Spotify(auth=access_token)
        results = sp.playlist_items(playlist_id)
        return jsonify(results)


@spotify_ns.route("/login")
class SpotifyLogin(Resource):
    def get(self):
        # Generate the Spotify authorization URL
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)


@spotify_ns.route("/callback")
class SpotifyCallback(Resource):
    def get(self):
        # Retrieve the authorization code from the query string
        code = request.args.get("code")
        print(code)
        if not code:
            return jsonify({"msg": "Authorization failed"}), 400

        # Exchange the authorization code for an access token
        token_info = sp_oauth.get_access_token(code)
        print(token_info)
        access_token = token_info["access_token"]

        # Fetch the user's Spotify account information
        sp = spotipy.Spotify(auth=access_token)
        user_info = sp.current_user()
        spotify_id = user_info.get("id")

        # Retrieve the user's token from the session
        token = session.get("token")

        # Link the Spotify account to the user's profile
        link_spotify(token, spotify_id, access_token)

        # Redirect the user to the recommendations page
        return redirect(f"http://localhost:8080/recommend")


@spotify_ns.route("/link-spotify")
class LinkSpotifyRoute(Resource):
    @jwt_required()
    def get(self):
        # Redirect the user to the Spotify login page
        return redirect("/api/spotify/login")
