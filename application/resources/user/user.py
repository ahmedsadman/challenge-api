from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import bp
from application.models import User, Challenge
from application.error_handlers import UserAlreadyExists, NotFound


@bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by id"""
    user = User.query.get(user_id)
    if user:
        return user.serialize()


@bp.route("/<user_id>/following", methods=["GET"])
@jwt_required
def get_following_list(user_id):
    """Get the list of people a user is following"""
    user = User.query.get(user_id)
    if user:
        return {"following": [u.serialize() for u in user.following.all()]}
    raise NotFound("User does not exist")


@bp.route("/<user_id>/followers", methods=["GET"])
@jwt_required
def get_follower_list(user_id):
    user = User.query.get(user_id)
    if user:
        return {"followers": [u.serialize() for u in user.followers.all()]}
    raise NotFound("User does not exist")


@bp.route("/feed", methods=["GET"])
@jwt_required
def get_user_feed():
    user = User.query.get(get_jwt_identity())
    page = request.args.get("page") or 1
    page = int(page)

    feed = user.get_feed()
    return Challenge.serialize_feed(user, feed)

    raise NotFound("User not found")
