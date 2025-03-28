from random import random
from dotenv import load_dotenv
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import redirect, session, request, jsonify
from flask_cors import CORS

from ..middleware import auth
from ..models import find_user_by_username, get_user_from_token, filter_popular, refresh_spotify, find_user
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
scopes = "user-read-email playlist-read-private playlist-read-collaborative, playlist-modify-public playlist-modify-private, user-top-read, user-read-recently-played"

# Initialize Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=redirect_uri, scope=scopes)


def refreshToken(user):
    """
    Refresh the Spotify access token for a user.

    Args:
        user (dict): The user object containing the refresh token.

    Returns:
        dict: The refreshed token information.
    """
    print(user)
    refreshed = sp_oauth.refresh_access_token(user["spotify_refresh_token"])
    refresh_spotify(user["_id"], refreshed["access_token"],
                    refreshed["refresh_token"])

    return refreshed


@spotify_ns.route("/")
class HelloWorld(Resource):
    """
    A simple test route to verify the API is working.
    """

    def get(self):
        """
        Returns a test message.

        Returns:
            str: A test message.
        """
        return "hello world! :)"


@spotify_ns.route("/recommend")
class RecommendRoute(Resource):
    """
    Endpoint to get track recommendations using an external API.
    """

    def request_reccobeats(self, url):
        """
        Makes a request to the Reccobeats API.

        Args:
            url (str): The API URL.

        Returns:
            dict: The response data from the API.
        """
        payload = {}
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response JSON
        response_data = response.json()
        return response_data

    @auth
    def get(user, self):
        """
        Fetches track recommendations based on seed tracks.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: A JSON response with recommendations or an error message.
        """
        print("HERE")
        seed_tracks = request.args.get("seed_tracks", "")
        if not seed_tracks:
            return jsonify({"error": "Seed tracks are required"}), 400

        try:
            recommend_url = f"https://api.reccobeats.com/v1/track/recommendation?size=100&seeds={seed_tracks}"
            recommend_data = self.request_reccobeats(recommend_url)
            recommend_data_popular = list(
                filter(filter_popular, recommend_data.get("content", []))
            )

            ids = [track.get("href").split("/")[-1]
                   for track in recommend_data_popular if "href" in track]
            ids_string = ",".join(ids)

            return jsonify({
                "recommendations": recommend_data_popular,
                "ids": ids_string
            })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recommendations: {e}")
            return jsonify({"error": "Failed to fetch recommendations"}), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500


@spotify_ns.route("/create_playlist")
class CreatePlaylist(Resource):
    """
    Endpoint to create a new Spotify playlist.
    """
    @auth
    def post(user, self):
        """
        Creates a new playlist with the provided track IDs.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: A success message with playlist details or an error response.
        """
        data = request.get_json()
        print(data)
        tracks = data.get("track_ids")
        if not tracks:
            return {"error": "No track IDs provided"}, 400

        access_token = user["spotify_token"]
        if not access_token:
            return {"msg": "Token not found"}, 401

        try:
            sp = spotipy.Spotify(auth=access_token)
            user_id = sp.current_user()["id"]
            playlist_name = f"Generated Playlist"
            playlist_description = "A playlist generated by the app"
            playlist = sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                description=playlist_description,
                public=False
            )

            track_uris = [f"spotify:track:{track}" for track in tracks]
            sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)

            return {
                "message": "Playlist created successfully!",
                "playlist_id": playlist["id"],
                "playlist_name": playlist_name,
                "playlist_description": playlist_description
            }, 201
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {e}")
            return {"error": "Failed to create playlist"}, 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "An unexpected error occurred"}, 500


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


