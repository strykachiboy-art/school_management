from flask import Blueprint, jsonify, g, abort

from App.decorators import role_required
from App.utils.helpers import validate_request
from App.requests.promotion_request import (
    PromotionEvaluationResponse,
    PromoteStudentRequest,
    RepeatStudentRequest,
    GraduateStudentRequest,
    PromotionHistoryResponse,
)
from App.services.promotion_service import (
    evaluate_student_promotion,
    promote_student as promote_student_service,
    repeat_student as repeat_student_service,
    graduate_student as graduate_student_service,
    get_student_promotion_history,
    get_session_promotions,
)

promotion_bp = Blueprint("promotion", __name__, url_prefix="/promotions")

# ====================================== evaluate_promotion_route ===============================================

@promotion_bp.route("/students/<int:student_id>/sessions/<int:academic_session_id>/evaluate", methods=["GET"])
@role_required("admin", "teacher")
def evaluate_promotion_route(student_id, academic_session_id):
    evaluation = evaluate_student_promotion(student_id, academic_session_id)

    if evaluation is None:
        abort(404, description="Student or academic session not found")

    serialized = PromotionEvaluationResponse.model_validate(evaluation).model_dump()
    return jsonify(serialized), 200


# ====================================== promote_student_route ===============================================

@promotion_bp.route("/students/<int:student_id>/sessions/<int:academic_session_id>/promote", methods=["POST"])
@role_required("admin", "teacher")
@validate_request(PromoteStudentRequest)
def promote_student_route(data: PromoteStudentRequest, student_id, academic_session_id):
    history = promote_student_service(
        student_id,
        academic_session_id,
        data.to_classroom_id,
        remarks=data.remarks,
        decided_by=g.user.id if g.user else None,
        decided_by_role=g.user.role if g.user else None,
        allow_level_skip=data.allow_level_skip,
    )

    if history is None:
        abort(404, description="Student not found")

    serialized = PromotionHistoryResponse.model_validate(history).model_dump()
    return jsonify(serialized), 201


# ====================================== repeat_student_route ===============================================

@promotion_bp.route("/students/<int:student_id>/sessions/<int:academic_session_id>/repeat", methods=["POST"])
@role_required("admin")
@validate_request(RepeatStudentRequest)
def repeat_student_route(data: RepeatStudentRequest, student_id, academic_session_id):
    history = repeat_student_service(
        student_id,
        academic_session_id,
        remarks=data.remarks,
        decided_by=g.user.id if g.user else None,
    )

    if history is None:
        abort(404, description="Student not found")

    serialized = PromotionHistoryResponse.model_validate(history).model_dump()
    return jsonify(serialized), 201


# ====================================== graduate_student_route ===============================================

@promotion_bp.route("/students/<int:student_id>/sessions/<int:academic_session_id>/graduate", methods=["POST"])
@role_required("admin")
@validate_request(GraduateStudentRequest)
def graduate_student_route(data: GraduateStudentRequest, student_id, academic_session_id):
    history = graduate_student_service(
        student_id,
        academic_session_id,
        remarks=data.remarks,
        decided_by=g.user.id if g.user else None,
    )

    if history is None:
        abort(404, description="Student not found")

    serialized = PromotionHistoryResponse.model_validate(history).model_dump()
    return jsonify(serialized), 201


# ====================================== student_promotion_history_route ===============================================

@promotion_bp.route("/students/<int:student_id>/history", methods=["GET"])
@role_required("admin", "teacher", "student")
def student_promotion_history_route(student_id):
    if g.user and g.user.role == "student" and getattr(g.user.student_profile, "id", None) != student_id:
        abort(403, description="Students may only view their own promotion history")

    history = get_student_promotion_history(student_id)

    if history is None:
        abort(404, description="Student not found")

    serialized = [PromotionHistoryResponse.model_validate(h).model_dump() for h in history]
    return jsonify(serialized), 200


# ====================================== session_promotions_route ===============================================

@promotion_bp.route("/sessions/<int:academic_session_id>", methods=["GET"])
@role_required("admin")
def session_promotions_route(academic_session_id):
    promotions = get_session_promotions(academic_session_id)

    if promotions is None:
        abort(404, description="Academic session not found")

    serialized = [PromotionHistoryResponse.model_validate(p).model_dump() for p in promotions]
    return jsonify(serialized), 200