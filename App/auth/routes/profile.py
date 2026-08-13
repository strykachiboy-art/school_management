from flask import g, jsonify, request
from App.auth.auth import auth_bp
from App.auth.schemas.profile import ProfileSchema
from App.auth.request.profile import ProfileUpdateRequest
from App.auth.services.profile import update_profile
from App.decorators import role_required


@auth_bp.route("/profile", methods = ["GET"])
@role_required("admin")
def get_profile():
    if not g.user:
        return jsonify({"error": "authentication required"})
    
    return jsonify(ProfileSchema().dump(g.user))


@auth_bp.route("/profile", methods = ["PATCH"])
@role_required("admin")
def update_user_profile():
    if not g.user:
        return jsonify({"error": "authentication required"})
    
    data = request.get_json()
    
    validated = ProfileUpdateRequest(**data)
    
    user = update_profile(
        g.user, validated.model_dump(exclude_unset=True)
    )
    
    return jsonify(ProfileSchema().dump(user)), 200