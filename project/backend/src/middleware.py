from functools import wraps
from flask import request, session, jsonify
from .models import get_user_from_token, find_user
import inspect


def admin_auth(f):
    """
    Middleware to enforce admin authentication for a route.

    This decorator checks if the user is authenticated and has admin privileges.
    If the user is not authenticated or does not have admin privileges, it returns
    an appropriate error response.

    Args:
        f (function): The route function to wrap.

    Returns:
        function: The wrapped function with admin authentication applied.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Retrieve the token from the session
        token = session.get("token")
        if not token:
            print("invalid token")
            return {"error": "Invalid token"}, 400

        # Find the user associated with the token
        user = find_user(token, True)
        if not user:
            print("user not found?")
            return {"error": "User not found"}, 404

        # Check if the user has admin privileges
        if not user["admin"]:
            return {"error": "Access denied"}, 403

        # Check if the wrapped function accepts the token as a parameter
        func_signature = inspect.signature(f)
        if "token" in func_signature.parameters:
            return f(user, token, *args, **kwargs)

        return f(user, *args, **kwargs)
    return decorated_function


def auth(f):
    """
    Middleware to enforce user authentication for a route.

    This decorator checks if the user is authenticated by validating the token
    stored in the session. If the user is not authenticated, it returns an error
    response.

    Args:
        f (function): The route function to wrap.

    Returns:
        function: The wrapped function with user authentication applied.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Retrieve the token from the session
        token = session.get("token")
        if not token:
            return {"error": "Invalid token"}, 400

        # Validate the token and find the user
        user = find_user(token, True)
        if not user:
            print("its not working here")
            return {"error": "User not found"}, 404

        # Convert the user's ID to a string for compatibility
        user["_id"] = str(user["_id"])

        # Check if the wrapped function accepts the token as a parameter
        func_signature = inspect.signature(f)
        if "token" in func_signature.parameters:
            return f(user, token, *args, **kwargs)

        return f(user, *args, **kwargs)

    return decorated_function
