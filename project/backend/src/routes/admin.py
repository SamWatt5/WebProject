from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username, find_user, make_admin, remove_admin  # Adjust the import as needed
from ..middleware import admin_auth

admin_bp = Blueprint('admin', __name__)

# DELETE	/api/admin/remove-user/:id	Admin removes a user	JWT (admin)
# This route will remove a user from the database
# The user must be logged in as an admin to access this route


@admin_bp.route('/remove-user/<id>', methods=['DELETE'])
@admin_auth
def remove_user(user, id):

    # Add the code to remove the user from the database here
    return jsonify({"message": "User removed successfully"})

@admin_bp.route('/make-admin/<id>', methods=['POST', 'GET'])
@admin_auth
def make_admin_route(user, id):
    foundUser = find_user(id)
    if not foundUser:
        return jsonify({"error": "User not found"}), 404

    make_admin(id)
    return jsonify({"message": "User is now an admin"}), 200

@admin_bp.route('/remove-admin/<id>', methods=['POST', 'GET'])
@admin_auth
def remove_admin_route(user, id):
    user = find_user(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    remove_admin(id)
    return jsonify({"message": "User is no longer an admin"}), 200