from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username  # Adjust the import as needed

user_bp = Blueprint('user', __name__)

#DELETE	/api/admin/remove-user/:id	Admin removes a user	JWT (admin)
# This route will remove a user from the database
# The user must be logged in as an admin to access this route
@user_bp.route('/remove-user/<id>', methods=['DELETE'])
@jwt_required() 
def remove_user(id):
    current_user = get_jwt_identity()

    # Add the code to remove the user from the database here
    return jsonify({"message": "User removed successfully"})