from flask import jsonify, abort
from App.routes.admin.admin import admin_bp
from App.models.result import Result
from App.services.grade_service import calculate_student_grade
from App.decorators import role_required

@admin_bp.route("/students/<int:student_id>/grade", methods=["GET"])
@role_required("admin")
def get_student_grade(student_id):
    results = Result.query.filter_by(student_id=student_id).all()
    
    if not results:
        abort(404, description="No results found for this student")
        
    grade = calculate_student_grade(results)
    
    return jsonify({
        "student_id": student_id,
        "grade": grade
    }), 200