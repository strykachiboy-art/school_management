from App.routes.admin.admin import admin_bp
from flask import Blueprint, jsonify, abort, request, render_template
from App.models.result import Result

from App.services.grade_service import calculate_student_grade
from App.decorators import role_required
from App.utils.helpers import wants_json

@admin_bp.route("/students/<int:student_id>/grade", methods=["GET"])
@role_required("admin")
def get_student_grade(student_id):
    # FIXED: Added field name and .all() to convert query to a list
    results = Result.query.filter_by(student_id=student_id).all()
    
    grade = calculate_student_grade(results)
    
    # FIXED: Added parentheses to function call
    if wants_json():
        return jsonify(grade), 200
    
    return render_template("admin/grades.html", grade=grade, student_id=student_id)