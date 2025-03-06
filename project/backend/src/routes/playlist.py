from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username  # Adjust the import as needed

user_bp = Blueprint('user', __name__)

# GET	/api/playlist/generate	Generate a group playlist	JWT + OAuth
# This route will generate a group playlist based on the user's friends
# The user must be logged in to access this route
# The user can only access their own friend list
@user_bp.route('/generate', methods=['GET'])
@jwt_required()
def generate_playlist():
    current_user = get_jwt_identity()

    # Add the code to generate the group playlist here
    return jsonify({"message": "Playlist generated successfully"})

#POST	/api/playlist/save	Save playlist to Spotify	JWT + OAuth
# This route will save the generated playlist to the user's Spotify account
# The user must be logged in to access this route
# The user can only access their own friend list
@user_bp.route('/save', methods=['POST'])
@jwt_required()
def save_playlist():
    current_user = get_jwt_identity()

    # Add the code to save the playlist to Spotify here
    return jsonify({"message": "Playlist saved successfully"})

