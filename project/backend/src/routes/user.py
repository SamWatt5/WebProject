from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username  # Adjust the import as needed

user_bp = Blueprint('user', __name__)


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
