from flask import abort
from App.models.exam import Exam
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from App.extensions import db

# ================================== Create Exam ===============================
def create_exam(data):
    """data is an ExamCreateRequest (Pydantic) — build the Exam model here."""
    exam = Exam(
        title=data.title,
        description=data.description,
        subject_id=data.subject_id,
        classroom_id=data.classroom_id,
        session_id=data.session_id,
        exam_date=data.exam_date,
        start_time=data.start_time,
        duration_minutes=data.duration_minutes,
        total_marks=data.total_marks,
    )
    try:
        db.session.add(exam)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="A subject with that code already exists.")

    return exam

#=============================== Get exam_id ================================
def get_exam(exam_id):
    return db.session.get(Exam, exam_id)


#============================ Get all Exam ==================================
def get_all_exam():
    return db.session.execute(
        db.select(Exam)
    ).scalars().all()


#============================= Update Exam ===================================
def update_exam(exam_id, form):
    exam = db.session.get(Exam, exam_id)

    if exam is None:
        return None

    exam.title = form.title
    exam.description = form.description
    exam.subject_id = form.subject_id
    exam.classroom_id = form.classroom_id
    exam.session_id = form.session_id
    exam.exam_date = form.exam_date
    exam.start_time = form.start_time
    exam.duration_minutes = form.duration_minutes
    exam.total_marks = form.total_marks

    db.session.commit()
    return exam

# ============================ Delete Exam ===============================
def delete_exam(exam_id):
    exam = db.session.get(Exam, exam_id)

    if exam is None:
        return False

    db.session.delete(exam)
    db.session.commit()
    return True


# =========================== Search and filter ============================
def search_exams(search=None, subject_id=None, classroom_id=None):
    statement = db.select(Exam)

    if search:
        statement = statement.where(
            Exam.title.ilike(f"%{search}%")
        )

    if subject_id:
        statement = statement.where(
            Exam.subject_id == subject_id
        )

    if classroom_id:
        statement = statement.where(
            Exam.classroom_id == classroom_id
        )

    return db.session.execute(statement).scalars().all()


# ========================= paginate_exams ============================
def paginate_exams(page=1, per_page=20):
    statement = db.select(Exam).order_by(Exam.exam_date)

    return db.paginate(statement,
                       page=page,
                       per_page=per_page,
                       error_out=False)