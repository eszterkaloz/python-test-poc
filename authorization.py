from functools import wraps
from flask import request, Response


class ValidationError(Exception):
    pass


def authorize(validator):
    def decorator(action):
        @wraps(action)
        def wrapper(*args, **kwargs):
            try:
                validator(request)
                return action(*args, **kwargs)
            except ValidationError:
                return Response('Authorization required', 401)

        return wrapper
    return decorator
