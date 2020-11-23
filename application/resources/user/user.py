from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import bp
from application.models import User, Challenge
from application.error_handlers import UserAlreadyExists, NotFound, BadRequest


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


@bp.route("/follow/<follow_id>", methods=["POST"])
@jwt_required
def follow(follow_id):
    me = User.query.get(get_jwt_identity())
    user = User.query.get(follow_id)

    if user is None:
        raise NotFound("User not found")

    if not me.is_following(user):
        me.follow(user)

    me.save()
    return {"message": "DONE!"}


@bp.route("/unfollow/<follow_id>", methods=["POST"])
@jwt_required
def unfollow(follow_id):
    me = User.query.get(get_jwt_identity())
    user = User.query.get(follow_id)

    if user is None:
        raise NotFound("User not found")

    if me.is_following(user):
        me.unfollow(user)
    else:
        raise BadRequest("The user is not being followed by you")

    me.save()
    return {"message": "DONE!"}


@bp.route("/feed", methods=["GET"])
@jwt_required
def get_user_feed():
    user = User.query.get(get_jwt_identity())
    page = request.args.get("page") or 1
    page = int(page)

    feed = user.get_feed()
    return Challenge.serialize_feed(user, feed)

    raise NotFound("User not found")


@bp.route("/my-challenges", methods=["GET"])
@jwt_required
def get_my_challenges():
    user = User.query.get(get_jwt_identity())
    return {"challenges": [item.serialize() for item in user.created_challenges.all()]}


@bp.route("/find", methods=["GET"])
def find_user():
    string = request.args.get("text")
    match = User.find(string)
    result = [item.serialize() for item in match.all()]
    return {"result": result}
