from flask import Blueprint, flash, jsonify, redirect, request, url_for, abort
from App.decorators import role_required
from App.forms.student_form import StudentForm
from App.forms.subject_form import SubjectForm
from App.schemas.subject_schema import SubjectSchema
from App.services.subject_services import (
    create_subject,
    get_subject,
    get_all_subjects,
    update_subject,
    delete_subject,
    search_subject_info,
    serialize_subject,
    paginate_subject,
)
from App.utils.helpers import wants_json

subject_bp = Blueprint("subject", __name__, url_prefix="/subjects")


@subject_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_subject_route():
    form = SubjectForm()

    if form.validate_on_submit():
        subject = create_subject(form)

        if subject is None:
            if wants_json():
                return jsonify(error="Could not create subject"), 400
            flash("Could not create subject", "danger")
            return jsonify(error="Could not create subject"), 400

        if wants_json():
            return jsonify(SubjectSchema().dump(subject)), 201

        flash("Subject created successfully", "success")
        return redirect(url_for("subject.get_subjects"))

    if wants_json():
        return jsonify(errors=form.errors), 400

    return jsonify({"message": "Submit subject fields via POST"}), 200


@subject_bp.route("", methods=["GET"])
@role_required("admin")
def get_subjects():
    search = request.args.get("search", "", type=str)

    if request.args.get("paginate") == "true":
        page = paginate_subject()
        return jsonify({
            "items": [SubjectSchema().dump(item) for item in page.items],
            "page": page.page,
            "pages": page.pages,
            "total": page.total,
        })
    elif search:
        subjects = search_subject_info(search)
    else:
        subjects = get_all_subjects()

    serialized_subjects = SubjectSchema(many=True).dump(subjects)
    return jsonify(serialized_subjects)


@subject_bp.route("/<int:subject_id>", methods=["GET"])
@role_required("admin")
def get_subject_detail(subject_id):
    subject = get_subject(subject_id)
    if subject is None:
        abort(404)

    return jsonify(SubjectSchema().dump(subject))


@subject_bp.route("/<int:subject_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def update_subject_route(subject_id):
    subject = get_subject(subject_id)
    if subject is None:
        abort(404)

    form = SubjectForm(obj=subject)

    if form.validate_on_submit():
        updated_subject = update_subject(subject_id, form)

        if wants_json():
            return jsonify(SubjectSchema().dump(updated_subject))

        flash("Subject updated successfully", "success")
        return redirect(url_for("subject.get_subject_detail", subject_id=updated_subject.id))

    return jsonify(SubjectSchema().dump(subject))


@subject_bp.route("/<int:subject_id>", methods=["DELETE"])
@role_required("admin")
def delete_subject_route(subject_id):
    deleted = delete_subject(subject_id)

    if not deleted:
        abort(404)

    if wants_json():
        return jsonify({"message": "Subject deleted successfully"}), 200

    flash("Subject deleted successfully", "success")
    return redirect(url_for("subject.get_subjects"))