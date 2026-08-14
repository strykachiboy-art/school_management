from flask import g, jsonify
from App.auth.auth import auth_bp
from App.decorators import role_required
from App.utils.helpers import validate_request
from App.auth.request.change_password import ChangePasswordRequest
from App.auth.services.change_password import change_password
from App.extensions import limiter


@auth_bp.route("/change_password", methods=["PATCH"])
@limiter.limit("5 per minute")
@role_required("admin", "teacher", "student")
@validate_request(ChangePasswordRequest)
def change_password_route(validated):

    if g.user is None:
        return jsonify({"error": "Authentication required"}), 401

    try:
        change_password(
            g.user,
            validated.current_password,
            validated.new_password
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"success": "Password changed successfully"}), 200