from application import db
from datetime import datetime
from application.models import BaseModel


class Submission(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenge.id"))

    # user who the submission is realted to
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    answer = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    is_correct = db.Column(db.Boolean, nullable=True)
    submitted_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # user -> backref
    # challenge -> backref

    def serialize(self):
        return {
            "id": self.id,
            "challenge_id": self.challenge_id,
            "submitted_by": {"id": self.user.id, "name": self.user.name},
            "answer": self.answer,
            "completed": self.completed,
            "is_correct": self.is_correct,
            "created_on": self.submitted_on,
            "updated_on": self.updated_on,
        }
