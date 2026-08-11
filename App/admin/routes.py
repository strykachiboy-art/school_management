from flask import Blueprint, jsonify
from App.decorators import role_required
from App.admin.services import get_admin_dashboard_stats as fetch_dashboard_stats

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin_bp")

@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def get_admin_dashboard():
    stats = fetch_dashboard_stats()
    return jsonify(stats), 200