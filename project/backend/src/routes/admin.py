from flask_restx import Namespace, Resource
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username, find_user, make_admin, remove_admin, get_users, delete_user
from ..middleware import admin_auth

admin_ns = Namespace('admin', description='Admin related operations')


#Not in use TO DELETE
@admin_ns.route('/user/<id>')
class RemoveUser(Resource):
    """
    Endpoint to remove a user account.

    Methods:
        delete(user, id): Deletes a user account by ID.
    """
    @admin_ns.doc(description="Removes a user account")
    @admin_auth
    def delete(self, user, id):
        """
        Deletes a user account from the database.

        Args:
            user (dict): The authenticated admin user.
            id (str): The ID of the user to be removed.

        Returns:
            Response: A success message or an error response.
        """
        # Add the code to remove the user from the database here
        return jsonify({"message": "User removed successfully"})


@admin_ns.route('/permissions/<id>')
class MakeAdminRoute(Resource):
    """
    Endpoint to manage admin permissions for a user.

    Methods:
        post(user, id): Grants admin permissions to a user.
        delete(user, id): Removes admin permissions from a user.
    """
    @admin_ns.doc(description="Grants admin permissions to a user")
    @admin_auth
    def post(self, user, id):
        """
        Grants admin permissions to a user.

        Args:
            user (dict): The authenticated admin user.
            id (str): The ID of the user to be granted admin permissions.

        Returns:
            Response: A success message or an error response.
        """
        print(f"[DEBUG] POST /permissions/{id} called")
        print(f"[DEBUG] Authenticated admin user: {user}")
        print(f"[DEBUG] Target user ID: {id}")

        foundUser = find_user(id)
        print(f"[DEBUG] Found user: {foundUser}")

        if not foundUser:
            print(f"[DEBUG] User with ID {id} not found")
            return {"error": "User not found"}, 404

        if foundUser["admin"]:
            print(f"[DEBUG] User with ID {id} is already an admin")
            return {"error": "User is already an admin"}, 400

        make_admin(id)
        print(f"[DEBUG] User with ID {id} has been granted admin privileges")
        return {"message": "User is now an admin"}, 200

    @admin_ns.doc(description="Removes admin permissions from a user")
    @admin_auth
    def delete(self, user, id):
        """
        Removes admin permissions from a user.

        Args:
            user (dict): The authenticated admin user.
            id (str): The ID of the user to have admin permissions removed.

        Returns:
            Response: A success message or an error response.
        """
        print(f"[DEBUG] DELETE /permissions/{id} called")
        print(f"[DEBUG] Authenticated admin user: {user}")
        print(f"[DEBUG] Target user ID: {id}")

        foundUser = find_user(id)
        print(f"[DEBUG] Found user: {foundUser}")

        if not foundUser:
            print(f"[DEBUG] User with ID {id} not found")
            return {"error": "User not found"}, 404

        if not foundUser["admin"]:
            print(f"[DEBUG] User with ID {id} is not an admin")
            return {"error": "User is not an admin"}, 400

        remove_admin(id)
        print(f"[DEBUG] Admin privileges removed for user with ID {id}")
        return {"message": "User is no longer an admin"}, 200


@admin_ns.route('/users')
class UsersRoute(Resource):
    """
    Endpoint to retrieve all user accounts.

    Methods:
        get(user): Retrieves all user accounts.
    """
    @admin_ns.doc(description="Gets all user accounts")
    @admin_auth
    def get(self, user):
        """
        Retrieves all user accounts from the database.

        Args:
            user (dict): The authenticated admin user.

        Returns:
            Response: A list of user accounts.
        """
        users = get_users()
        print(users)

        for user in users:
            user["_id"] = str(user["_id"])
        return users, 200


@admin_ns.route("/users/<username>")
class UserRoute(Resource):
    """
    Endpoint to manage a specific user account.

    Methods:
        get(user, username): Retrieves a user account by username.
        delete(user, username): Deletes a user account by username.
    """
    @admin_ns.doc(description="Gets a user account")
    @admin_auth
    def get(self, user, username):
        """
        Retrieves a user account by username.

        Args:
            user (dict): The authenticated admin user.
            username (str): The username of the user to retrieve.

        Returns:
            Response: The user account details or an error response.
        """
        foundUser = find_user_by_username(username, True)
        if not foundUser:
            return {"error": "User not found"}, 404

        foundUser["_id"] = str(foundUser["_id"])
        return foundUser, 200

    @admin_ns.doc(description="Deletes a user account")
    @admin_auth
    def delete(self, user, username):
        """
        Deletes a user account by username.

        Args:
            user (dict): The authenticated admin user.
            username (str): The username of the user to delete.

        Returns:
            Response: A success message or an error response.
        """
        foundUser = find_user_by_username(username, True)
        if not foundUser:
            return {"error": "User not found"}, 404

        delete_user(username)
        return {"message": "User removed successfully"}, 200

@admin_ns.route('/test/grant-admin/<id>')
class TestGrantAdminRoute(Resource):
    """
    Test-only endpoint to grant admin privileges to a user without authentication.

    Methods:
        post(id): Grants admin privileges to a user by ID.
    """
    @admin_ns.doc(description="Grants admin privileges to a user without authentication (TEST ONLY)")
    def post(self, id):
        """
        Grants admin privileges to a user without requiring authentication.

        Args:
            id (str): The ID of the user to be granted admin privileges.

        Returns:
            Response: A success message or an error response.
        """
        print(f"[DEBUG] TEST POST /test/grant-admin/{id} called")
        print(f"[DEBUG] Target user ID: {id}")

        foundUser = find_user(id)
        print(foundUser)
        print(f"[DEBUG] Found user: {foundUser}")

        if not foundUser:
            print(f"[DEBUG] User with ID {id} not found")
            return {f"error": "User not found"}, 404 

        if foundUser["admin"]:
            print(f"[DEBUG] User with ID {id} is already an admin")
            return {"error": "User is already an admin"}, 400

        make_admin(id)
        print(f"[DEBUG] User with ID {id} has been granted admin privileges")
        return {"message": "User is now an admin (TEST ONLY)"}, 200
