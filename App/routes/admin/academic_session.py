from flask import Blueprint, jsonify, request, abort
from App.decorators import role_required
from App.utils.helpers import validate_request
from App.requests.academic_session import (
    AcademicSessionCreateRequest,
    AcademicSessionUpdateRequest,
    AcademicSessionResponse,
)

from App.services.academic_session import (
    create_academic_session,
    get_all_academic_session,
    get_academic_session,
    update_academic_session,
    delete_session,
    activate_academic_session,
)

academic_session_bp = Blueprint("academic_session", __name__, url_prefix="/academic-sessions")


# ====================================== create_academic_session ===============================================

@academic_session_bp.route("/create", methods=["POST"])
@role_required("admin")
@validate_request(AcademicSessionCreateRequest)
def create_session(data: AcademicSessionCreateRequest):
    session = create_academic_session(data)
    serialized = AcademicSessionResponse.model_validate(session).model_dump()
    return jsonify(serialized), 201


# ====================================== get_all_academic_sessions ===============================================

@academic_session_bp.route("", methods=["GET"])
@role_required("admin", "teacher")
def get_all_sessions():
    search = request.args.get("search", "", type=str)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    result = get_all_academic_session(search=search, page=page, per_page=per_page)

    return jsonify({
        "items": [AcademicSessionResponse.model_validate(item).model_dump() for item in result.items],
        "page": result.page,
        "pages": result.pages,
        "total": result.total,
    }), 200


# ====================================== get_academic_session ===============================================

@academic_session_bp.route("/<int:session_id>", methods=["GET"])
@role_required("admin", "teacher")
def get_session(session_id):
    session = get_academic_session(session_id)
    if session is None:
        abort(404, description="Academic session not found")

    serialized = AcademicSessionResponse.model_validate(session).model_dump()
    return jsonify(serialized), 200


# ====================================== update_academic_session ===============================================

@academic_session_bp.route("/<int:session_id>/edit", methods=["PUT", "PATCH"])
@role_required("admin")
@validate_request(AcademicSessionUpdateRequest)
def update_session(data: AcademicSessionUpdateRequest, session_id):
    session = update_academic_session(data, session_id)
    if session is None:
        abort(404, description="Academic session not found")

    serialized = AcademicSessionResponse.model_validate(session).model_dump()
    return jsonify(serialized), 200


# ====================================== delete_academic_session ===============================================

@academic_session_bp.route("/<int:session_id>", methods=["DELETE"])
@role_required("admin")
def delete_academic_session_route(session_id):
    deleted = delete_session(session_id)
    if not deleted:
        abort(404, description="Academic session not found")

    return jsonify({"message": "Academic session deleted successfully"}), 200


# ====================================== activate_academic_session ===============================================

@academic_session_bp.route("/<int:session_id>/activate", methods=["PATCH"])
@role_required("admin")
def activate_session(session_id):
    session = activate_academic_session(session_id)
    if session is None:
        abort(404, description="Academic session not found")

    serialized = AcademicSessionResponse.model_validate(session).model_dump()
    return jsonify(serialized), 200