from flask import Blueprint, request, jsonify, session
from ..models import add_jwt, create_user, find_user_by_username, verify_password

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

    create_user(fname, lname, email, username, password)
    return {"message": "User created successfully"}, 201


@auth_bp.route("/login", methods=["GET"])
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
        session["username"] = username
        session["email"] = user["email"]
        print("WORKING!", username, password)
        return {"message": "Login successful"}, 200
    else:
        return {"error": "Invalid credentials"}, 401


@auth_bp.route("/logout")
def logout():
    session.clear()
    return {"message": "Logged out successfully"}, 200
