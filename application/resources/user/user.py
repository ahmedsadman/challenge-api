from flask import request
from . import bp
from application.models import User, Challenge
from application.error_handlers import UserAlreadyExists, NotFound


@bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by id"""
    user = User.query.get(user_id)
    if user:
        return user.serialize()
    raise NotFound("User does not exist")


@bp.route("/<user_id>/following", methods=["GET"])
def get_following_list(user_id):
    """Get the list of people a user is following"""
    user = User.query.get(user_id)
    if user:
        return {"following": [u.serialize() for u in user.following.all()]}
    raise NotFound("User does not exist")


@bp.route("/<user_id>/followers", methods=["GET"])
def get_follower_list(user_id):
    user = User.query.get(user_id)
    if user:
        return {"followers": [u.serialize() for u in user.followers.all()]}
    raise NotFound("User does not exist")


@bp.route("/<user_id>/feed", methods=["GET"])
def get_user_feed(user_id):
    user = User.query.get(user_id)
    page = request.args.get("page") or 1
    page = int(page)

    if user:
        feed = user.get_feed()
        return Challenge.serialize_feed(user, feed)

    raise NotFound("User not found")
