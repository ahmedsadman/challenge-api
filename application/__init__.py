from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from application.error_handlers import BaseError

db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
jwt = JWTManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.errorhandler(BaseError)
    def handle_error(error):
        return error.serialize(), error.status

    @app.after_request
    def session_commit(response):
        """Commit the database session, only after the request has been successfully completed"""
        if response.status_code >= 400:
            return response
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            return response

    with app.app_context():
        from .resources import user_bp
        from .resources import auth_bp

        app.register_blueprint(user_bp, url_prefix="/user")
        app.register_blueprint(auth_bp, url_prefix="/auth")

        return app

