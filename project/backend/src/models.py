from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

client = MongoClient(
    "mongodb+srv://2508240:2508240@webproject.u0mcu.mongodb.net/?retryWrites=true&w=majority&appName=WebProject")
db = client["Project"]
collection = db["Users"]


def create_user(fname, lname, email, username, password):
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


def link_spotify(token, spotify_id, access_token, refresh_token):
    collection.update_one({"_id": ObjectId(token)}, {
                          "$set": {"spotify_id": str(spotify_id), "spotify_token": str(access_token), "spotify_refresh_token": str(refresh_token)}})

def refresh_spotify(id, access_token, refresh_token):
    collection.update_one({"_id": ObjectId(id)}, { "spotify_token": str(access_token), "spotify_refresh_token": str(refresh_token)})

def add_jwt(email, jwt):
    collection.update_one({"email": email}, {
                          "$set": {"jwt": jwt}})

def delete_user(username):
    return collection.delete_one({"username": username})

def find_user(id, includeId=False):
    if includeId == False:
        return collection.find_one({"_id": ObjectId(id)}, {"_id": includeId})
    return collection.find_one({"_id": ObjectId(id)})


def find_user_by_username(username, includeId=False):
    if includeId == False:
        return collection.find_one({"username": username}, {"_id": includeId})
    return collection.find_one({"username": username})


def remove_user(username):
    collection.delete_one({"username": username})


def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)


def get_user_friends(username):
    user = find_user_by_username(username)
    if user:
        return user.get("friends", [])
    return []


def make_friends(user1, user2):
    collection.update_one({"_id": ObjectId(user1)}, {
                          "$addToSet": {"friends": str(user2)}})
    collection.update_one({"_id": ObjectId(user2)}, {
                          "$addToSet": {"friends": str(user1)}})


def remove_friends(user1, user2):
    collection.update_one({"_id": ObjectId(user1)}, {
                          "$pull": {"friends": str(user2)}})
    collection.update_one({"_id": ObjectId(user2)}, {
                          "$pull": {"friends": str(user1)}})


def get_basic_user_info(user):
    return collection.find_one({"_id": ObjectId(user)}, {"password": False, "spotify_token": False, "spotify_refresh_token": False})

def get_user_from_token(token):
    id = ObjectId(token)
    return collection.find_one({"_id": id}, {"_id": False})


def make_admin(user):
    result = collection.update_one({"_id": ObjectId(user)}, {
                                   "$set": {"admin": True}})


def remove_admin(user):
    collection.update_one({"_id": ObjectId(user)}, {"$set": {"admin": False}})


def get_users():
    return list(collection.find({}))


def filter_popular(track):
    return track["popularity"] > 0 and "GB" in track["availableCountries"]


def saved_liked_songs_to_user(user, liked_songs):
    collection.update_one({"_id": ObjectId(user)}, {
                          "$set": {"liked_songs": liked_songs}})
