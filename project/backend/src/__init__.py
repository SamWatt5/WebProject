from flask import Flask
from flask_cors import CORS
from flask_session import Session
from .config import Config
from .routes.auth import auth_ns
from .routes.user import user_ns
from .routes.admin import admin_ns
from .routes.spotify import spotify_ns
from flask_restx import Api


def create_app():
    """
    Factory function to create and configure the Flask application.

    This function initializes the Flask app with:
    - CORS support for cross-origin requests.
    - Session management using Flask-Session.
    - Configuration settings from the Config class.
    - Flask-RESTx API setup with namespaces for different routes.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
         r"/api/*": {"origins": "http://localhost:8080"}})
    app.config.from_object(Config)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'your_secret_key'
    Session(app)

    api = Api(
        title="TrackMates API",
        version="1.0",
        description="An API for the TrackMates application",
        doc="/docs"
    )

    app.config["RESTX_MASK_SWAGGER"] = False
    api.init_app(app)

    # Register namespaces for different routes
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(user_ns, path="/api/user")
    api.add_namespace(spotify_ns, path="/api/spotify")
    api.add_namespace(admin_ns, path="/api/admin")

    return app
