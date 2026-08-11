from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, abort
from App.schemas.student_schema import StudentSchema
from App.decorators import role_required
from App.forms.student_form import StudentForm
from App.services.student_services import (
    create_students,
    get_all_students,
    get_student_by_id,
    update_student as update_student_service,
    delete_student as delete_student_service,
    search_student_info,
    filter_classroom_id,
    filter_admission_number,
    paginate_students,
)
from App.utils.helpers import wants_json

student_bp = Blueprint("student", __name__, url_prefix="/students")


@student_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_student():
    form = StudentForm()

    if form.validate_on_submit():
        student = create_students(form)

        if wants_json():
            return jsonify(StudentSchema().dump(student)), 201

        flash("Student created successfully", "success")
        return redirect(url_for("student.get_all_student"))

    return render_template("admin/create_student.html", form=form)


@student_bp.route("", methods=["GET"])
@role_required("admin")
def get_all_student():
    search = request.args.get("search", "", type=str)
    classroom_id = request.args.get("classroom_id", None, type=int)
    admission_number = request.args.get("admission_number", None, type=str)

    if search:
        students = search_student_info(search)
    elif classroom_id:
        students = filter_classroom_id(classroom_id)
    elif admission_number:
        students = filter_admission_number(admission_number)
    elif request.args.get("paginate") == "true":
        page = paginate_students()
        if wants_json():
            return jsonify({
                "items": [StudentSchema().dump(item) for item in page.items],
                "page": page.page,
                "pages": page.pages,
                "total": page.total,
            })
        return render_template("admin/students.html", students=page.items, page=page)
    else:
        students = get_all_students()

    if wants_json():
        serialized_students = StudentSchema(many=True).dump(students)
        return jsonify(serialized_students)

    return render_template("admin/students.html", students=students)


@student_bp.route("/<int:student_id>", methods=["GET"])
@role_required("admin")
def get_student(student_id):
    student = get_student_by_id(student_id)
    if student is None:
        abort(404)

    if wants_json():
        return jsonify(StudentSchema().dump(student))

    return render_template("admin/student_detail.html", student=student)


@student_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def update_student(student_id):
    student = get_student_by_id(student_id)

    if student is None:
        abort(404)

    form = StudentForm(obj=student)

    if form.validate_on_submit():
        updated_student = update_student_service(student_id, form)

        if wants_json():
            return jsonify(StudentSchema().dump(updated_student))

        flash("Student updated successfully!", "success")
        return redirect(url_for("student.get_student", student_id=updated_student.id))

    return render_template("admin/edit_student.html", form=form, student=student)


@student_bp.route("/<int:student_id>", methods=["DELETE"])
@role_required('admin')
def delete_student(student_id):
    deleted = delete_student_service(student_id)

    if not deleted:
        abort(404)

    if wants_json():
        return jsonify({"message": "Student deleted successfully"}), 200

    flash("Student deleted successfully", "success")
    return redirect(url_for("student.get_all_student"))