from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .routes.auth import auth_bp
from .routes.user import user_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this!

    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    return app
