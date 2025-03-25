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

load_dotenv()

spotify_ns = Namespace("spotify", description="Spotify API routes")

CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://localhost:8000/api/spotify/callback"

scopes = "user-read-email playlist-read-private playlist-read-collaborative"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=redirect_uri, scope=scopes)


@spotify_ns.route("/")
class HelloWorld(Resource):
    def get(self):
        return "hello world! :)"


@spotify_ns.route("/recommend")
class RecommendRoute(Resource):
    @auth
    def get(user, self):
        print("it HAS to work here... right?")
        # Get seed parameters from query string
        seed_artists = request.args.get("seed_artists", "")
        seed_genres = request.args.get("seed_genres", "")
        seed_tracks = request.args.get("seed_tracks", "")

        print("ok so the error wasnt here then")

        # Ensure at least one seed is provided
        if not (seed_artists or seed_genres or seed_tracks):
            return jsonify({"error": "At least one seed parameter (artist, genre, or track) is required"}), 400

        # Call Spotify's recommendations endpoint
        try:
            # Fetch recommendations from Spotify
            print("no problem here1")
            recommendations = sp_oauth.recommendations(
                seed_artists=seed_artists.split(",") if seed_artists else None,
                seed_genres=seed_genres.split(",") if seed_genres else None,
                seed_tracks=seed_tracks.split(",") if seed_tracks else None
            )
            print("No problem here2")

            print(f"\n\n{recommendations}\n\n")

            # Convert the response to a JSON-serializable format
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
            print("no problem here3")

            return jsonify(response)
        except spotipy.exceptions.SpotifyException as e:
            return jsonify({"error": f"Spotify API error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@spotify_ns.route("/me_playlists")
class MePlaylists(Resource):
    def get(self):
        token = session.get("token")
        user = get_user_from_token(token)
        access_token = user["spotify_token"]
        if not access_token:
            return jsonify({"msg": "Token not found"}), 401

        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user_playlists()
        return jsonify(results)


@spotify_ns.route("/playlist/<string:playlist_id>/tracks")
class PlaylistTracks(Resource):
    def get(self, playlist_id):
        access_token = session.get("spotify_access_token")
        if not access_token:
            return jsonify({"msg": "Token not found"}), 401

        sp = spotipy.Spotify(auth=access_token)
        results = sp.playlist_items(playlist_id)
        return jsonify(results)


@spotify_ns.route("/login")
class SpotifyLogin(Resource):
    def get(self):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)


@spotify_ns.route("/callback")
class SpotifyCallback(Resource):
    def get(self):
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

        link_spotify(token, spotify_id, access_token)

        # Redirect to your frontend profile page with the JWT token
        return redirect(f"http://localhost:5500/project/backend/profile.html")


@spotify_ns.route("/link-spotify")
class LinkSpotifyRoute(Resource):
    @jwt_required()
    def get(self):
        return redirect("/api/spotify/login")
