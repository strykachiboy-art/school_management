from flask import Blueprint, jsonify, request, abort, flash, redirect, url_for
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from App.schemas.result_schema import ResultSchema
from App.decorators import role_required

from App.services.result_services import (
    create_result,
    get_result as get_result_by_id,
    get_all_result as get_all_result_service,  
    delete_result,
    search_results,
    paginate_result
)

from App.utils.helpers import wants_json

result_bp = Blueprint("result", __name__, url_prefix="/results")


# ================================= Create Exam Route ==================================
@result_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_result_route():
    result_data = request.get_json(silent=True) or request.form.to_dict()

    try:
        result_instance = ResultSchema().load(result_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    created_result = create_result(
        student_id=result_instance.student_id, 
        exam_id=result_instance.exam_id,
        marks_obtained=result_instance.marks_obtained
    )

    serialized_result = ResultSchema().dump(created_result)

    if wants_json():
        return jsonify(serialized_result), 201
        
    flash("Result created successfully")
    
    return jsonify(serialized_result), 201


# ============================ Get All Results Route ============================
@result_bp.route("/", methods=["GET"])  
@role_required("admin")
def get_all_results_route(): 
    results = get_all_result_service()

    serialized_result = ResultSchema(many=True).dump(results)
    
    if wants_json():
        return jsonify(serialized_result), 200
   
    return jsonify(serialized_result), 200


# ============================ Get Result by ID Route ============================
@result_bp.route("/<int:result_id>", methods=["GET"])
@role_required("admin")
def get_result_route(result_id):
    result = get_result_by_id(result_id)
    
    if not result:
        abort(404, description="Result not found")
    
    serialized_result = ResultSchema().dump(result)
    
    if wants_json():
        return jsonify(serialized_result), 200
    
    return jsonify(serialized_result), 200


# ============================ Delete Result Route ============================
@result_bp.route("/<int:result_id>/delete", methods=["DELETE"])
@role_required("admin")
def delete_result_route(result_id):
    deleted = delete_result(result_id)
    
    if not deleted:
        abort(404, description="Result not found")
    
    if wants_json():
        return jsonify({"message": "Result deleted successfully"}), 200
    
    flash("Result deleted successfully")
    return redirect(url_for("result.get_all_results_route"))


# ============================ Search Result Route ============================
@result_bp.route("/search", methods=["GET"])
@role_required("admin")
def search_result_route():
    try:
        student_id = request.args.get("student_id", type=int)
        exam_id = request.args.get("exam_id", type=int)

        if request.args.get("paginate") == "true":
            page = paginate_result()
            return jsonify({
                "items": ResultSchema(many=True).dump(page.items),
                "page": page.page,
                "pages": page.pages,
                "total": page.total,
            })
        elif student_id or exam_id:
            results = search_results(student_id=student_id, exam_id=exam_id)
        else:
            results = get_all_result_service()

        return jsonify(ResultSchema(many=True).dump(results))

    except Exception as e:
        if wants_json():
            return jsonify({"error": "An unexpected error occurred."}), 500
        abort(500)