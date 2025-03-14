from dotenv import load_dotenv
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, session, request, jsonify, Blueprint
from flask_cors import CORS

from ..models import link_spotify

load_dotenv()

spotify_bp = Blueprint('spotify', __name__)

CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
redirect_uri = "http://localhost:8000/api/spotify/callback"

scopes = "user-read-email playlist-read-private playlist-read-collaborative"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=redirect_uri, scope=scopes)


@spotify_bp.route("/")
def hello_world():
    return "hello world! :)"


@spotify_bp.route("/me_playlists")
@jwt_required()
def me_playlists():
    claims = get_jwt()
    access_token = claims.get("spotify_access_token")
    if not access_token:
        return jsonify({"msg": "Token not found"}), 401

    sp = spotipy.Spotify(auth=access_token)
    results = sp.current_user_playlists()
    return jsonify(results)


@spotify_bp.route("/playlist/<playlist_id>/tracks")
@jwt_required()
def playlist(playlist_id):
    claims = get_jwt()
    access_token = claims.get("spotify_access_token")
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
    if not code:
        return jsonify({"msg": "Authorization failed"}), 400

    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]

    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.current_user()
    spotify_id = user_info.get("id")
    # Assuming email is passed as a query parameter
    email = user_info.get("email")

    print(email, spotify_id, access_token)
    link_spotify(email, spotify_id, access_token)

    # Create a new JWT token with the access token
    additional_claims = {"spotify_access_token": access_token}
    jwt_token = create_access_token(
        identity=email, additional_claims=additional_claims)

    # Return the new JWT token in the response body
    return jsonify(token=jwt_token), 200


@spotify_bp.route("/link-spotify")
@jwt_required()
def link_spotify_route():
    user = get_jwt_identity()
    session["email"] = user
    return redirect("/api/spotify/login")
