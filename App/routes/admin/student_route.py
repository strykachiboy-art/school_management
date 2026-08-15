from flask import Blueprint, jsonify, request, abort
from App.decorators import role_required
from App.utils.helpers import validate_request
from App.requests.student_request import StudentCreateRequest, StudentResponse

from App.services.student_services import (
    create_students,
    get_all_students,
    get_student_by_id,
    update_student as update_student_service,
    delete_student as delete_student_service,
    search_student_info,
    filter_classroom_id,
    filter_admission_number,
    paginate_students,
)

student_bp = Blueprint("student", __name__, url_prefix="/students")


# ====================================== create_student ===============================================

@student_bp.route("/create", methods=["POST"])
@role_required("admin")
@validate_request(StudentCreateRequest)
def create_student(data: StudentCreateRequest):
    student = create_students(data)
    
    serialized_student = StudentResponse.model_validate(student).model_dump()
    return jsonify(serialized_student), 201


# ====================================== get_all_student ===============================================

@student_bp.route("", methods=["GET"])
@role_required("admin", "teacher")
def get_all_student():
    search = request.args.get("search", "", type=str)
    classroom_id = request.args.get("classroom_id", None, type=int)
    admission_number = request.args.get("admission_number", None, type=str)

    if request.args.get("paginate") == "true":
        page = paginate_students()
        return jsonify({
            "items": [StudentResponse.model_validate(item).model_dump() for item in page.items],
            "page": page.page,
            "pages": page.pages,
            "total": page.total,
        }), 200
    elif search:
        students = search_student_info(search)
    elif classroom_id:
        students = filter_classroom_id(classroom_id)
    elif admission_number:
        students = filter_admission_number(admission_number)
    else:
        students = get_all_students()

    serialized_students = [StudentResponse.model_validate(s).model_dump() for s in students]
    return jsonify(serialized_students), 200


# ====================================== get_student ===============================================

@student_bp.route("/<int:student_id>", methods=["GET"])
@role_required("admin", "teacher", "student")
def get_student(student_id):
    student = get_student_by_id(student_id)
    if student is None:
        abort(404, description="Student not found")

    serialized_student = StudentResponse.model_validate(student).model_dump()
    return jsonify(serialized_student), 200


# ====================================== update_student ===============================================

@student_bp.route("/<int:student_id>/edit", methods=["PUT", "PATCH"])
@role_required("admin")
@validate_request(StudentCreateRequest)
def update_student(data: StudentCreateRequest, student_id):
    student = get_student_by_id(student_id)
    if student is None:
        abort(404, description="Student not found")

    updated_student = update_student_service(student_id, data)
    
    serialized_student = StudentResponse.model_validate(updated_student).model_dump()
    return jsonify(serialized_student), 200


# ====================================== delete_student ===============================================

@student_bp.route("/<int:student_id>", methods=["DELETE"])
@role_required("admin")
def delete_student(student_id):
    deleted = delete_student_service(student_id)

    if not deleted:
        abort(404, description="Student not found")

    return jsonify({"message": "Student deleted successfully"}), 200