from datetime import datetime, timezone
from typing import Optional
from flask import abort
from sqlalchemy.exc import IntegrityError

from App.extensions import db
from App.models.excuses import Excuse
from App.models.attendance import Attendance
from App.enums.excuse import ExcuseStatus
from App.enums.attendance import AttendanceStatus
from App.services.notification_excuse_service import notify_excuse_decision


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Excuses must be requested within this many days of the absence they cover.
EXCUSE_REQUEST_WINDOW_DAYS = 7


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

    days_since_absence = (_utcnow().date() - attendance.date).days
    if days_since_absence > EXCUSE_REQUEST_WINDOW_DAYS:
        abort(
            400,
            description=(
                f"Excuses must be requested within {EXCUSE_REQUEST_WINDOW_DAYS} days of the "
                f"absence. This absence was {days_since_absence} days ago."
            ),
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
    notify_excuse_decision(excuse)
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
    notify_excuse_decision(excuse)
    return excuse


def bulk_review_excuses(excuse_ids: list, decision: ExcuseStatus, reviewer_id: int) -> dict:
    """
    Approve or reject multiple excuses in one call. Excuses that don't exist or
    aren't PENDING are skipped and reported rather than failing the whole batch.
    """
    if decision not in (ExcuseStatus.APPROVED, ExcuseStatus.REJECTED):
        abort(400, description="decision must be either 'approved' or 'rejected'.")

    excuses = db.session.scalars(
        db.select(Excuse).where(Excuse.id.in_(excuse_ids))
    ).all()

    found_ids = {excuse.id for excuse in excuses}
    not_found = [eid for eid in excuse_ids if eid not in found_ids]

    reviewed = []
    reviewed_excuses = []
    skipped = []
    reviewed_at = _utcnow()

    for excuse in excuses:
        if excuse.status != ExcuseStatus.PENDING:
            skipped.append({"excuse_id": excuse.id, "reason": f"already {excuse.status.value}"})
            continue

        excuse.status = decision
        excuse.reviewed_by = reviewer_id
        excuse.reviewed_at = reviewed_at
        excuse.attendance.status = (
            AttendanceStatus.EXCUSED if decision == ExcuseStatus.APPROVED else AttendanceStatus.ABSENT
        )
        reviewed.append(excuse.id)
        reviewed_excuses.append(excuse)

    db.session.commit()

    for excuse in reviewed_excuses:
        notify_excuse_decision(excuse)

    return {
        "reviewed": reviewed,
        "skipped": skipped,
        "not_found": not_found,
    }