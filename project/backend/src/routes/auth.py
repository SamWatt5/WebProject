from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import create_user, find_user_by_username, verify_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return {"error": "No JSON data provided"}, 400

    fname = data.get("fname")
    lname = data.get("lname")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    profile_pic_url = data.get("profilePicUrl", "default_profile.png")

    if not fname or not lname or not email or not username or not password:
        return {"error": "Missing required fields"}, 400

    if find_user_by_username(username):
        return {"error": "User already exists"}, 400

    create_user(fname, lname, email, username, password, profile_pic_url)
    return {"message": "User created successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return {"error": "No JSON data provided"}, 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"error": "Missing username or password"}, 400

    user = find_user_by_username(username)
    if not user:
        return {"error": "User not found"}, 404

    if verify_password(user["password"], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return {"error": "Invalid credentials"}, 401
