# Add New Routes: Create new route files in the routes directory and register them in __init__.py.

from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from .routes.new_route import new_route_bp
from .routes.auth import auth_bp
from .config import Config
from flask_cors import CORS
from flask import Flask
from flask import Blueprint, request

new_route_bp = Blueprint('new_route', __name__)


@new_route_bp.route("/new", methods=["GET"])
def new_route():
    return {"message": "This is a new route"}, 200


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(new_route_bp, url_prefix='/api/new')

    return app

# Add New Models: Define new models in models.py or create separate model files if needed.


client = MongoClient("mongodb://localhost:27017/")
db = client["user_test"]
collection = db["users"]


def create_user(email, username, password):
    user_doc = {
        "email": email,
        "username": username,
        "password": generate_password_hash(password)
    }
    collection.insert_one(user_doc)


def find_user_by_username(username):
    return collection.find_one({"username": username})


def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

# New model function


def update_user(username, new_data):
    collection.update_one({"username": username}, {"$set": new_data})

# Add New Utilities: Add utility functions in utils.py or create separate utility files if needed.


def format_response(data):
    return {"status": "success", "data": data}
