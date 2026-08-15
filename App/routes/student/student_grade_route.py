from flask import jsonify, abort, g, Blueprint
from App.decorators import role_required
from App.services.student_grade_service import get_student_own_grade

student_grade_bp = Blueprint("student_grade", __name__, url_prefix="/student")


@student_grade_bp.route("/me/grade", methods=["GET"])
@role_required("student")
def get_my_grade_route():
    student = g.user.student_profile

    if student is None:
        abort(403, description="Student profile not found")

    try:
        grade = get_student_own_grade(student.id)
    except ValueError as e:
        abort(404, description=str(e))

    return jsonify({
        "average": grade["average"],
        "grade": grade["grade"],
        "remark": grade["remark"]
    }), 200