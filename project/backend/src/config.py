import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/user_test')
    SPOTIPY_CLIENT_ID = os.getenv('CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv(
        'REDIRECT_URI', 'http://localhost:8000/api/spotify/callback')
    SPOTIPY_SCOPE = "playlist-read-private playlist-read-collaborative"
