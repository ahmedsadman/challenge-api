from flask import request
from datetime import datetime
from . import bp
from application.models import User, Challenge, Submission
from application.error_handlers import UserAlreadyExists, NotFound


@bp.route("", methods=["POST"])
def create_challenge():
    data = request.get_json()
    expires = datetime.strptime(data["expires_on"], "%Y-%m-%dT%H:%M:%S.%fz")

    author = User.query.filter_by(id=data["author_id"]).first()

    if author is None:
        raise NotFound("User not found")

    new_challenge = Challenge(
        author=author, question=data["question"], expires_on=expires
    )

    for tag_name in data["tags"]:
        u = User.query.filter_by(name=tag_name).first()
        if u is not None:
            new_challenge.add_tag(u)
    new_challenge.save()

    return new_challenge.serialize(), 201


@bp.route("/<challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)

    # if user id is given, serialize challenge in relation to that user
    user_id = request.args.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        if user is not None:
            return challenge.serialize_for_user(user)
        raise NotFound("User not found")
    return challenge.serialize()


@bp.route("/<challenge_id>/submissions", methods=["GET"])
def get_submissions(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    return {"submissions": [item.serialize() for item in challenge.submissions.all()]}


@bp.route("/<challenge_id>/submissions", methods=["POST"])
def add_submission(challenge_id):
    data = request.get_json()
    challenge = Challenge.query.get(challenge_id)

    if challenge is None:
        return NotFound("Challenge not found")

    current_time = datetime.utcnow()

    if current_time >= challenge.expires_on:
        return {"message": "Challenge expired. Cannot accept answers now"}

    user = User.query.get(data["user_id"])

    if user is None:
        raise NotFound("User not found")

    submission = Submission(challenge=challenge, user=user, answer=data["answer"])
    submission.save()

    return submission.serialize(), 201
