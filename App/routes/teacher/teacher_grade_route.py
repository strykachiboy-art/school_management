from flask import Blueprint, jsonify, abort, g
from App.decorators import role_required
from App.services.teacher_grade_service import get_student_grade_for_teachers

teacher_grade_bp = Blueprint("teacher_grade", __name__, url_prefix="/teacher")


@teacher_grade_bp.route("/students/<int:student_id>/grade", methods=["GET"])
@role_required("teacher")
def get_student_grade(student_id):
    teacher = g.user.teacher_profile

    if teacher is None:
        abort(403, description="Teacher profile not found")

    try:
        grade = get_student_grade_for_teachers(teacher.id, student_id)
    except ValueError as e:
        abort(404, description=str(e))

    return jsonify({
        "student_id": student_id,
        "grade": grade
    }), 200