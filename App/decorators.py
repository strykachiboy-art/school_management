"""Reusable decorators for the application."""
from functools import wraps
from flask import abort, current_app, g, jsonify


# App/decorators.py
def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not g.user:
                abort(401, description="Authentication required")
            
            # Extract string value if role is an Enum
            user_role = g.user.role.value if hasattr(g.user.role, "value") else str(g.user.role)
            allowed = [r.value if hasattr(r, "value") else str(r) for r in allowed_roles]
            
            if user_role.lower() not in [a.lower() for a in allowed]:
                abort(403, description="Permission denied")
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator