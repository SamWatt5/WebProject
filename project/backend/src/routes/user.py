from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import find_user_by_username

user_bp = Blueprint('user', __name__)


@user_bp.route("/profile/<username>", methods=["GET"])
@jwt_required()
def profile(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify({"error": "Access forbidden"}), 403

    user = find_user_by_username(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user["_id"] = str(user["_id"])
    return jsonify(user), 200
