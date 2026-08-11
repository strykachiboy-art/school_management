from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, abort
from App.decorators import role_required
from App.forms.teachers_form import TeacherForm
from App.schemas.teacher_schema import TeacherSchema
from App.services.teacher_services import (
    create_teachers,
    update_teachers as update_teacher_service,
    get_teacher_by_id,
    get_all_teachers,
    delete_teacher as delete_teacher_service,
    filter_Teacher,
    search_teacher_info,
    paginate_teachers,
)
from App.services.classroom_services import (
    get_classroom, serialize_classroom
)
from App.utils.helpers import wants_json

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teachers")


@teacher_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_teacher():
    form = TeacherForm()

    if form.validate_on_submit():
        teacher = create_teachers(form)

        if wants_json():
            return jsonify(TeacherSchema().dump(teacher)), 201

        flash("Teacher created successfully", "success")
        return redirect(url_for("teacher.get_all_teacher"))

    return render_template("admin/create_teacher.html", form=form)


@teacher_bp.route("", methods=["GET"])
@role_required("admin")
def get_all_teacher():
    search = request.args.get("search", "", type=str)
    teacher_id = request.args.get("id", None, type=int)
    user_id = request.args.get("user_id", None, type=int)

    if search:
        teacher = search_teacher_info(search)
    elif teacher_id or user_id:
        filters = {}
        if teacher_id:
            filters["id"] = teacher_id
        if user_id:
            filters["user_id"] = user_id
        teacher = filter_Teacher(**filters)
    elif request.args.get("paginate") == "true":
        page = paginate_teachers()
        if wants_json():
            return jsonify({
                "items": [TeacherSchema().dump(item) for item in page.items],
                "page": page.page,
                "pages": page.pages,
                "total": page.total,
            })
        return render_template("admin/teachers.html", teacher=page.items, page=page)
    else:
        teacher = get_all_teachers()

    if wants_json():
        serialized_teachers = TeacherSchema(many=True).dump(teacher)
        return jsonify(serialized_teachers)

    return render_template("admin/teachers.html", teacher=teacher)


@teacher_bp.route("/<int:teacher_id>", methods=["GET"])
@role_required("admin")
def get_teacher(teacher_id):
    teacher = get_teacher_by_id(teacher_id)
    if teacher is None:
        abort(404)

    if wants_json():
        return jsonify(TeacherSchema().dump(teacher))

    return render_template("admin/teachers.html", teacher=teacher)


@teacher_bp.route("/<int:teacher_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def update_teacher(teacher_id):
    teacher = get_teacher_by_id(teacher_id)

    if teacher is None:
        abort(404)

    form = TeacherForm(obj=teacher)

    if form.validate_on_submit():
        updated_teacher = update_teacher_service(teacher_id, form)

        if wants_json():
            return jsonify(TeacherSchema().dump(updated_teacher))

        flash("Teacher updated successfully!", "success")
        return redirect(url_for("teacher.get_teacher", teacher_id=updated_teacher.id))

    return render_template("admin/edit_teacher.html", form=form, teacher=teacher)


@teacher_bp.route("/<int:teacher_id>", methods=["DELETE"])
@role_required("admin")
def delete_teacher(teacher_id):
    deleted = delete_teacher_service(teacher_id)

    if not deleted:
        abort(404)

    if wants_json():
        return jsonify({"message": "Teacher deleted successfully"}), 200

    flash("Teacher deleted successfully", "success")
    return redirect(url_for("teacher.get_all_teacher"))


@teacher_bp.route("/classrooms/<int:classroom_id>", methods=["GET"])
@role_required("admin")
def get_classroom_details(classroom_id):
    classroom = get_classroom(classroom_id)
    if classroom is None:
        abort(404)

    if wants_json():
        return jsonify(serialize_classroom(classroom))

    return render_template("admin/classes.html", classroom=classroom)