from flask import request
from datetime import datetime
from . import bp
from application.models import User, Challenge
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
