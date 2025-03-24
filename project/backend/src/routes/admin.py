from flask_restx import Namespace, Resource
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username, find_user, make_admin, remove_admin, get_users
from ..middleware import admin_auth

admin_ns = Namespace('admin', description='Admin related operations')

@admin_ns.route('/remove-user/<id>')
class RemoveUser(Resource):
    @admin_auth
    def delete(self, user, id):
        # Add the code to remove the user from the database here
        return jsonify({"message": "User removed successfully"})

@admin_ns.route('/make-admin/<id>')
class MakeAdminRoute(Resource):
    @admin_auth
    def post(user, self, id):
        foundUser = find_user(id)
        if not foundUser:
            return jsonify({"error": "User not found"}), 404

        make_admin(id)
        return jsonify({"message": "User is now an admin"}), 200

    @admin_auth
    def get(user, self, id):
        foundUser = find_user(id)
        if not foundUser:
            return jsonify({"error": "User not found"}), 404

        make_admin(id)
        return jsonify({"message": "User is now an admin"}), 200

@admin_ns.route('/remove-admin/<id>')
class RemoveAdminRoute(Resource):
    @admin_auth
    def post(user, self, id):
        user = find_user(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        remove_admin(id)
        return jsonify({"message": "User is no longer an admin"}), 200

    @admin_auth
    def get(user, self, id):
        user = find_user(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        remove_admin(id)
        return jsonify({"message": "User is no longer an admin"}), 200

@admin_ns.route('/users')
class UsersRoute(Resource):
    @admin_auth
    def get(user, self):
        users = get_users()
        print(users)

        return users, 200