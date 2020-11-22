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
