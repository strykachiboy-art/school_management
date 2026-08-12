from flask import Blueprint, flash, jsonify, redirect, request, url_for, abort
from App.decorators import role_required
from App.forms.classroom_form import ClassroomForm
from App.schemas.classroom_schema import ClassroomSchema
from App.services.classroom_services import (
    create_classroom,
    get_all_classrooms,
    get_classroom,
    get_all_classroom_list,
    update_classroom as update_classroom_service,
    delete_classroom as delete_classroom_service,
)
from App.utils.helpers import wants_json

classroom_bp = Blueprint("classroom", __name__, url_prefix="/classrooms")


@classroom_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_classroom_route():
    form = ClassroomForm()

    if request.method == "POST" and form.validate():
        classroom = create_classroom(form)

        if classroom is None:
            flash("Could not create classroom", "danger")
            return jsonify({"message": "Could not create classroom"}), 400

        if wants_json():
            return jsonify(ClassroomSchema().dump(classroom)), 201

        flash("Classroom created successfully", "success")
        return redirect(url_for("classroom.get_all_classrooms_route"))

    if request.method == "POST":
        return jsonify({"errors": form.errors}), 400

    return jsonify({"message": "Submit classroom fields via POST"}), 200


@classroom_bp.route("", methods=["GET"])
@role_required("admin", "teacher")
def get_all_classrooms_route():
    if request.args.get("list") == "true":
        classrooms = get_all_classroom_list()
        return jsonify(ClassroomSchema(many=True).dump(classrooms))

    page = get_all_classrooms(search=request.args.get("search", "", type=str))

    return jsonify({
        "items": ClassroomSchema(many=True).dump(page.items),
        "page": page.page,
        "pages": page.pages,
        "total": page.total,
    })


@classroom_bp.route("/<int:classroom_id>", methods=["GET"])
@role_required("admin", "teacher")
def get_classroom_detail(classroom_id):
    classroom = get_classroom(classroom_id)
    if classroom is None:
        abort(404)

    return jsonify(ClassroomSchema().dump(classroom))


@classroom_bp.route("/<int:classroom_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def update_classroom_route(classroom_id):
    classroom = get_classroom(classroom_id)
    if classroom is None:
        abort(404)

    form = ClassroomForm(obj=classroom)

    if request.method == "POST" and form.validate():
        updated_classroom = update_classroom_service(classroom_id, form)

        if wants_json():
            return jsonify(ClassroomSchema().dump(updated_classroom))

        flash("Classroom updated successfully", "success")
        return redirect(url_for("classroom.get_classroom_detail", classroom_id=updated_classroom.id))

    if request.method == "POST":
        return jsonify({"errors": form.errors}), 400

    return jsonify(ClassroomSchema().dump(classroom))


@classroom_bp.route("/<int:classroom_id>", methods=["DELETE"])
@role_required("admin")
def delete_classroom_route(classroom_id):
    deleted = delete_classroom_service(classroom_id)

    if not deleted:
        abort(404)

    if wants_json():
        return jsonify({"message": "Classroom deleted successfully"}), 200

    flash("Classroom deleted successfully", "success")
    return redirect(url_for("classroom.get_all_classrooms_route"))