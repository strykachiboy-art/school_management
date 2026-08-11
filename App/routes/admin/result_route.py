from flask import Blueprint, jsonify, render_template, request, abort, flash, redirect, url_for
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

    # Correct use of dot notation because load_instance = True
    created_result = create_result(
        student_id=result_instance.student_id, 
        exam_id=result_instance.exam_id,
        marks_obtained=result_instance.marks_obtained
    )

    serialized_result = ResultSchema().dump(created_result)

    if wants_json():
        return jsonify(serialized_result), 201
        
    flash("Result created successfully")
    
    return render_template("results/result_detail.html", result=created_result)


# ============================ Get All Results Route ============================
@result_bp.route("/", methods=["GET"])  
@role_required("admin")
def get_all_results_route(): 
    results = get_all_result_service()
    
    if not results:
        abort(404, description="Results not found")
    
    serialized_result = ResultSchema(many=True).dump(results)
    
    if wants_json():
        return jsonify(serialized_result), 200
   
    # FIXED: Changed from result_detail.html to get_results.html for lists
    return render_template("results/get_results.html", results=results)


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
    
    return render_template("results/result_detail.html", result=result)


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
        classroom_id = request.args.get("classroom_id", type = int)

        if student_id:
            results = search_results(student_id=student_id)
        elif exam_id:
            results = search_results(exam_id=exam_id)
        elif classroom_id:
            results = search_results(classroom_id=classroom_id)
        elif request.args.get("paginate") == "true":
            page = paginate_result()
            if wants_json():
                return jsonify({
                    "items": ResultSchema(many=True).dump(page.items),
                    "page": page.page,
                    "pages": page.pages,
                    "total": page.total,
                })
            return render_template("results/results.html", results=page.items, page=page)
        else:
            results = get_all_result_service()

        if wants_json():
            return jsonify(ResultSchema(many=True).dump(results))

        return render_template("results/results.html", results=results)
        
    except Exception as e:
        if wants_json():
            return jsonify({"error": "An unexpected error occurred."}), 500
        abort(500)