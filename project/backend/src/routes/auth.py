from flask import request, session, redirect
from ..models import add_jwt, create_user, find_user_by_username, verify_password
from flask_restx import Namespace, Resource, reqparse
from ..middleware import auth

auth_ns = Namespace("auth", description="Authentication operations")


@auth_ns.route("/signup")
class SignupRoute(Resource):
    """
    Endpoint for user signup.

    Methods:
        post(): Creates a new user account.
    """
    parser = reqparse.RequestParser()
    parser.add_argument("fname", type=str, required=True,
                        help="First name is required")
    parser.add_argument("lname", type=str, required=True,
                        help="Last name is required")
    parser.add_argument("email", type=str, required=True,
                        help="Email is required")
    parser.add_argument("username", type=str, required=True,
                        help="Username is required")
    parser.add_argument("password", type=str, required=True,
                        help="Password is required")
    parser.add_argument("profilePicUrl", type=str,
                        required=False, help="Profile picture URL is required")

    @auth_ns.doc(description="Creates a new user account")
    @auth_ns.expect(parser)
    def post(self):
        """
        Creates a new user account.

        Returns:
            Response: A success message or an error response.
        """
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
    """
    Endpoint for user login.

    Methods:
        post(): Logs the user into the application.
    """
    @auth_ns.doc(description="Logs the user into the application")
    def post(self):
        """
        Logs the user into the application.

        Returns:
            Response: A success message with user ID or an error response.
        """
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
            # Set the token in the session
            session["token"] = str(user["_id"])  # Use the user's ID as the token
            return {"message": "Login successful", "code": str(user["_id"])}, 200
        else:
            return {"error": "Invalid credentials"}, 401


@auth_ns.route("/callback")
class CallbackRoute(Resource):
    """
    Endpoint for Spotify authentication callback.

    Methods:
        get(): Handles the callback from Spotify authentication.
    """
    @auth_ns.doc(description="Callback route for Spotify authentication")
    @auth_ns.doc(params={"code": {
        "description": "The code provided by Spotify",
        "in": "query",
        "type": "string",
        "required": True
    }})
    def get(self):
        """
        Handles the callback from Spotify authentication.

        Returns:
            Response: Redirects the user to the frontend application.
        """
        session["token"] = request.args.get("code")
        return redirect("http://localhost:8080/")


@auth_ns.route("/logout", methods=["POST"])
class LogoutRoute(Resource):
    """
    Endpoint for user logout.

    Methods:
        post(): Logs the user out of the application.
    """
    @auth_ns.doc(description="Logs the user out of the application")
    def post(self):
        """
        Logs the user out of the application.

        Returns:
            Response: Redirects the user to the frontend application.
        """
        session.clear()
        return redirect("http://localhost:8080/")

@auth_ns.route("/test-user-id")
class TestUserIdRoute(Resource):
    """
    Endpoint to retrieve a user ID and user dictionary for testing purposes.

    Methods:
        post(): Retrieves the user ID and user dictionary for a given username.
    """
    def post(self):
        # Get the username from the request
        username = request.json.get("username")
        if not username:
            return {"error": "Username is required"}, 400

        # Find the user by username and include the _id field
        user = find_user_by_username(username, includeId=True)
        if not user:
            return {"error": "User not found"}, 404

        # Return the user ID and user dictionary
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return {"user_id": user["_id"], "user": user}, 200