@spotify_ns.route("/blend")
class Blend(Resource):
    """
    Endpoint to blend playlists between the user and a friend.
    """
    @auth
    def get(user, self):
        """
        Blends playlists between the authenticated user and a friend.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: A JSON response with the blended playlist or an error message.
        """
        # Retrieve the friend's ID from the query parameters
        friend_id = request.args.get("friend_id")
        if not friend_id:
            return {"error": "Friend ID is required"}, 400

        sp = spotipy.Spotify(auth=user["spotify_token"])
        try:
            sp.me()
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                refreshToken(user)

        temp = find_user(friend_id, True)
        print(temp)

        if not temp:
            return {"error": "Friend not found"}, 404

        if not "spotify_token" in temp:
            return {"error": "Friend's Spotify account not linked"}, 404

        sp = spotipy.Spotify(auth=temp["spotify_token"])
        try:
            sp.me()
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                refreshed = refreshToken(temp)
                temp["spotify_token"] = refreshed["access_token"]
                sp = spotipy.Spotify(auth=refreshed["access_token"])

        # Call the blend method with the friend's ID
        return self.blend(user, friend_id)

    def get_playlist_tracks(self, user, spotipy_returned):
        """
        Retrieves all tracks from the user's playlists.

        Args:
            user (dict): The authenticated user.
            spotipy_returned (dict): The playlists returned by the Spotify API.

        Returns:
            list: A list of tracks from the user's playlists.
        """
        access_token = user["spotify_token"]
        if not access_token:
            return {"msg": "Token not found"}, 401

        # Initialize Spotify client
        sp = spotipy.Spotify(auth=access_token)
        user_tracks = []
        for playlist in spotipy_returned["items"]:
            playlist_tracks = sp.playlist_items(playlist["id"])
            for item in playlist_tracks["items"]:
                if "track" in item:
                    user_tracks.append(item["track"])
        return user_tracks

    def blend(self, user, friend_id):
        """
        Combines tracks from the user's and friend's playlists into a blended playlist.

        Args:
            user (dict): The authenticated user.
            friend_id (str): The friend's ID.

        Returns:
            Response: A JSON response with the blended playlist or an error message.
        """
        access_token = user["spotify_token"]
        print(access_token)
        if not access_token:
            print("im here")
            return {"msg": "Token not found"}, 401

        try:
            # Initialize Spotify client
            sp = spotipy.Spotify(auth=access_token)

            # Fetch the current user's playlists
            user_tracks = self.get_playlist_tracks(
                user, sp.current_user_playlists())

            # Fetch the friend's playlists
            friend = get_user_from_token(friend_id)
            if not friend or "spotify_id" not in friend:
                return {"error": "Friend's Spotify account not linked"}, 404

            friend_tracks = self.get_playlist_tracks(user, sp.user_playlists(
                friend["spotify_id"], limit=50))

            # Combine and shuffle tracks
            combined_tracks = []
            for track in user_tracks:
                if track in friend_tracks:
                    combined_tracks.append(track)

            # Return the blended playlist
            return {
                "playlist": [{
                    "id": track["id"],
                    "title": track["name"],
                    "artist": track["artists"][0]["name"],
                    "link": track["external_urls"]["spotify"],
                    "cover": track["album"]["images"][0]["url"]
                } for track in combined_tracks if track and isinstance(track, dict)]
            }
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {e}")
            return {"error": "Failed to blend playlists"}, 500
        except IndexError as e:
            print(f"List index out of range: {e}")
            return {"error": "An error occurred while blending playlists"}, 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "An unexpected error occurred"}, 500


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
        refresh_token = token_info["refresh_token"]

        # Fetch the user's Spotify account information
        sp = spotipy.Spotify(auth=access_token)
        user_info = sp.current_user()
        spotify_id = user_info.get("id")

        # Retrieve the user's token from the session
        token = session.get("token")

        # Link the Spotify account to the user's profile
        link_spotify(token, spotify_id, access_token, refresh_token)

        # Redirect the user to the recommendations page
        return redirect(f"http://localhost:8080/settings")


@spotify_ns.route("/link-spotify")
class LinkSpotifyRoute(Resource):
    @auth
    def get(user, self):
        # Redirect the user to the Spotify login page
        return redirect("/api/spotify/login")


@spotify_ns.route("/top-tracks")
class TopTracks(Resource):
    @auth
    def get(user, self):
        try:
            # Initialize Spotify client with the user's token
            sp = spotipy.Spotify(auth=user["spotify_token"])
            sp.me()  # Test the token validity
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:  # Token expired
                refreshed = refreshToken(user)
                user["spotify_token"] = refreshed["access_token"]
                sp = spotipy.Spotify(auth=refreshed["access_token"])

        try:
            # Fetch the user's top tracks from Spotify
            results = sp.current_user_top_tracks(limit=50)

            # Format the results to include only relevant details
            formatted_results = [
                {
                    "name": track["name"],
                    "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                    "album": track["album"]["name"],
                    "link": track["external_urls"]["spotify"]
                }
                for track in results["items"]
            ]

            return {"tracks": formatted_results}, 200
        except Exception as e:
            print(f"Error fetching top tracks: {e}")
            return {"error": "Failed to fetch top tracks"}, 500


@spotify_ns.route("/recently-played")
class RecentlyPlayed(Resource):
    @auth
    def get(user, self):
        try:
            # Initialize Spotify client with the user's token
            sp = spotipy.Spotify(auth=user["spotify_token"])
            sp.me()  # Test the token validity
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:  # Token expired
                refreshed = refreshToken(user)
                user["spotify_token"] = refreshed["access_token"]
                sp = spotipy.Spotify(auth=refreshed["access_token"])

        try:
            # Fetch the user's recently played tracks from Spotify
            results = sp.current_user_recently_played(limit=10)

            # Format the results to include only relevant details
            formatted_results = [
                {
                    "name": track["track"]["name"],
                    "artist": ", ".join([artist["name"] for artist in track["track"]["artists"]]),
                    "album": track["track"]["album"]["name"],
                    "link": track["track"]["external_urls"]["spotify"],
                    # Link to the cover art
                    "cover_art": track["track"]["album"]["images"][0]["url"]
                }
                for track in results["items"]
            ]
            return {"recently_played": formatted_results}, 200
        except Exception as e:
            print(f"Error fetching recently played tracks: {e}")
            return {"error": "Failed to fetch recently played tracks"}, 500
