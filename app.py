from application import create_app
from config import Config
from application.models import User
from application import db

app = create_app(Config)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User}


@app.cli.command("seed-db")
def seed_db():
    # Not complete, just dummy
    with app.app_context():
        u1 = User(name="Jami", email="jami@gmail.com", password="test")
        u2 = User(name="Samyo", email="samyo@gmail.com", password="test")

        save_all([u1, u2])
        u1.follow(u2)
        save_all([u1, u2])

        db.session.commit()
        print("Done")


def save_all(items):
    # items -> array
    for item in items:
        item.save()


if __name__ == "__main__":
    app.run(debug=True, port=3001)
