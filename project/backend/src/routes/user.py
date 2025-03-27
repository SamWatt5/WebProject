from flask import request, session, jsonify
from flask_restx import Namespace, Resource
from ..models import find_user_by_username, get_basic_user_info, get_user_friends, make_friends, remove_friends, get_user_from_token, find_user
from ..middleware import auth

user_ns = Namespace('user', description='User related operations')


@user_ns.route("/me")
class MeRoute(Resource):
    @auth
    def get(user, self):
        print(user)
        return user, 200

    def patch(user, self):
        data = request.get_json()
        print(data)


@user_ns.route('/link-spotify/<username>')
class LinkSpotifyRoute(Resource):
    def post(self, username):
        current_user = session.get("username")

        if current_user != username:
            return jsonify({"error": "Access denied"}), 403

        # Add the code to link the user's Spotify account here
        return jsonify({"message": "Spotify account linked successfully"})


@user_ns.route("/find/<target>")
class FindRoute(Resource):
    @auth
    def get(user, self, target):

        foundTarget = find_user_by_username(target, True)

        if not foundTarget:
            try:
                foundTarget = find_user(target, True)
            except:
                pass

        if not foundTarget:
            return {"error": "User not found"}, 404

        foundTarget = get_basic_user_info(foundTarget["_id"])
        foundTarget["_id"] = str(foundTarget["_id"])

        return foundTarget, 200


@user_ns.route('/friends')
class FriendsRoute(Resource):
    @auth
    def get(user, self):
        friendsList = get_user_friends(user["username"])
        list = []
        for friend in friendsList:
            list.append(find_user(str(friend), True))

        return list, 200


@user_ns.route('/friends/<username>')
class ManageFriendsRoute(Resource):
    @auth
    def post(user, token, self, username):
        existing_friends = get_user_friends(user["username"])
        person = find_user_by_username(username, True)
        if not person:
            return {"error": "User not found"}, 404

        if person["_id"] in existing_friends:
            return {"error": "User is already a friend"}, 400

        make_friends(token, person["_id"])
        return {"message": "Friend added successfully"}

    @auth
    def delete(user, token, self, username):
        existing_friends = get_user_friends(user["username"])
        person = find_user_by_username(username, True)
        if not person:
            return jsonify({"error": "User not found"}), 404

        print(existing_friends)

        if not str(person["_id"]) in existing_friends:
            return jsonify({"error": "User is not a friend"}), 400

        remove_friends(token, person["_id"])
        return {"message": "Friend removed successfully"}
