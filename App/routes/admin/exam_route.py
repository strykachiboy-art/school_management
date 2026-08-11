from flask import Blueprint, jsonify, render_template, request, abort, flash, redirect, url_for
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from App.schemas.exam_schema import ExamSchema
from App.decorators import role_required

from App.services.exam_services import (
    create_exam,
    get_exam as get_exam_by_id,
    get_all_exam,
    delete_exam,
    search_exams,
    paginate_exams
)

from App.utils.helpers import wants_json


exam_bp = Blueprint('exam', __name__, url_prefix="/exams")


# ================================= Create Exam Route ==================================
@exam_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_exam_route():
    if request.method == "POST":
        try:
            # Load and validate request data into an Exam model instance using load_instance = True
            exam_data = request.get_json(silent=True) or request.form.to_dict()
            exam_instance = ExamSchema().load(exam_data)
            
            # Pass the loaded instance or data to your service layer
            created_exam = create_exam(exam_instance)

            if wants_json():
                return jsonify(ExamSchema().dump(created_exam)), 201

            flash("Exam created successfully", "success")
            return redirect(url_for("exam.get_exams"))

        except ValidationError as e:
            if wants_json():
                return jsonify({"error": "Validation failed", "messages": e.messages}), 400
            flash("Validation failed — check your inputs.", "danger")
            
        except IntegrityError:
            if wants_json():
                return jsonify({"error": "Database error — duplicate or invalid constraint."}), 400
            flash("Could not create exam — check for duplicate entries.", "danger")

    return render_template("exams/create_exam.html")


# ================================== Get All Exams Route ==================================
@exam_bp.route("/", methods=["GET"])
@role_required("admin")
def get_exams():
    try:
        search = request.args.get("search", "", type=str)
        subject_id = request.args.get("subject_id", None, type=int)
        classroom_id = request.args.get("classroom_id", None, type=int)
        
        if search:
            exams = search_exams(search)
        elif subject_id:
             exams = search_exams(subject_id)
        elif classroom_id:
             exams = search_exams(classroom_id)
        elif request.args.get("paginate") == "true":
            page = paginate_exams()
            if wants_json():
                return jsonify({
                    "items": ExamSchema(many=True).dump(page.items),
                    "page": page.page,
                    "pages": page.pages,
                    "total": page.total,
                })
            return render_template("exams/exams.html", exams=page.items, page=page)
        else:
            exams = get_all_exam()

        if wants_json():
            return jsonify(ExamSchema(many=True).dump(exams))

        return render_template("exams/exams.html", exams=exams)
        
    except Exception as e:
        if wants_json():
            return jsonify({"error": "An unexpected error occurred."}), 500
        abort(500)



#============================== get exam id ===============================
@exam_bp.route("/<int:exam_id>", methods=["GET"])
@role_required("admin")
def get_exam(exam_id):
    exam = get_exam_by_id(exam_id)
    if exam is None:
        if wants_json():
            return jsonify({"error": "Exam not found"}), 404
        abort(404)

    if wants_json():
        return jsonify(ExamSchema().dump(exam))

    return render_template("exams/exam.html", exam=exam)



#============================== remove exam =====================================
@exam_bp.route("/<int:exam_id>", methods=["DELETE"])
@role_required("admin")
def remove_exam(exam_id):
    deleted = delete_exam(exam_id)
    if not deleted:
        if wants_json():
            return jsonify({"error": "Exam not found"}), 404
        abort(404)

    if wants_json():
        return jsonify({"message": "Exam deleted successfully"}), 200

    flash("Exam deleted successfully", "success")
    return redirect(url_for("exam.get_exams"))