class BaseError(Exception):
    """Base Error class"""

    def __init__(self, message=None, error=None, status=500):
        super().__init__(self)
        self.message = message
        self.error = error
        self.status = status

    def serialize(self):
        d = dict()
        d["message"] = self.message

        if self.error:
            d["error"] = self.error

        return d


class UserAlreadyExists(BaseError):
    def __init__(self):
        super().__init__()
        self.message = "A user with the given email already exists"
        self.status = 400


class NotFound(BaseError):
    def __init__(self, message="Not found"):
        super().__init__()
        self.message = message
        self.status = 404


class ServerError(BaseError):
    def __init__(self, message="Internal server error"):
        super().__init__()
        self.message = message
        self.status = 500


class BadRequest(BaseError):
    def __init__(self, message="Bad request"):
        super().__init__()
        self.message = message
        self.status = 400


class AuthorizationError(BaseError):
    INVALID_CRED = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED = "TOKEN_EXPIRED"

    def __init__(self, message="Unauthorized", error=None):
        super().__init__()
        self.message = message
        self.error = error
        self.status = 401
