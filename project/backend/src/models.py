from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

# Connect to MongoDB database
client = MongoClient(
    "mongodb+srv://2508240:2508240@webproject.u0mcu.mongodb.net/?retryWrites=true&w=majority&appName=WebProject")
db = client["Project"]
collection = db["Users"]


def create_user(fname, lname, email, username, password):
    """
    Create a new user in the database.

    Args:
        fname (str): First name of the user.
        lname (str): Last name of the user.
        email (str): Email address of the user.
        username (str): Username of the user.
        password (str): Plaintext password of the user.

    Returns:
        None
    """
    user_doc = {
        "first_name": fname,
        "last_name": lname,
        "email": email,
        "username": username,
        "profile_pic_url": "default_profile.png",
        "password": generate_password_hash(password),
        "spotify_id": None,
        "spotify_token": None,
        "spotify_refresh_token": None,
        "friends": [],
        "admin": False
    }
    collection.insert_one(user_doc)


def update_user(id, fname, lname, email, username, password):
    """
    Update an existing user's information.

    Args:
        id (str): User's ID.
        fname (str): Updated first name.
        lname (str): Updated last name.
        email (str): Updated email address.
        username (str): Updated username.
        password (str): Updated plaintext password.

    Returns:
        None
    """
    user_doc = {
        "first_name": fname,
        "last_name": lname,
        "email": email,
        "username": username,
        "password": generate_password_hash(password)
    }
    collection.update_one({"_id": ObjectId(id)}, {"$set": user_doc})


def link_spotify(token, spotify_id, access_token, refresh_token):
    """
    Link a Spotify account to a user.

    Args:
        token (str): User's ID.
        spotify_id (str): Spotify user ID.
        access_token (str): Spotify access token.
        refresh_token (str): Spotify refresh token.

    Returns:
        None
    """
    collection.update_one({"_id": ObjectId(token)}, {
        "$set": {"spotify_id": str(spotify_id), "spotify_token": str(access_token), "spotify_refresh_token": str(refresh_token)}})


def refresh_spotify(id, access_token, refresh_token):
    """
    Refresh a user's Spotify tokens.

    Args:
        id (str): User's ID.
        access_token (str): New Spotify access token.
        refresh_token (str): New Spotify refresh token.

    Returns:
        None
    """
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"spotify_token": str(
        access_token), "spotify_refresh_token": str(refresh_token)}})


def add_jwt(email, jwt):
    """
    Add a JWT token to a user.

    Args:
        email (str): User's email address.
        jwt (str): JWT token.

    Returns:
        None
    """
    collection.update_one({"email": email}, {
        "$set": {"jwt": jwt}})


def delete_user(username):
    """
    Delete a user by username.

    Args:
        username (str): Username of the user to delete.

    Returns:
        pymongo.results.DeleteResult: Result of the delete operation.
    """
    return collection.delete_one({"username": username})


def find_user(id, includeId=False):
    """
    Find a user by ID.

    Args:
        id (str): User's ID.
        includeId (bool): Whether to include the ID in the result.

    Returns:
        dict: User document.
    """
    if includeId == False:
        return collection.find_one({"_id": ObjectId(id)}, {"_id": includeId})
    return collection.find_one({"_id": ObjectId(id)})


def find_user_by_username(username, includeId=False):
    """
    Find a user by username.

    Args:
        username (str): Username of the user.
        includeId (bool): Whether to include the ID in the result.

    Returns:
        dict: User document.
    """
    if includeId == False:
        return collection.find_one({"username": username}, {"_id": includeId})
    return collection.find_one({"username": username})


def remove_user(username):
    """
    Remove a user by username.

    Args:
        username (str): Username of the user to remove.

    Returns:
        None
    """
    collection.delete_one({"username": username})


def verify_password(stored_password, provided_password):
    """
    Verify a user's password.

    Args:
        stored_password (str): Hashed password stored in the database.
        provided_password (str): Plaintext password provided by the user.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return check_password_hash(stored_password, provided_password)


def get_user_friends(username):
    """
    Get a user's friends list.

    Args:
        username (str): Username of the user.

    Returns:
        list: List of friends.
    """
    user = find_user_by_username(username)
    if user:
        return user.get("friends", [])
    return []


def make_friends(user1, user2):
    """
    Add two users as friends.

    Args:
        user1 (str): ID of the first user.
        user2 (str): ID of the second user.

    Returns:
        None
    """
    collection.update_one({"_id": ObjectId(user1)}, {
        "$addToSet": {"friends": str(user2)}})
    collection.update_one({"_id": ObjectId(user2)}, {
        "$addToSet": {"friends": str(user1)}})


def remove_friends(user1, user2):
    """
    Remove a friendship between two users.

    Args:
        user1 (str): ID of the first user.
        user2 (str): ID of the second user.

    Returns:
        None
    """
    collection.update_one({"_id": ObjectId(user1)}, {
        "$pull": {"friends": str(user2)}})
    collection.update_one({"_id": ObjectId(user2)}, {
        "$pull": {"friends": str(user1)}})


def get_basic_user_info(user):
    """
    Get basic information about a user.

    Args:
        user (str): User's ID.

    Returns:
        dict: Basic user information.
    """
    return collection.find_one({"_id": ObjectId(user)}, {"password": False, "spotify_token": False, "spotify_refresh_token": False})


def get_user_from_token(token):
    """
    Get a user document from a token.

    Args:
        token (str): User's token.

    Returns:
        dict: User document.
    """
    id = ObjectId(token)
    return collection.find_one({"_id": id}, {"_id": False})


def make_admin(user):
    """
    Grant admin privileges to a user.

    Args:
        user (str): User's ID.

    Returns:
        None
    """
    result = collection.update_one({"_id": ObjectId(user)}, {
        "$set": {"admin": True}})


def remove_admin(user):
    """
    Revoke admin privileges from a user.

    Args:
        user (str): User's ID.

    Returns:
        None
    """
    collection.update_one({"_id": ObjectId(user)}, {"$set": {"admin": False}})


def get_users():
    """
    Get all users in the database.

    Returns:
        list: List of user documents.
    """
    return list(collection.find({}))


def filter_popular(track):
    """
    Filter tracks based on popularity and availability.

    Args:
        track (dict): Track document.

    Returns:
        bool: True if the track is popular and available in GB, False otherwise.
    """
    return track["popularity"] > 0 and "GB" in track["availableCountries"]


def saved_liked_songs_to_user(user, liked_songs):
    """
    Save liked songs to a user's profile.

    Args:
        user (str): User's ID.
        liked_songs (list): List of liked songs.

    Returns:
        None
    """
    collection.update_one({"_id": ObjectId(user)}, {
        "$set": {"liked_songs": liked_songs}})
