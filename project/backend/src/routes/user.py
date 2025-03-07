from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username, get_user_friends, make_friends, remove_friends

user_bp = Blueprint('user', __name__)

# This route will return the user's profile information
# based on the username provided in the URL
# The user must be logged in to access this route
# The user can only access their own profile


@user_bp.route('/profile/<username>', methods=['GET'])
@jwt_required()
def profile(username):
    current_user = get_jwt_identity()
    print(current_user)

    if current_user != username:
        return jsonify({"error": "Access denied"}), 403
    user = find_user_by_username(username)
    print(user)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Ensure the '_id' key exists in the user dictionary
    # if '_id' in user:
    #     user["_id"] = str(user["_id"])
    #     print("here1")
    # else:
    #     print("didnt work!")
    #     return jsonify({"error": "User ID not found"}), 500

    return jsonify(user)

# This route will link the user's Spotify account
# to the application
# The user must be logged in to access this route
# The user can only link their own Spotify account
# The user must provide a valid Spotify access token


@user_bp.route('/link-spotify/<username>', methods=['POST'])
@jwt_required()
def link_spotify(username):
    current_user = get_jwt_identity()

    if current_user != username:
        return jsonify({"error": "Access denied"}), 403

    # Add the code to link the user's Spotify account here
    return jsonify({"message": "Spotify account linked successfully"})

# This route will Fetch friend list
# The user must be logged in to access this route
# The user can only access their own friend list


@user_bp.route('/friends/<username>', methods=['GET'])
# @jwt_required()
def friends(username):
    # current_user = get_jwt_identity()

    # if current_user != username:
    #     return jsonify({"error": "Access denied"}), 403

    # Add the code to fetch the user's friend list here
    print(get_user_friends(username))
    return jsonify(get_user_friends(username))

# This route will add a new freind  to the user's friend list
# The user must be logged in to access this route
# The user can only add friends to their own friend list


@user_bp.route('/add-friend/<username>', methods=['POST'])
@jwt_required()
def add_friend(username):
    current_user = get_jwt_identity()

    if current_user != username:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    friend = data.get("friend")
    if not friend:
        return jsonify({"error": "Missing friend field"}), 400

    isPerson = True if find_user_by_username(friend) else False
    if not isPerson:
        return jsonify({"error": "User not found"})

    make_friends(username, friend)
    return jsonify({"message": f"{friend} added to friend list"})


@user_bp.route('/remove-friend/<username>', methods=['POST'])
@jwt_required()
def remove_friend(username):
    current_user = get_jwt_identity()

    if current_user != username:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    friend = data.get("friend")
    if not friend:
        return jsonify({"error": "Missing friend field"}), 400

    isPerson = True if find_user_by_username(friend) else False
    if not isPerson:
        return jsonify({"error": "User not found"})

    remove_friends(username, friend)
    return jsonify({"message": f"{friend} removed from friend list"})
