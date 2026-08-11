"""Reusable decorators for the application."""
from functools import wraps
from flask import abort, current_app, g, jsonify


def role_required(*allowed_roles):
    """Allow access only to users with one of the allowed roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_app.config.get("ADMIN_ACCESS_ENABLED", False):
                abort(403)

            user = getattr(g, "user", None)
            if user is None:
                return jsonify({"message": "Login required"}), 401
            
            role = getattr(user, "role", None)
            
            if role not in allowed_roles:
                return jsonify({"message": "forbidden"}), 403

            return view_func(*args, **kwargs)

        return wrapper

    return decorator