from flask import Blueprint, jsonify, request, session
from ..models import find_user_by_username, get_user_friends, make_friends, remove_friends, get_user_from_token, find_user
from ..middleware import auth

user_bp = Blueprint('user', __name__)

# This route will return the user's profile information
# The user must be logged in to access this route
# The user can only access their own profile information
@user_bp.route("/me", methods=["GET"])
@auth
def me(user):
    return jsonify(user), 200


# This route will link the user's Spotify account
# to the application
# The user must be logged in to access this route
# The user can only link their own Spotify account
# The user must provide a valid Spotify access token
@user_bp.route('/link-spotify/<username>', methods=['POST'])
def link_spotify(username):
    current_user = session.get("username")

    if current_user != username:
        return jsonify({"error": "Access denied"}), 403

    # Add the code to link the user's Spotify account here
    return jsonify({"message": "Spotify account linked successfully"})


@user_bp.route("/find/<target>", methods=["GET"])
@auth
def find(user, target):
    foundTarget = find_user_by_username(target)

    if not foundTarget:
        try:
            foundTarget = find_user(target)
        except:
            pass

    if not foundTarget:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(foundTarget)

# This route will Fetch friend list
# The user must be logged in to access this route
# The user can only access their own friend list
@user_bp.route('/friends', methods=['GET'])
@auth
def friends(user):
    friendsList = get_user_friends(user["username"])
    list = []
    for friend in friendsList:
        list.append(find_user(str(friend), False))

    print(list)
    return jsonify(list)



# This route will add a new freind  to the user's friend list
# The user must be logged in to access this route
# The user can only add friends to their own friend list
@user_bp.route('/add-friend/<username>', methods=['GET', 'POST'])
@auth
def add_friend(user, token, username):
    existing_friends = get_user_friends(user["username"])
    person = find_user_by_username(username, True)
    if not person:
        return jsonify({"error": "User not found"}), 404 
    
    if person["_id"] in existing_friends:
        return jsonify({"error": "User is already a friend"}), 400
    
    
    make_friends(token, person["_id"])
    return { "message": "Friend added successfully" }


@user_bp.route('/remove-friend/<username>', methods=['POST'])
@auth
def remove_friend(user, token, username):
    existing_friends = get_user_friends(user["username"])
    person = find_user_by_username(username, True)
    if not person:
        return jsonify({"error": "User not found"}), 404 

    print(existing_friends)

    if not str(person["_id"]) in existing_friends:
        return jsonify({"error": "User is not a friend"}), 400
    
    
    remove_friends(token, person["_id"])
    return { "message": "Friend added removed" }
