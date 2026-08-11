from flask import abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.subject import Subject


def create_subject(form):
    subject = Subject(
        name=form.name.data,
        code=form.code.data,
        description=form.description.data,
    )

    try:
        db.session.add(subject)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="A subject with that code already exists.")

    return subject


def get_subject(subject_id):
    return db.session.get(Subject, subject_id)


def get_all_subjects():
    return Subject.query.order_by(Subject.id.desc()).all()


def update_subject(subject_id, form):
    subject = get_subject(subject_id)  # 404s automatically if missing

    subject.name = form.name.data or subject.name
    subject.code = form.code.data or subject.code
    subject.description = form.description.data if form.description.data is not None else subject.description

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="A subject with that code already exists.")

    return subject


def delete_subject(subject_id):
    subject = db.session.get(Subject, subject_id)  # plain lookup — caller decides on missing
    if subject is None:
        return False

    db.session.delete(subject)
    db.session.commit()
    return True


def search_subject_info(search):
    return (
        Subject.query.filter(or_(Subject.name.ilike(f"%{search}%"), Subject.code.ilike(f"%{search}%")))
        .order_by(Subject.id.desc())
        .all()
    )


def serialize_subject(subject):
    return {
        "id": subject.id,
        "name": subject.name,
        "code": subject.code,
        "description": subject.description,
        "created_at": subject.created_at.isoformat() if subject.created_at else None,
        "updated_at": subject.updated_at.isoformat() if subject.updated_at else None,
    }


def paginate_subject(page=1, per_page=10):
    return Subject.query.order_by(Subject.id.desc()).paginate(page=page, per_page=per_page, error_out=False)