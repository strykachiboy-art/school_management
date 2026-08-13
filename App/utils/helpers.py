from flask import request
from functools import wraps
from pydantic import ValidationError


def wants_json():
    return request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html


def validate_request(schema=None):
    """A decorator to validate incoming JSON request data against a Pydantic schema."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            raw_data = request.get_json(silent=True) or {}

            if schema:
                validated = schema.model_validate(raw_data)  # ValidationError now bubbles up
                return f(validated, *args, **kwargs)

            return f(*args, **kwargs)
        return decorated_function
    return decorator