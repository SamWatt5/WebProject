from flask import request, jsonify, session, redirect
from ..models import add_jwt, create_user, find_user_by_username, verify_password
from flask_restx import Namespace, Resource
from ..middleware import auth

auth_ns = Namespace("auth", description="Authentication operations")

@auth_ns.route("/signup")
class SignupRoute(Resource):
    def post(self):
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

@auth_ns.route("/login")
class LoginRoute(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "No JSON data provided"}, 400

        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"error": "Missing username or password"}, 400

        user = find_user_by_username(username, True)
        if not user:
            return {"error": "User not found"}, 404

        if verify_password(user["password"], password):
            print(user)
            return {"message": "Login successful", "code": str(user["_id"])}, 200
        else:
            return {"error": "Invalid credentials"}, 401

@auth_ns.route("/callback")
class CallbackRoute(Resource):
    def get(self):
        session["token"] = request.args.get("code")
        return redirect("http://localhost:8080/")

@auth_ns.route("/logout")
class LogoutRoute(Resource):
    def get(self):
        session.clear()
        return redirect("https://localhost:8080")
