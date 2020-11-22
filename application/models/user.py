from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from application import db
from werkzeug.security import check_password_hash, generate_password_hash
from application.models import BaseModel
from application.tables import follower_map


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    _password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    following = db.relationship(
        "User",
        secondary=follower_map,
        primaryjoin=(follower_map.c.user_id == id),
        secondaryjoin=(follower_map.c.follows_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    # followers -> backref

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_following(self, user):
        return self.following.filter_by(id=user.id).first() is not None

    def follow(self, user):
        """Follow a new user"""
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        """Unfollow an user"""
        if self.is_following(user):
            self.following.remove(user)

    def serialize(self):
        return {"id": self.id, "name": self.name}
