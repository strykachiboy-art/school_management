from flask import abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from App.extensions import db
from App.models.teacher import Teacher
from App.models.user import User


def create_teachers(form):
    user = User(
        username=form.username,
        email=form.email,
        password=generate_password_hash(form.password),
        role="teacher",
    )
    db.session.add(user)

    teacher = Teacher(
        full_name=form.full_name,
        email=form.email,
        phone=form.phone,
    )

    try:
        db.session.flush()  # assigns user.id
        teacher.user_id = user.id
        db.session.add(teacher)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="A user with that username or email already exists.")

    return teacher


def get_all_teachers():
    return Teacher.query.order_by(Teacher.id.desc()).all()


def get_teacher_by_id(teacher_id):
    return db.session.get(Teacher, teacher_id)


def update_teachers(teacher_id, form):
    teacher = db.session.get(Teacher, teacher_id)
    if teacher is None:
        return None

    teacher.full_name = form.full_name or teacher.full_name
    teacher.email = form.email or teacher.email
    teacher.phone = form.phone or teacher.phone

    if teacher.user is not None:
        teacher.user.email = form.email or teacher.user.email

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="That email is already in use.")

    return teacher


def delete_teacher(teacher_id):
    teacher = db.session.get(Teacher, teacher_id)
    if teacher is None:
        return False

    user = teacher.user
    db.session.delete(teacher)
    if user is not None:
        db.session.delete(user)
    db.session.commit()
    return True


def filter_Teacher(**filters):
    query = Teacher.query
    if "id" in filters:
        query = query.filter(Teacher.id == filters["id"])
    if "user_id" in filters:
        query = query.filter(Teacher.user_id == filters["user_id"])
    return query.order_by(Teacher.id.desc()).all()


def search_teacher_info(search):
    return (
        Teacher.query.join(Teacher.user)
        .filter(or_(Teacher.full_name.ilike(f"%{search}%"), User.username.ilike(f"%{search}%")))
        .order_by(Teacher.id.desc())
        .all()
    )


def paginate_teachers(page=1, per_page=10):
    return Teacher.query.order_by(Teacher.id.desc()).paginate(page=page, per_page=per_page, error_out=False)


def sort_teacher(page=1, per_page=10):
    return Teacher.query.order_by(Teacher.id.desc()).paginate(page=page, per_page=per_page, error_out=False)