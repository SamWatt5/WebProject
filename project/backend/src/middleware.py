from functools import wraps
from flask import request, session, jsonify
from .models import get_user_from_token
import inspect

def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return {"error": "Token not set"}, 400
        
        token = session.get("token")
        if not token:
            return {"error": "Invalid token"}, 400
        
        user = get_user_from_token(token)
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
        if 'token' not in session:
            return {"error": "Token not set"}, 400

        token = session.get("token")
        if not token:
            return {"error": "Invalid token"}, 400

        user = get_user_from_token(token)
        if not user:
            return {"error": "User not found"}, 404

        func_signature = inspect.signature(f)
        if "token" in func_signature.parameters:
            return f(user, token, *args, **kwargs)

        return f(user, *args, **kwargs)
    
    return decorated_function
