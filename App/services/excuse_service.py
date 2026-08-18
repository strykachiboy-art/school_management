from datetime import datetime, timezone
from flask import abort
from sqlalchemy.exc import IntegrityError

from typing import Optional
from App.extensions import db
from App.models.excuses import Excuse
from App.models.attendance import Attendance
from App.enums.excuse import ExcuseStatus
from App.enums.attendance import AttendanceStatus


def _utcnow():
    return datetime.now(timezone.utc)


# ============================ 1. Create Excuse ============================

def create_excuse(attendance_id: int, reason: str) -> Excuse:
    """
    Creates a new pending excuse for an existing ABSENT attendance record.
    """
    attendance = db.session.get(Attendance, attendance_id)
    if not attendance:
        abort(404, description=f"Attendance record with ID {attendance_id} not found.")

    if attendance.status != AttendanceStatus.ABSENT:
        abort(
            400,
            description="An excuse can only be submitted for an ABSENT attendance record.",
        )

    existing_excuse = db.session.scalar(
        db.select(Excuse).where(Excuse.attendance_id == attendance_id)
    )
    if existing_excuse:
        abort(
            400,
            description="An excuse request already exists for this attendance record.",
        )

    excuse = Excuse(
        attendance_id=attendance_id,
        reason=reason,
        status=ExcuseStatus.PENDING,
    )

    try:
        db.session.add(excuse)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Could not create excuse due to a database constraint error.")

    return excuse


# ============================ 2. Get Single Excuse ============================

def get_excuse(excuse_id: int) -> Excuse:
    """
    Retrieves a single excuse by ID.
    """
    excuse = db.session.get(Excuse, excuse_id)
    if not excuse:
        abort(404, description=f"Excuse with ID {excuse_id} not found.")
    return excuse


# ============================ 3. Get Excuses ============================

def get_excuses(
    student_id: Optional[int] = None,
    term_id: Optional[int] = None,
    status: Optional[ExcuseStatus] = None,
):
    """
    Retrieves multiple excuses with optional filters for student, term, or status.
    """
    stmt = db.select(Excuse).join(Attendance, Excuse.attendance_id == Attendance.id)

    if student_id:
        stmt = stmt.where(Attendance.student_id == student_id)
    if term_id:
        stmt = stmt.where(Attendance.term_id == term_id)
    if status:
        stmt = stmt.where(Excuse.status == status)

    stmt = stmt.order_by(Excuse.created_at.desc())
    return db.session.scalars(stmt).all()


# ============================ 4. Update Excuse ============================

def update_excuse(excuse_id: int, reason: str) -> Excuse:
    """
    Updates the reason for a PENDING excuse. APPROVED or REJECTED excuses cannot be updated.
    """
    excuse = get_excuse(excuse_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot update excuse with status '{excuse.status.value}'. Only PENDING excuses can be modified.",
        )

    excuse.reason = reason
    db.session.commit()
    return excuse


# ============================ 5. Delete Excuse ============================

def delete_excuse(excuse_id: int) -> bool:
    """
    Deletes a PENDING excuse. APPROVED or REJECTED excuses cannot be deleted.
    """
    excuse = get_excuse(excuse_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot delete excuse with status '{excuse.status.value}'. Only PENDING excuses can be deleted.",
        )

    db.session.delete(excuse)
    db.session.commit()
    return True


# ============================ 6. Approve Excuse ============================

def approve_excuse(excuse_id: int, reviewer_id: int) -> Excuse:
    """
    Approves a PENDING excuse, automatically updating attendance status to EXCUSED.
    """
    excuse = get_excuse(excuse_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot approve excuse with status '{excuse.status.value}'. Only PENDING excuses can be reviewed.",
        )

    excuse.status = ExcuseStatus.APPROVED
    excuse.reviewed_by = reviewer_id
    excuse.reviewed_at = _utcnow()

    # Automatically update Attendance record to EXCUSED
    excuse.attendance.status = AttendanceStatus.EXCUSED

    db.session.commit()
    return excuse


# ============================ 7. Reject Excuse ============================

def reject_excuse(excuse_id: int, reviewer_id: int) -> Excuse:
    """
    Rejects a PENDING excuse, keeping attendance status as ABSENT.
    """
    excuse = get_excuse(excuse_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot reject excuse with status '{excuse.status.value}'. Only PENDING excuses can be reviewed.",
        )

    excuse.status = ExcuseStatus.REJECTED
    excuse.reviewed_by = reviewer_id
    excuse.reviewed_at = _utcnow()

    # Ensure Attendance status stays ABSENT
    excuse.attendance.status = AttendanceStatus.ABSENT

    db.session.commit()
    return excuse