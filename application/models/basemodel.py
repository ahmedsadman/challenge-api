from application import db
from application.error_handlers import ServerError


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        self._flush()
        return self

    def delete(self):
        db.session.delete(self)
        self._flush()

    def _flush(self):
        try:
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            raise ServerError("Error while saving to database")
