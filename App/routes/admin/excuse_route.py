from flask import Blueprint, jsonify, request, g, abort
from pydantic import ValidationError

from App.decorators import role_required
from App.requests.excuse_request import ExcuseCreateRequest, ExcuseUpdateRequest, ExcuseResponse
from App.services import excuse_service
from App.enums.excuse import ExcuseStatus

excuse_bp = Blueprint("excuse_bp", __name__, url_prefix="/excuses")


def _current_student_id() -> int:
    student = g.user.student_profile
    if student is None:
        abort(403, description="Student profile not found.")
    return student.id


@excuse_bp.route("", methods=["POST"])
@role_required("student")
def create_excuse():
    try:
        data = ExcuseCreateRequest.model_validate(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    excuse = excuse_service.create_excuse(
        attendance_id=data.attendance_id,
        reason=data.reason,
        student_id=_current_student_id(),
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 201


@excuse_bp.route("/<int:excuse_id>", methods=["GET"])
@role_required("admin", "teacher", "student")
def get_excuse(excuse_id: int):
    excuse = excuse_service.get_excuse(excuse_id)
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200


@excuse_bp.route("", methods=["GET"])
@role_required("admin", "teacher", "student")
def get_excuses():
    student_id = request.args.get("student_id", type=int)
    term_id = request.args.get("term_id", type=int)
    raw_status = request.args.get("status", type=str)

    status = None
    if raw_status:
        try:
            status = ExcuseStatus(raw_status.lower())
        except ValueError:
            return jsonify({"error": f"Invalid status parameter '{raw_status}'"}), 400

    excuses = excuse_service.get_excuses(
        student_id=student_id,
        term_id=term_id,
        status=status,
    )
    results = [ExcuseResponse.model_validate(e).model_dump() for e in excuses]
    return jsonify(results), 200


@excuse_bp.route("/<int:excuse_id>", methods=["PATCH"])
@role_required("student")
def update_excuse(excuse_id: int):
    try:
        data = ExcuseUpdateRequest.model_validate(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    excuse = excuse_service.update_excuse(
        excuse_id=excuse_id,
        reason=data.reason,
        student_id=_current_student_id(),
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200


@excuse_bp.route("/<int:excuse_id>", methods=["DELETE"])
@role_required("student")
def delete_excuse(excuse_id: int):
    excuse_service.delete_excuse(
        excuse_id=excuse_id,
        student_id=_current_student_id(),
    )
    return jsonify({"message": f"Excuse {excuse_id} deleted successfully."}), 200


@excuse_bp.route("/<int:excuse_id>/approve", methods=["POST"])
@role_required("admin", "teacher")
def approve_excuse(excuse_id: int):
    excuse = excuse_service.approve_excuse(
        excuse_id=excuse_id,
        reviewer_id=g.user.id,
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200


@excuse_bp.route("/<int:excuse_id>/reject", methods=["POST"])
@role_required("admin", "teacher")
def reject_excuse(excuse_id: int):
    excuse = excuse_service.reject_excuse(
        excuse_id=excuse_id,
        reviewer_id=g.user.id,
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200