from flask import Blueprint, jsonify
from ..models import find_user_by_username

user_bp = Blueprint('user', __name__)


@user_bp.route("/profile/<username>", methods=["GET"])
def profile(username):
    user = find_user_by_username(username)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200
