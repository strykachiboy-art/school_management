from flask import jsonify
from App.decorators import role_required
from App.routes.admin.admin import admin_bp
from App.services.admin_report_services import get_admin_report
from App.enums.role import Role


@admin_bp.route("/report", methods=["GET"])
@role_required(Role.ADMIN)
def get_admin_report_route():
    report = get_admin_report()
    return jsonify(report), 200