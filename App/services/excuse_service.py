from datetime import datetime, timezone
from typing import Optional
from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.excuses import Excuse
from App.models.attendance import Attendance
from App.enums.excuse import ExcuseStatus
from App.enums.attendance import AttendanceStatus


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _assert_owns_excuse(excuse: Excuse, student_id: int) -> None:
    if excuse.attendance.student_id != student_id:
        abort(403, description="You can only manage your own excuse requests.")


def create_excuse(attendance_id: int, reason: str, student_id: int) -> Excuse:
    attendance = db.session.get(Attendance, attendance_id)
    if not attendance:
        abort(404, description=f"Attendance record with ID {attendance_id} not found.")

    if attendance.student_id != student_id:
        abort(403, description="You can only submit an excuse for your own attendance record.")

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


def get_excuse(excuse_id: int) -> Excuse:
    excuse = db.session.get(Excuse, excuse_id)
    if not excuse:
        abort(404, description=f"Excuse with ID {excuse_id} not found.")
    return excuse


def get_excuses(
    student_id: Optional[int] = None,
    term_id: Optional[int] = None,
    status: Optional[ExcuseStatus] = None,
):
    stmt = db.select(Excuse).join(Attendance, Excuse.attendance_id == Attendance.id)

    if student_id:
        stmt = stmt.where(Attendance.student_id == student_id)
    if term_id:
        stmt = stmt.where(Attendance.term_id == term_id)
    if status:
        stmt = stmt.where(Excuse.status == status)

    stmt = stmt.order_by(Excuse.created_at.desc())
    return db.session.scalars(stmt).all()


def update_excuse(excuse_id: int, reason: str, student_id: int) -> Excuse:
    excuse = get_excuse(excuse_id)
    _assert_owns_excuse(excuse, student_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot update excuse with status '{excuse.status.value}'. Only PENDING excuses can be modified.",
        )

    excuse.reason = reason
    db.session.commit()
    return excuse


def delete_excuse(excuse_id: int, student_id: int) -> bool:
    excuse = get_excuse(excuse_id)
    _assert_owns_excuse(excuse, student_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot delete excuse with status '{excuse.status.value}'. Only PENDING excuses can be deleted.",
        )

    db.session.delete(excuse)
    db.session.commit()
    return True


def approve_excuse(excuse_id: int, reviewer_id: int) -> Excuse:
    excuse = get_excuse(excuse_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot approve excuse with status '{excuse.status.value}'. Only PENDING excuses can be reviewed.",
        )

    excuse.status = ExcuseStatus.APPROVED
    excuse.reviewed_by = reviewer_id
    excuse.reviewed_at = _utcnow()

    # Sync parent Attendance status to EXCUSED
    excuse.attendance.status = AttendanceStatus.EXCUSED

    db.session.commit()
    return excuse


def reject_excuse(excuse_id: int, reviewer_id: int) -> Excuse:
    excuse = get_excuse(excuse_id)

    if excuse.status != ExcuseStatus.PENDING:
        abort(
            400,
            description=f"Cannot reject excuse with status '{excuse.status.value}'. Only PENDING excuses can be reviewed.",
        )

    excuse.status = ExcuseStatus.REJECTED
    excuse.reviewed_by = reviewer_id
    excuse.reviewed_at = _utcnow()

    # Retain parent Attendance status as ABSENT
    excuse.attendance.status = AttendanceStatus.ABSENT

    db.session.commit()
    return excuse