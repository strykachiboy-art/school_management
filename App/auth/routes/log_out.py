# App/auth/routes/logout.py
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

from App.auth.auth import auth_bp
from App.auth.services.log_out import revoke_token


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    token = get_jwt()
    revoke_token(token["jti"], token["exp"])
    return jsonify({"message": "Successfully logged out"}), 200