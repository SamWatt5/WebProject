from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient("mongodb://localhost:27017/")
db = client["user_test"]
collection = db["users"]


def create_user(fname, lname, email, username, password):
    user_doc = {
        "first_name": fname,
        "last_name": lname,
        "email": email,
        "username": username,
        "profile_pic_url": "default_profile.png",
        "password": generate_password_hash(password),
        "spotify_connected": False,
        "friends": []
    }
    collection.insert_one(user_doc)


def find_user_by_username(username):
    return collection.find_one({"username": username}, {"_id": False})


def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)
