from flask import request, session, jsonify
from flask_restx import Namespace, Resource
from ..models import find_user, find_user_by_username, get_basic_user_info, get_user_friends, make_friends, remove_friends, get_user_from_token, update_user, remove_user
from ..middleware import auth

user_ns = Namespace('user', description='User related operations')


@user_ns.route("/me")
class MeRoute(Resource):
    """
    Endpoint to manage the authenticated user's account.

    Methods:
        get(user): Retrieves the authenticated user's information.
        patch(user): Updates the authenticated user's information.
        delete(user): Deletes the authenticated user's account.
    """
    @auth
    def get(user, self):
        """
        Retrieves the authenticated user's information.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: The user's information.
        """
        return user, 200

    @auth
    def patch(user, self):
        """
        Updates the authenticated user's information.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: A success message or an error response.
        """
        data = request.get_json()
        if not "username" in data:
            return {"error": "Username is required"}, 400
        if not "password" in data:
            return {"error": "Password is required"}, 400
        if not "fname" in data:
            return {"error": "First name is required"}, 400
        if not "lname" in data:
            return {"error": "Last name is required"}, 400
        if not "email" in data:
            return {"error": "Email is required"}, 400

        update_user(user["_id"], data["fname"], data["lname"],
                    data["email"], data["username"], data["password"])
        return {"message": "User updated successfully"}, 200

    @auth
    def delete(user, self):
        """
        Deletes the authenticated user's account.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: A success message.
        """
        remove_user(user["username"])
        return {"message": "User removed successfully"}, 200

# Not in use
@user_ns.route('/link-spotify/<username>')
class LinkSpotifyRoute(Resource):
    """
    Endpoint to link a user's Spotify account.

    Methods:
        post(username): Links the authenticated user's Spotify account.
    """

    def post(self, username):
        """
        Links the authenticated user's Spotify account.

        Args:
            username (str): The username of the user.

        Returns:
            Response: A success message or an error response.
        """
        current_user = session.get("username")

        if current_user != username:
            return jsonify({"error": "Access denied"}), 403

        # Add the code to link the user's Spotify account here
        return jsonify({"message": "Spotify account linked successfully"})


@user_ns.route("/find/<target>")
class FindRoute(Resource):
    """
    Endpoint to find a user by username or ID.

    Methods:
        get(user, target): Retrieves a user's information by username or ID.
    """
    @auth
    def get(user, self, target):
        """
        Retrieves a user's information by username or ID.

        Args:
            user (dict): The authenticated user.
            target (str): The username or ID of the target user.

        Returns:
            Response: The target user's information or an error response.
        """
        foundTarget = find_user_by_username(target, True)

        if not foundTarget:
            try:
                foundTarget = find_user(target, True)
            except:
                pass

        if not foundTarget:
            return {"error": "User not found"}, 404

        foundTarget = get_basic_user_info(foundTarget["_id"])
        foundTarget["_id"] = str(foundTarget["_id"])

        return foundTarget, 200


@user_ns.route('/friends')
class FriendsRoute(Resource):
    """
    Endpoint to manage the authenticated user's friends list.

    Methods:
        get(user): Retrieves the authenticated user's friends list.
    """
    @auth
    def get(user, self):
        """
        Retrieves the authenticated user's friends list.

        Args:
            user (dict): The authenticated user.

        Returns:
            Response: A list of the user's friends.
        """
        friendsList = get_user_friends(user["username"])
        list = []
        for friend in friendsList:
            list.append(find_user(str(friend), True))

        return list, 200


@user_ns.route('/friends/<username>')
class ManageFriendsRoute(Resource):
    """
    Endpoint to manage friendships.

    Methods:
        post(user, token, username): Adds a friend to the authenticated user's friends list.
        delete(user, token, username): Removes a friend from the authenticated user's friends list.
    """
    @auth
    def post(user, token, self, username):
        """
        Adds a friend to the authenticated user's friends list.

        Args:
            user (dict): The authenticated user.
            token (str): The user's token.
            username (str): The username of the friend to add.

        Returns:
            Response: A success message or an error response.
        """
        existing_friends = get_user_friends(user["username"])
        person = find_user_by_username(username, True)
        if not person:
            return {"error": "User not found"}, 404

        if person["_id"] in existing_friends:
            return {"error": "User is already a friend"}, 400

        make_friends(token, person["_id"])
        return {"message": "Friend added successfully"}, 200

    @auth
    def delete(user, token, self, username):
        """
        Removes a friend from the authenticated user's friends list.

        Args:
            user (dict): The authenticated user.
            token (str): The user's token.
            username (str): The username of the friend to remove.

        Returns:
            Response: A success message or an error response.
        """
        existing_friends = get_user_friends(user["username"])
        person = find_user_by_username(username, True)
        if not person:
            return jsonify({"error": "User not found"}), 404

        print(existing_friends)

        if not str(person["_id"]) in existing_friends:
            return jsonify({"error": "User is not a friend"}), 400

        remove_friends(token, person["_id"])
        return {"message": "Friend removed successfully"}, 200
