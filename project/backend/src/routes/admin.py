from flask_restx import Namespace, Resource
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username, find_user, make_admin, remove_admin, get_users, delete_user
from ..middleware import admin_auth

admin_ns = Namespace('admin', description='Admin related operations')

@admin_ns.route('/user/<id>')
class RemoveUser(Resource):
    @admin_ns.doc(description="Removes a user account")
    @admin_auth
    def delete(self, user, id):
        # Add the code to remove the user from the database here
        return jsonify({"message": "User removed successfully"})

@admin_ns.route('/permissions/<id>')
class MakeAdminRoute(Resource):
    @admin_ns.doc(description="Grants admin permissions to a user")
    @admin_auth
    def post(user, self, id):
        foundUser = find_user(id)
        if not foundUser:
            return {"error": "User not found"}, 404

        if foundUser["admin"]:
            return { "error": "User is already an admin" }, 400

        make_admin(id)
        return {"message": "User is now an admin"}, 200

    @admin_ns.doc(description="Removes admin permissions from a user")
    @admin_auth
    def delete(user, self, id):
        user = find_user(id)
        if not user:
            return {"error": "User not found"}, 404
        
        if not user["admin"]:
            return { "error": "User is not an admin" }, 400

        remove_admin(id)
        return {"message": "User is no longer an admin"}, 200

@admin_ns.route('/users')
class UsersRoute(Resource):
    @admin_ns.doc(description="Gets all user accounts")
    @admin_auth
    def get(user, self):
        users = get_users()
        print(users)

        for user in users:
            user["_id"] = str(user["_id"])
        return users, 200
    
@admin_ns.route("/users/<username>")
class UserRoute(Resource):
    @admin_ns.doc(description="Gets a user account")
    @admin_auth
    def get(user, self, username):
        foundUser = find_user_by_username(username, True)
        if not foundUser:
            return {"error": "User not found"}, 404

        foundUser["_id"] = str(foundUser["_id"])
        return foundUser, 200
    
    @admin_ns.doc(description="Deletes a user account")
    @admin_auth
    def delete(user, self, username):
        foundUser = find_user_by_username(username, True)
        if not foundUser:
            return {"error": "User not found"}, 404
        
        delete_user(username)
        return {"message": "User removed successfully"}, 200 