from flask import abort
from App.models.exam import Exam
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.services.audit_log_service import create_audit_log
from App.enums.audit import AuditAction

# ================================== Create Exam ===============================
def create_exam(data, actor_id=None):
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

    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.CREATE,
            resource_type="Exam",
            resource_id=exam.id,
            description=f"Created exam {exam.title}",
        )

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
def update_exam(exam_id, form, actor_id=None):
    exam = db.session.get(Exam, exam_id)

    if exam is None:
        return None

    changes = {}
    if form.title and form.title != exam.title:
        changes["title"] = {"before": exam.title, "after": form.title}
    if form.description and form.description != exam.description:
        changes["description"] = {"before": exam.description, "after": form.description}
    if form.subject_id and form.subject_id != exam.subject_id:
        changes["subject_id"] = {"before": exam.subject_id, "after": form.subject_id}
    if form.classroom_id and form.classroom_id != exam.classroom_id:
        changes["classroom_id"] = {"before": exam.classroom_id, "after": form.classroom_id}
    if form.session_id and form.session_id != exam.session_id:
        changes["session_id"] = {"before": exam.session_id, "after": form.session_id}
    if form.exam_date and form.exam_date != exam.exam_date:
        changes["exam_date"] = {"before": str(exam.exam_date), "after": str(form.exam_date)}
    if form.start_time and form.start_time != exam.start_time:
        changes["start_time"] = {"before": str(exam.start_time), "after": str(form.start_time)}
    if form.duration_minutes and form.duration_minutes != exam.duration_minutes:
        changes["duration_minutes"] = {"before": exam.duration_minutes, "after": form.duration_minutes}
    if form.total_marks and form.total_marks != exam.total_marks:
        changes["total_marks"] = {"before": exam.total_marks, "after": form.total_marks}

    exam.title = form.title or exam.title
    exam.description = form.description or exam.description
    exam.subject_id = form.subject_id or exam.subject_id
    exam.classroom_id = form.classroom_id or exam.classroom_id
    exam.session_id = form.session_id or exam.session_id
    exam.exam_date = form.exam_date or exam.exam_date
    exam.start_time = form.start_time or exam.start_time
    exam.duration_minutes = form.duration_minutes or exam.duration_minutes
    exam.total_marks = form.total_marks or exam.total_marks

    db.session.commit()

    if changes and actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.UPDATE,
            resource_type="Exam",
            resource_id=exam.id,
            description=f"Updated exam {exam.title}",
            changes=changes,
        )

    return exam

# ============================ Delete Exam ===============================
def delete_exam(exam_id, actor_id=None):
    exam = db.session.get(Exam, exam_id)

    if exam is None:
        return False

    exam_title = exam.title
    db.session.delete(exam)
    db.session.commit()

    if actor_id:
        create_audit_log(
            actor_id=actor_id,
            action=AuditAction.DELETE,
            resource_type="Exam",
            resource_id=exam_id,
            description=f"Deleted exam {exam_title}",
        )

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