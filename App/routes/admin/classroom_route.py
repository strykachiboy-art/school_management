from flask import Blueprint, jsonify, request, abort
from App.decorators import role_required
from App.utils.helpers import validate_request
from App.requests.classroom_request import ClassroomCreateRequest, ClassroomResponse
from App.services.classroom_services import (
    create_classroom,
    get_all_classrooms,
    get_classroom,
    get_all_classroom_list,
    update_classroom as update_classroom_service,
    delete_classroom as delete_classroom_service,
)

classroom_bp = Blueprint("classroom", __name__, url_prefix="/classrooms")

# ====================================== Classroom assignment routes ===============================================

@classroom_bp.route("/create", methods=["POST"])
@role_required("admin")
@validate_request(ClassroomCreateRequest)
def create_classroom_route(data: ClassroomCreateRequest):
    classroom = create_classroom(data)

    if classroom is None:
        abort(400, description="Could not create classroom")

    serialized_classroom = ClassroomResponse.model_validate(classroom).model_dump()
    return jsonify(serialized_classroom), 201

# ====================================== get_all_classrooms_route ===============================================

@classroom_bp.route("", methods=["GET"])
@role_required("admin", "teacher")
def get_all_classrooms_route():
    if request.args.get("list") == "true":
        classrooms = get_all_classroom_list()
        serialized_list = [ClassroomResponse.model_validate(c).model_dump() for c in classrooms]
        return jsonify(serialized_list), 200

    page = get_all_classrooms(search=request.args.get("search", "", type=str))

    return jsonify({
        "items": [ClassroomResponse.model_validate(item).model_dump() for item in page.items],
        "page": page.page,
        "pages": page.pages,
        "total": page.total,
    }), 200


# ====================================== get_classroom_detail routes ===============================================

@classroom_bp.route("/<int:classroom_id>", methods=["GET"])
@role_required("admin", "teacher")
def get_classroom_detail(classroom_id):
    classroom = get_classroom(classroom_id)
    if classroom is None:
        abort(404, description="Classroom not found")

    serialized_classroom = ClassroomResponse.model_validate(classroom).model_dump()
    return jsonify(serialized_classroom), 200


# ====================================== update_classroom_route ===============================================

@classroom_bp.route("/<int:classroom_id>/edit", methods=["PUT", "PATCH"])
@role_required("admin")
@validate_request(ClassroomCreateRequest)
def update_classroom_route(data: ClassroomCreateRequest, classroom_id):
    classroom = get_classroom(classroom_id)
    if classroom is None:
        abort(404, description="Classroom not found")

    updated_classroom = update_classroom_service(classroom_id, data)

    serialized_classroom = ClassroomResponse.model_validate(updated_classroom).model_dump()
    return jsonify(serialized_classroom), 200


# ====================================== delete_classroom_route ===============================================

@classroom_bp.route("/<int:classroom_id>", methods=["DELETE"])
@role_required("admin")
def delete_classroom_route(classroom_id):
    deleted = delete_classroom_service(classroom_id)

    if not deleted:
        abort(404, description="Classroom not found")

    return jsonify({"message": "Classroom deleted successfully"}), 200