from flask import abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from App.extensions import db
from App.models.student import Student
from App.models.user import User


def create_students(form):
    user = User(
        username=form.username.data,
        email=form.email.data,
        password=generate_password_hash(form.password.data),
        role="student",
    )
    db.session.add(user)

    student = Student(
        full_name=form.full_name.data,
        email=form.email.data,
        phone=form.phone.data,
        admission_number=form.admission_number.data,
        classroom_id=form.classroom_id.data,
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

    student.full_name = form.full_name.data or student.full_name
    student.email = form.email.data or student.email
    student.phone = form.phone.data or student.phone
    student.admission_number = form.admission_number.data or student.admission_number
    student.classroom_id = form.classroom_id.data if form.classroom_id.data is not None else student.classroom_id

    if student.user is not None:
        student.user.email = form.email.data or student.user.email

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