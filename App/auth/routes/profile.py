from flask import g, jsonify
from flask_jwt_extended import jwt_required

from App.auth.auth import auth_bp
from App.auth.schemas.profile import ProfileSchema
from App.auth.request.profile import ProfileUpdateRequest
from App.auth.services.profile import update_profile
from App.utils.helpers import validate_request


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    if not g.user:
        return jsonify({"error": "authentication required"}), 401

    return jsonify(ProfileSchema().dump(g.user)), 200


@auth_bp.route("/profile", methods=["PATCH"])
@jwt_required()
@validate_request(ProfileUpdateRequest)
def update_user_profile(validated):
    if not g.user:
        return jsonify({"error": "authentication required"}), 401

    user = update_profile(
        g.user, validated.model_dump(exclude_unset=True)
    )

    return jsonify(ProfileSchema().dump(user)), 200