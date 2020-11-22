from application import db
from datetime import datetime
from application.models import BaseModel


class Challenge(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    expires_on = db.Column(db.DateTime)

    tags = db.relationship(
        "User",
        secondary="challenge_tags",
        lazy="dynamic",
        backref=db.backref("tagged_in_challenges", lazy="dynamic"),
    )

    submissions = db.relationship("Submission", backref="challenge", lazy="dynamic")

    # author -> backref

    def serialize(self):
        return {
            "id": self.id,
            "author": {"id": self.author.id, "name": self.author.name},
            "question": self.question,
            "created_on": self.created_on,
            "expires_on": self.expires_on,
        }

    def add_tag(self, user):
        self.tags.append(user)

    def serialize_for_user(self, user):
        """Adds tag and submission information (if applicable) with the default serialization"""
        serialized = self.serialize()

        # check if the user was tagged in the challenge
        if self.tags.filter_by(id=user.id).first() is not None:
            serialized["tagged"] = True

            # also append submission information if applicable
            submission = self.submissions.filter_by(user_id=user.id).first()
            if submission is not None:
                serialized["submission"] = submission.serialize()
        else:
            serialized["tagged"] = False
            serialized["submission"] = None

        return serialized

    @classmethod
    def serialize_feed(cls, user_id, feed_queryobj, page=1, per_page=10):
        """Take the Tweet query object and serialize with pagination"""
        paginated_feed = feed_queryobj.paginate(
            page=page, per_page=per_page, error_out=True
        )
        return {
            "total": paginated_feed.total,
            "page": paginated_feed.page,
            "items": [
                item.serialize_for_user(user_id) for item in paginated_feed.items
            ],
            "has_prev": paginated_feed.has_prev,
            "has_next": paginated_feed.has_next,
            "per_page": per_page,
        }
