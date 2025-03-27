from functools import wraps
from flask import request, session, jsonify
from .models import get_user_from_token, find_user
import inspect


def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # auth_header = request.headers.get("Authorization")
        # if not auth_header or not auth_header.startswith("Bearer "):
        #     return {"error": "Authorization header missing or invalid"}, 400

        token = session.get("token")
        if not token:
            print("invalid token")
            return {"error": "Invalid token"}, 400

        user = find_user(token, True)
        if not user:
            return {"error": "User not found"}, 404

        if not user["admin"]:
            return {"error": "Access denied"}, 403

        func_signature = inspect.signature(f)
        if "token" in func_signature.parameters:
            return f(user, token, *args, **kwargs)

        return f(user, *args, **kwargs)
    return decorated_function


def auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        # auth_header = request.headers.get("Authorization")
        # if not auth_header or not auth_header.startswith("Bearer "):
        #     return {"error": "Authorization header missing or invalid"}, 400

        # Extract the token from the header
        token = session.get("token")
        if not token:
            return {"error": "Invalid token"}, 400

        # Validate the token and get the user
        user = find_user(token, True)
        if not user:
            return {"error": "User not found"}, 404
        
        user["_id"] = str(user["_id"])  

        # Pass the user and token to the wrapped function
        func_signature = inspect.signature(f)
        if "token" in func_signature.parameters:
            return f(user, token, *args, **kwargs)

        return f(user, *args, **kwargs)

    return decorated_function
