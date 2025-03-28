import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class Config:
    """
    Configuration class for the application.

    This class loads configuration values from environment variables
    and provides default values where applicable.

    Attributes:
        SECRET_KEY (str): Secret key for securing sessions and cookies.
        MONGO_URI (str): URI for connecting to the MongoDB database.
        SPOTIPY_CLIENT_ID (str): Spotify API client ID.
        SPOTIPY_CLIENT_SECRET (str): Spotify API client secret.
        SPOTIPY_REDIRECT_URI (str): Redirect URI for Spotify API authentication.
        SPOTIPY_SCOPE (str): Scope of permissions requested from Spotify API.
    """

    # Not sure if this file is actually being used anymore, but it was once upon a time
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/user_test')
    SPOTIPY_CLIENT_ID = os.getenv('CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv(
        'REDIRECT_URI', 'http://localhost:8000/api/spotify/callback')
    SPOTIPY_SCOPE = "playlist-read-private playlist-read-collaborative"
