from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from application import db
from werkzeug.security import check_password_hash, generate_password_hash
from application.models import BaseModel, Challenge
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
    created_challenges = db.relationship("Challenge", backref="author", lazy="dynamic")
    challenge_submissions = db.relationship(
        "Submission", backref="user", lazy="dynamic"
    )
    # followers -> backref
    # tagged_in_challenges -> backref

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

    def get_feed(self):
        # challenges that the user is tagged in
        tagged = self.tagged_in_challenges

        # not tagged, but following the author
        followed = Challenge.query.join(
            follower_map, (follower_map.c.follows_id == Challenge.author_id)
        ).filter(follower_map.c.user_id == self.id)

        # challenges created by the user himself
        own_challenges = self.created_challenges

        # combine both and return
        # TODO: Make the feed relevant to the user by sorting according to relevance
        return (
            tagged.union(followed)
            .union(own_challenges)
            .order_by(Challenge.created_on.desc())
        )

    @classmethod
    def find(cls, text):
        """Find users whose name matches with the given text"""
        return cls.query.filter(func.lower(cls.name).contains(text.lower()))

    def serialize(self):
        return {"id": self.id, "name": self.name}
