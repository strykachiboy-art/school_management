from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.classroom import Classroom
from App.models.student import Student


def create_classroom(data):
    classroom = Classroom(
        name=data.name,
        capacity=data.capacity or 0,
        location=data.location,
        teacher_id=data.teacher_id or None,
    )

    try:
        db.session.add(classroom)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not create classroom — check for duplicate name.")

    return classroom


def get_all_classrooms(search="", page=1, per_page=10):
    stmt = db.select(Classroom)
    if search:
        stmt = stmt.where(Classroom.name.ilike(f"%{search}%"))

    stmt = stmt.order_by(Classroom.id.desc())
    return db.paginate(stmt, page=page, per_page=per_page, error_out=False)


def get_classroom(classroom_id):
    return db.session.get(Classroom, classroom_id)


def get_all_classroom_list():
    stmt = db.select(Classroom).order_by(Classroom.id.desc())
    return db.session.scalars(stmt).all()


def update_classroom(classroom_id, data):
    classroom = db.session.get(Classroom, classroom_id)
    if classroom is None:
        return None

    classroom.name = data.name or classroom.name
    classroom.capacity = data.capacity if data.capacity is not None else classroom.capacity
    classroom.location = data.location or classroom.location

    if data.teacher_id is not None:
        classroom.teacher_id = data.teacher_id or None

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not update classroom — check for duplicate name.")

    return classroom


def delete_classroom(classroom_id):
    classroom = db.session.get(Classroom, classroom_id)
    if classroom is None:
        return False

    db.session.delete(classroom)
    db.session.commit()
    return True


def bulk_assign_students(classroom_id, student_ids):
    classroom = db.session.get(Classroom, classroom_id)
    if classroom is None:
        return None

    stmt = db.select(Student).where(Student.id.in_(student_ids))
    students = db.session.scalars(stmt).all()

    found_ids = {s.id for s in students}
    missing_ids = [sid for sid in student_ids if sid not in found_ids]

    for student in students:
        student.classroom_id = classroom.id

    db.session.commit()

    return {
        "classroom_id": classroom.id,
        "assigned_ids": sorted(found_ids),
        "missing_ids": missing_ids,
    }


def serialize_classroom(classroom):
    return {
        "id": classroom.id,
        "name": classroom.name,
        "capacity": classroom.capacity,
        "location": classroom.location,
        "teacher_id": classroom.teacher_id,
    }