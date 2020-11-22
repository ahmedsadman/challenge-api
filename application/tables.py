from application import db

"""Association tables used for many-to-many relationships"""

# following-follower mapping
follower_map = db.Table(
    "follower_map",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("follows_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

# challenge-user tags mapping
challenge_tags = db.Table(
    "challenge_tags",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "challenge_id", db.Integer, db.ForeignKey("challenge.id"), primary_key=True
    ),
)

