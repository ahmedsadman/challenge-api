from application import db

"""Association tables used for many-to-many relationships"""

follower_map = db.Table(
    "follower_map",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("follows_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)
