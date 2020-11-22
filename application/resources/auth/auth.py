from flask import request
from datetime import timedelta
from flask_jwt_extended import create_access_token
from application.models import User
from application.error_handlers import AuthorizationError, NotFound, BadRequest
from . import bp


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user:
        raise BadRequest("User with the given email already exists")

    user = User(name=data["name"], email=data["email"], password=data["password"])
    user.save()
    return user.serialize(), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        expires = timedelta(minutes=30)  # token will expire after 15 min
        access_token = create_access_token(
            identity=user.id, fresh=True, expires_delta=expires
        )
        return {"access_token": access_token}

    raise AuthorizationError(error=AuthorizationError.INVALID_CRED)
