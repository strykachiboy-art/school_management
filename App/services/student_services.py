from flask import abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from App.models import Classroom

from App.extensions import db
from App.models.student import Student
from App.models.user import User


def create_students(form):
    user = User(
        username=form.username,
        email=form.email,
        password=generate_password_hash(form.password),
        role="student",
    )
    db.session.add(user)

    student = Student(
        full_name=form.full_name,
        email=form.email,
        phone=form.phone,
        admission_number=form.admission_number,
        classroom_id=form.classroom_id,
    )

    try:
        db.session.flush()  # assigns user.id
        student.user_id = user.id
        db.session.add(student)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="A user with that username or email already exists.")

    return student


def get_all_students():
    return Student.query.order_by(Student.id.desc()).all()


def get_student_by_id(student_id):
    return db.session.get(Student, student_id)


def update_student(student_id, form):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    student.full_name = form.full_name or student.full_name
    student.email = form.email or student.email
    student.phone = form.phone or student.phone
    student.admission_number = form.admission_number or student.admission_number
    student.classroom_id = form.classroom_id if form.classroom_id is not None else student.classroom_id

    if student.user is not None:
        student.user.email = form.email or student.user.email

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="That email is already in use.")

    return student


def delete_student(student_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return False

    user = student.user
    db.session.delete(student)
    if user is not None:
        db.session.delete(user)
    db.session.commit()
    return True


def search_student_info(search):
    return (
        Student.query.join(Student.user)
        .filter(or_(Student.full_name.ilike(f"%{search}%"), User.username.ilike(f"%{search}%")))
        .order_by(Student.id.desc())
        .all()
    )


def filter_classroom_id(classroom_id):
    return Student.query.filter(Student.classroom_id == classroom_id).order_by(Student.id.desc()).all()


def filter_admission_number(admission_number):
    return Student.query.filter(Student.admission_number == admission_number).order_by(Student.id.desc()).all()


def paginate_students(page=1, per_page=10):
    return Student.query.order_by(Student.id.desc()).paginate(page=page, per_page=per_page, error_out=False)


def sort_student(page=1, per_page=10):
    return Student.query.order_by(Student.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

def add_student_to_classroom(student_id, classroom_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    classroom = db.session.get(Classroom, classroom_id)
    if classroom is None:
        abort(404, description="Classroom not found")

    student.classroom_id = classroom_id
    db.session.commit()
    return student


def delete_student_from_classroom(student_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return None

    student.classroom_id = None
    db.session.commit()
    return student