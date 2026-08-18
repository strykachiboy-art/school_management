from flask import Blueprint, jsonify, request, g
from pydantic import ValidationError

from App.requests.excuse_request import ExcuseCreateRequest, ExcuseUpdateRequest, ExcuseResponse
from App.services import excuse_service
from App.enums.excuse import ExcuseStatus

excuse_bp = Blueprint("excuse_bp", __name__, url_prefix="/excuses")


# ============================ 1. Create Excuse ============================

@excuse_bp.route("", methods=["POST"])
def create_excuse():
    try:
        data = ExcuseCreateRequest.model_validate(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    excuse = excuse_service.create_excuse(
        attendance_id=data.attendance_id,
        reason=data.reason,
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 201


# ============================ 2. Get Single Excuse ============================

@excuse_bp.route("/<int:excuse_id>", methods=["GET"])
def get_excuse(excuse_id: int):
    excuse = excuse_service.get_excuse(excuse_id)
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200


# ============================ 3. Get Excuses (List/Filter) ============================

@excuse_bp.route("", methods=["GET"])
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


# ============================ 4. Update Excuse ============================

@excuse_bp.route("/<int:excuse_id>", methods=["PATCH"])
def update_excuse(excuse_id: int):
    try:
        data = ExcuseUpdateRequest.model_validate(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    excuse = excuse_service.update_excuse(
        excuse_id=excuse_id,
        reason=data.reason,
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200


# ============================ 5. Delete Excuse ============================

@excuse_bp.route("/<int:excuse_id>", methods=["DELETE"])
def delete_excuse(excuse_id: int):
    excuse_service.delete_excuse(excuse_id)
    return jsonify({"message": f"Excuse {excuse_id} deleted successfully."}), 200


# ============================ 6. Approve Excuse ============================

@excuse_bp.route("/<int:excuse_id>/approve", methods=["POST"])
def approve_excuse(excuse_id: int):
    reviewer_id = getattr(g, "user_id", None) or request.json.get("reviewer_id") if request.is_json else None
    if not reviewer_id:
        return jsonify({"error": "Reviewer ID is required."}), 400

    excuse = excuse_service.approve_excuse(
        excuse_id=excuse_id,
        reviewer_id=reviewer_id,
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200


# ============================ 7. Reject Excuse ============================

@excuse_bp.route("/<int:excuse_id>/reject", methods=["POST"])
def reject_excuse(excuse_id: int):
    reviewer_id = getattr(g, "user_id", None) or request.json.get("reviewer_id") if request.is_json else None
    if not reviewer_id:
        return jsonify({"error": "Reviewer ID is required."}), 400

    excuse = excuse_service.reject_excuse(
        excuse_id=excuse_id,
        reviewer_id=reviewer_id,
    )
    return jsonify(ExcuseResponse.model_validate(excuse).model_dump()), 200