# App/auth/routes/register.py
from flask import jsonify

from App.auth.auth import auth_bp
from App.auth.services.register import register_user
from App.auth.request.register import RegisterRequest
from App.auth.schemas.profile import ProfileSchema
from App.utils.helpers import validate_request
from App.extensions import limiter

profile_schema = ProfileSchema()


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("3 per minute")
@validate_request(RegisterRequest)
def register(payload: RegisterRequest):
    user, error = register_user(payload.username, payload.email, payload.password)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Registration successful",
        "user": profile_schema.dump(user),
    }), 201