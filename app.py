from application import create_app
from config import Config
from application.models import User, Challenge, Submission
from application import db

app = create_app(Config)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Challenge": Challenge, "Submission": Submission}


@app.cli.command("seed-db")
def seed_db():
    # seed the database with fake data
    with app.app_context():
        # create users
        u1 = User(name="Jami", email="jami@gmail.com", password="test")
        u2 = User(name="Samyo", email="samyo@gmail.com", password="test")

        save_all([u1, u2])

        # follow
        u1.follow(u2)
        u2.follow(u1)

        # create and tag challenges
        c1 = Challenge(question="Who invented Python?", author=u1)
        c1.tags.append(u2)
        c1.save()

        # challenge submissions
        s = Submission(user=u2, challenge=c1, answer="Guido Van Rossum")

        save_all([u1, u2, c1, s])

        db.session.commit()
        print("Done")


def save_all(items):
    # items -> array
    for item in items:
        item.save()


if __name__ == "__main__":
    app.run(debug=True, port=3001)
